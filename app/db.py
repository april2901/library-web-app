import mysql.connector
from flask import current_app

def get_db_connection():
    conn = mysql.connector.connect(**current_app.config['DB_CONFIG'])
    return conn


def execute_query(query, params=None, fetch=None):
    """DB 쿼리 실행을 처리하는 중앙 함수.

    Args:
        query (str): 실행할 SQL 쿼리.
        params (tuple, optional): 쿼리에 전달할 파라미터. SQL 인젝션 방지.
        fetch (str, optional): 'one' 또는 'all'을 지정하여 결과를 가져옴. 지정하지 않으면 데이터를 변경(commit)만 함.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    
    # 1. fetch 인자에 따라 다른 동작 수행
    if fetch == 'all':
        result = cursor.fetchall()
    elif fetch == 'one':
        result = cursor.fetchone()
    else:
        # 2. SELECT가 아닌 INSERT, UPDATE, DELETE 쿼리는 commit이 필요
        conn.commit()
        result = None
        
    cursor.close()
    conn.close()
    
    return result

def get_newbooks():
    query = '''
        SELECT * FROM book_data
        ORDER BY book_code DESC
        LIMIT 6;
        '''
    print('get_newbooks called')
    return execute_query(query, fetch='all')

def verify_user(name, pw):
    print('verify_user called with:', name, pw)
    query = '''
        SELECT user_id, user_name FROM users
        WHERE user_name = %s AND user_pw = %s;
    '''
    params = (name, pw)
    result = execute_query(query, params=params, fetch='one')
    print('verify_user result:', result)
    return result