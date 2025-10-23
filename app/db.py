import mysql.connector
from flask import current_app
from datetime import datetime, timedelta

def get_db_connection():
    conn = mysql.connector.connect(**current_app.config['DB_CONFIG'])
    return conn


def execute_query(query, params=None, fetch=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    
    if fetch == 'all':
        result = cursor.fetchall()
    elif fetch == 'one':
        result = cursor.fetchone()
    elif fetch == 'lastrowid':
        result = cursor.lastrowid
        conn.commit()
    else:
        conn.commit()
        result = None
        
    cursor.close()
    conn.close()
    
    return result

#최신 등록 순 6권
def get_newbooks():
    query = '''
        SELECT * FROM book_data
        ORDER BY book_code DESC
        LIMIT 6;
        '''
    print('get_newbooks 호출')
    return execute_query(query, fetch='all')

#유저 확인
def verify_user(name, pw):
    print('verify_user 호출:', name, pw)
    query = '''
        SELECT user_id, user_name, user_role FROM users
        WHERE user_name = %s AND user_pw = %s;
    '''
    params = (name, pw)
    result = execute_query(query, params=params, fetch='one')
    print('verify_user result:', result)
    return result

#유저 있는지 확인
def is_user_exists(name):
    print('is_user_exists 호출:', name)
    query = '''
        SELECT user_id FROM users
        WHERE user_name = %s;
    '''
    params = (name,)
    result = execute_query(query, params=params, fetch='one')
    print('is_user_exists 호출:', result)
    return result is not None

#유저 등록
def create_user(name, pw, user_role):
    print('create_user 호출:', name, pw, user_role)
    query = '''
        INSERT INTO users(user_name, user_pw, user_role) VALUES (%s, %s, %s);
    '''
    params = (name, pw, user_role)
    execute_query(query, params=params)
    
#대여 많이 한 유저 5명
def get_top_rent_users():
    query = '''
        SELECT user_name, COUNT(rent_id) as rent_count
        FROM rent NATURAL JOIN users
        GROUP BY user_id
        ORDER BY COUNT(rent_id) DESC
        LIMIT 5;
    '''
    print('get_top_rent_users 호출')
    return execute_query(query, fetch='all')

#모든 유저 받아오기
def get_all_users():
    query = '''
        SELECT user_id, user_name, user_role
        FROM users
        ORDER BY user_id ASC;
    '''
    print('get_all_users 호출')
    return execute_query(query, fetch='all')

#유령회원 리스트 받기
def get_ghost_users():
    query = '''
        SELECT user_id, user_name, user_role
        FROM users
        WHERE user_id NOT IN (SELECT DISTINCT user_id FROM rent);
    '''
    print('get_ghost_users 호출')
    return execute_query(query, fetch='all')

#모든 책 카테고리 포함해 받아오기
def get_all_books_with_categories():
    query = """ㅈ
        SELECT book_id, title, author, GROUP_CONCAT(category_name SEPARATOR ', ') AS categories, is_rent
        FROM book_status LEFT JOIN book_data ON book_status.book_code = book_data.book_code
        LEFT JOIN book_category ON book_data.book_code = book_category.book_code
        LEFT JOIN category ON book_category.category_id = category.category_id
        GROUP BY book_data.book_code, book_id
        ORDER BY book_id ASC;
    """
    print('get_all_books_with_categories 호출')
    return execute_query(query, fetch='all')


#책 추가
def add_book(title, author, category_ids):
    print('add_book 호출:', title, author, category_ids)
    #있는 책 종류인지?
    find_book_query = "SELECT book_code FROM book_data WHERE title = %s AND author = %s;"
    existing_book = execute_query(find_book_query, params=(title, author), fetch='one')

    #있는 종류면 재고 하나 추가, 대여는 기본 False
    if existing_book:
        book_code = existing_book['book_code']
        add_copy_query = "INSERT INTO book_status (book_code) VALUES (%s);"
        execute_query(add_copy_query, params=(book_code,))
        
    #없는 거면 book_data에 추가하고 code받아옴
    else:
        add_book_query = "INSERT INTO book_data (title, author) VALUES (%s, %s);"
        new_book_code = execute_query(add_book_query, params=(title, author), fetch='lastrowid')

        #book_status에 재고 추가
        add_copy_query = "INSERT INTO book_status (book_code) VALUES (%s);"
        execute_query(add_copy_query, params=(new_book_code,))

        #여러개 카테고리 처리
        if category_ids: #category_ids = ['1', '2']
            
            category_query_parts = []
            params = []
            for cat_id in category_ids:
                category_query_parts.append("(%s, %s)")
                params.extend([new_book_code, cat_id])
                
                #category_query_parts : ['(%s, %s)', '(%s, %s)']
                #[101, '1', 101, '2'] book_code=101가정
            
            # 최종 쿼리 문자열 생성 "INSERT INTO book_category (book_code, category_id) VALUES (%s, %s), (%s, %s);"
            category_query = f"INSERT INTO book_category (book_code, category_id) VALUES {', '.join(category_query_parts)};"
            execute_query(category_query, params=tuple(params))



def delete_book(book_id):
    print('delete_book 호출:', book_id, end=' ')
    #삭제할 id를 가진 책의 code찾기
    find_code_query = "SELECT book_code FROM book_status WHERE book_id = %s;"
    book = execute_query(find_code_query, params=(book_id,), fetch='one')
    

    book_code = book['book_code']

    #삭제
    delete_copy_query = "DELETE FROM book_status WHERE book_id = %s;"
    execute_query(delete_copy_query, params=(book_id,))

    # 같은 종류 책 더있는지?
    count_query = "SELECT COUNT(*) AS copy_count FROM book_status WHERE book_code = %s;"
    remaining = execute_query(count_query, params=(book_code,), fetch='one')

    # 더 없으면 다 지워
    if remaining and remaining['copy_count'] == 0:
        print(f"Book code {book_code}의 마지막 책 삭제. 관련 데이터도 삭제.")
        
        #1
        delete_category_link_query = "DELETE FROM book_category WHERE book_code = %s;"
        execute_query(delete_category_link_query, params=(book_code,))
        
        #2
        delete_book_data_query = "DELETE FROM book_data WHERE book_code = %s;"
        execute_query(delete_book_data_query, params=(book_code,))

def get_all_categories_with_count():
    print('get_all_categories_with_count 호출')
    query = """
        SELECT c.category_id, c.category_name, COUNT(bc.book_code) AS book_count
        FROM category AS c LEFT JOIN book_category AS bc ON c.category_id = bc.category_id
        GROUP BY c.category_id
        ORDER BY c.category_id;
    """
    return execute_query(query, fetch='all')


def add_category(category_name):
    print('add_category 호출:', category_name)
    query = "INSERT INTO category (category_name) VALUES (%s);"
    execute_query(query, params=(category_name,))

def is_category_exists(category_name):
    print('is_category_exists 호출:', category_name)
    query = "SELECT category_id FROM category WHERE category_name = %s;"
    result = execute_query(query, params=(category_name,), fetch='one')
    return result is not None

def delete_category(category_id):
    print('delete_category 호출:', category_id)
    query = "DELETE FROM category WHERE category_id = %s;"
    execute_query(query, params=(category_id,))
    
    
#유저 예약 기록 받아오기
def get_user_reservations(user_id):
    print('get_user_reservations 호출:', user_id)
    query = """
        SELECT bd.title, bd.author, r.reservation_date, r.book_code
        FROM reservation AS r
        JOIN book_data AS bd ON r.book_code = bd.book_code
        WHERE r.user_id = %s
        ORDER BY r.reservation_date DESC;
    """
    return execute_query(query, params=(user_id,), fetch='all')

#유저 대여 기록 받아오기
def get_user_rentals(user_id):
    print('get_user_rentals 호출:', user_id)
    query = """
        SELECT r.rent_id, bd.title, bd.author, r.rent_date, r.return_date, r.book_id
        FROM rent AS r
        JOIN book_status AS bs ON r.book_id = bs.book_id
        JOIN book_data AS bd ON bs.book_code = bd.book_code
        WHERE r.user_id = %s
        ORDER BY r.rent_date DESC;
    """
    return execute_query(query, params=(user_id,), fetch='all')

#책 반납
def return_book(rent_id):
    print('return_book 호출:', rent_id)
   
    update_rent_query = "UPDATE rent SET return_date = NOW() WHERE rent_id = %s;"
    execute_query(update_rent_query, params=(rent_id,))

    
    update_status_query = """
        UPDATE book_status 
        SET is_rent = FALSE 
        WHERE book_id = (SELECT book_id FROM rent WHERE rent_id = %s);
    """
    execute_query(update_status_query, params=(rent_id,))
    

#모든 책 받아오기
def get_all_books(search_query=None, sort_by='title', sort_order='asc'):
    # 기본
    base_query = """
        SELECT
            bd.book_code, bd.title, bd.author,
            GROUP_CONCAT(DISTINCT c.category_name ORDER BY c.category_name SEPARATOR ', ') AS categories,
            COUNT(DISTINCT bs.book_id) AS total_quantity,
            COALESCE(avail_counts.available_count, 0) AS available_quantity 
        FROM book_data AS bd
        LEFT JOIN book_status AS bs ON bd.book_code = bs.book_code 
        LEFT JOIN book_category AS bc ON bd.book_code = bc.book_code
        LEFT JOIN category AS c ON bc.category_id = c.category_id
        LEFT JOIN (
            SELECT book_code, COUNT(book_id) AS available_count
            FROM book_status
            WHERE is_rent = FALSE
            GROUP BY book_code
        ) AS avail_counts ON bd.book_code = avail_counts.book_code
    """
    
    params = []
    where_sql = ""

    # 검색
    if search_query:
        search_pattern = f"%{search_query}%"
        where_sql = " WHERE (bd.title LIKE %s OR bd.author LIKE %s OR c.category_name LIKE %s)"
        params.extend([search_pattern, search_pattern, search_pattern])

    # 최종
    final_query = base_query + where_sql
    final_query += " GROUP BY bd.book_code"

    # 정렬
    allowed_sort_columns = {'title': 'bd.title', 'author': 'bd.author', 'category': 'categories'}
    sort_column = allowed_sort_columns.get(sort_by, 'bd.title')
    order = 'DESC' if sort_order.lower() == 'desc' else 'ASC'
    final_query += f" ORDER BY {sort_column} {order}"

    return execute_query(final_query, params=tuple(params), fetch='all')


#최근 3개월간 가장 인기있는 책 상위 10권
def get_popular_books_last_3_months(limit=10):
    """최근 3개월간 가장 많이 대출된 책 (종류별) 순위를 반환합니다."""
    # 3개월 전 날짜 계산
    three_months_ago = datetime.now() - timedelta(days=90)
    
    query = """
        SELECT bd.title, bd.author, COUNT(r.rent_id) AS rental_count
        FROM rent AS r
        JOIN book_status AS bs ON r.book_id = bs.book_id
        JOIN book_data AS bd ON bs.book_code = bd.book_code
        WHERE r.rent_date >= %s 
        GROUP BY bd.book_code
        ORDER BY rental_count DESC
        LIMIT %s;
    """
    
    return execute_query(query, params=(three_months_ago, limit), fetch='all')

# 가장 인기있는 카테고리 상위 5개
def get_popular_categories_last_3_months(limit=5):
    three_months_ago = datetime.now() - timedelta(days=90)
    
    query = """
        SELECT c.category_name, COUNT(r.rent_id) AS rental_count
        FROM rent AS r
        JOIN book_status AS bs ON r.book_id = bs.book_id
        JOIN book_category AS bc ON bs.book_code = bc.book_code
        JOIN category AS c ON bc.category_id = c.category_id
        WHERE r.rent_date >= %s
        GROUP BY c.category_id
        ORDER BY rental_count DESC
        LIMIT %s;
    """
    return execute_query(query, params=(three_months_ago, limit), fetch='all')

#유저 대출 상태 확인
def get_user_borrowing_status(user_id):
    
    query = """
        SELECT r.rent_date, bs.book_code
        FROM rent AS r
        JOIN book_status AS bs ON r.book_id = bs.book_id
        WHERE r.user_id = %s AND r.return_date IS NULL;
    """
    current_rentals = execute_query(query, params=(user_id,), fetch='all')

    current_loan_count = len(current_rentals)
    is_overdue = False
    borrowed_book_codes = set() 

    seven_days_ago = datetime.now() - timedelta(days=7)
    for rental in current_rentals:
        borrowed_book_codes.add(rental['book_code'])
        # rent_date가 7일보다 오래되면
        if rental['rent_date'] < seven_days_ago:
            is_overdue = True
            break 

    return {
        'current_loan_count': current_loan_count,
        'is_overdue': is_overdue,
        'borrowed_book_codes': list(borrowed_book_codes) 
    }

#대출 가능한 책 찾기
def find_available_copy(book_code):
    query = """
        SELECT book_id FROM book_status
        WHERE book_code = %s AND is_rent = FALSE
        LIMIT 1; 
    """
    result = execute_query(query, params=(book_code,), fetch='one')
    return result['book_id'] if result else None

#책빌리기
def borrow_book(user_id, book_id):
    # 대여 기록 추가
    add_rent_query = "INSERT INTO rent (user_id, book_id, rent_date) VALUES (%s, %s, NOW());"
    execute_query(add_rent_query, params=(user_id, book_id))

    # 책 상태 대여중
    update_status_query = "UPDATE book_status SET is_rent = TRUE WHERE book_id = %s;"
    execute_query(update_status_query, params=(book_id,))

    
#이미 예약했는지?
def check_existing_reservation(user_id, book_code):
    query = "SELECT reservation_id FROM reservation WHERE user_id = %s AND book_code = %s;"
    result = execute_query(query, params=(user_id, book_code), fetch='one')
    return result is not None 

#예약하기
def add_reservation(user_id, book_code):
    query = "INSERT INTO reservation (user_id, book_code, reservation_date) VALUES (%s, %s, NOW());"
    execute_query(query, params=(user_id, book_code))
    
#예약 삭제하기
def delete_reservation(user_id, book_code):
    query = "DELETE FROM reservation WHERE user_id = %s AND book_code = %s;"
    execute_query(query, params=(user_id, book_code))

#가장 먼저 예약한 사용자 찾기
def get_oldest_reservation_user(book_code):
    query = """
        SELECT user_id FROM reservation 
        WHERE book_code = %s ㄱㅂㅂrereㅎ
        ORDER BY reservation_date ASC 
        LIMIT 1;
    """
    result = execute_query(query, params=(book_code,), fetch='one')
    return result['user_id'] if result else None