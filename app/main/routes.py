from flask import Blueprint, render_template, request,session, redirect, url_for, flash
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def homepage():
    new_book_list = db.get_newbooks()
    top_users_list = db.get_top_rent_users()
    user_status = None
    if 'user_id' in session:
        user_status = db.get_user_borrowing_status(session['user_id'])
    return render_template('main/homepage.html', new_books = new_book_list, top_users = top_users_list, user_status = user_status)

@main_bp.route('/allbooks')
def allbookspage():
    search_term = request.args.get('search')
    sort_column = request.args.get('sort_by', 'title') 
    sort_direction = request.args.get('sort_order', 'asc') 

    all_book_list = db.get_all_books(
        search_query=search_term, 
        sort_by=sort_column, 
        sort_order=sort_direction
    )

    user_status = None
    user_reservations = [] 
    if 'user_id' in session:
        user_id = session['user_id']
        user_status = db.get_user_borrowing_status(user_id)
        reservations_raw = db.get_user_reservations(user_id) 
        user_reservations = [
            r['book_code'] for r in reservations_raw
            if isinstance(r, dict) and 'book_code' in r and r['book_code']
        ]
        
    return render_template('main/allbooks.html', books=all_book_list, user_status=user_status, user_reservations=user_reservations) 
    
@main_bp.route('/topbooks')
def topbookspage():
    top_books = db.get_popular_books_last_3_months(limit=10) # 상위 10권
    top_categories = db.get_popular_categories_last_3_months(limit=5) # 상위 5개 카테고리
    
    return render_template('main/topbooks.html', top_books=top_books, top_categories=top_categories)



@main_bp.route('/borrow/<int:book_code>', methods=['POST'])
def borrow(book_code):
    # 1. 로그인 확인
    if 'user_id' not in session:
        flash("로그인이 필요한 서비스입니다.", "error")
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    user_status = db.get_user_borrowing_status(user_id)

    # 2. 대출 규칙 검사
    if user_status['is_overdue']:
        flash("연체 중인 도서가 있어 대출할 수 없습니다. 먼저 반납해주세요.", "error")
        return redirect(request.referrer or url_for('main.homepage'))
    if user_status['current_loan_count'] >= 3:
        flash("최대 3권까지만 대출할 수 있습니다.", "error")
        return redirect(request.referrer or url_for('main.homepage'))
    if book_code in user_status['borrowed_book_codes']:
        flash("이미 동일한 종류의 책을 대출 중입니다.", "error")
        return redirect(request.referrer or url_for('main.homepage'))

    # 3. 대출 가능한 책 찾기
    available_copy_id = db.find_available_copy(book_code)
    # 4. 예약자 우선 처리 (✨ 여기가 핵심!)
    oldest_reserver_id = db.get_oldest_reservation_user(book_code)

    # 4-1. 예약자가 있고, 대출 가능한 책이 방금 반납된 예약 도서일 경우
    if oldest_reserver_id is not None and available_copy_id is not None:
        # 현재 대출 시도자가 가장 먼저 예약한 사람이 아니라면, 대출 불가
        if oldest_reserver_id != user_id:
            flash("해당 도서는 다른 사용자가 먼저 예약하여 대출할 수 없습니다.", "warning")
            return redirect(request.referrer or url_for('books.all_books'))
        # 현재 대출 시도자가 가장 먼저 예약한 사람이라면, 대출 진행 (아래 4-2로 넘어감)
        
    # 4-2. 예약자가 없거나, 대출 시도자가 예약자 본인일 경우 대출 진행
    elif available_copy_id is None:
        flash("해당 도서의 대출 가능한 재고가 없습니다.", "error")
        return redirect(request.referrer or url_for('books.all_books'))

    # 5. 대출 실행
    try:
        db.borrow_book(user_id, available_copy_id)
        
        # 5-1. 만약 이 사용자가 예약자였다면, 예약 기록 삭제 (✨ 여기가 핵심!)
        if oldest_reserver_id == user_id:
            db.delete_reservation(user_id, book_code)
            flash("예약하신 도서 대출에 성공했습니다!", "success")
        else:
            flash("도서 대출에 성공했습니다!", "success")
            
    except Exception as e:
        flash(f"대출 처리 중 오류가 발생했습니다: {e}", "error")

    # 6. 이전 페이지로 리다이렉트
    return redirect(request.referrer or url_for('books.all_books'))

@main_bp.route('/reserve/<int:book_code>', methods=['POST'])
def reserve(book_code):
    # 1. 로그인 확인
    if 'user_id' not in session:
        flash("로그인이 필요한 서비스입니다.", "error")
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    user_status = db.get_user_borrowing_status(user_id)

    # 2. 예약 규칙 검사
    if user_status['is_overdue']:
        flash("연체 중인 도서가 있어 예약할 수 없습니다.", "error")
        return redirect(request.referrer or url_for('main.allbooks'))

    # 3. 실제 재고 확인 (혹시 모를 상황 대비)
    available_copy_id = db.find_available_copy(book_code)
    if available_copy_id:
        flash("현재 대출 가능한 재고가 있어 예약할 수 없습니다. 바로 대출해주세요.", "warning")
        return redirect(request.referrer or url_for('main.allbooks'))
        
    # 4. 이미 예약했는지 확인
    if db.check_existing_reservation(user_id, book_code):
        flash("이미 해당 도서를 예약하셨습니다.", "warning")
        return redirect(request.referrer or url_for('main.allbooks'))
            
    # 5. 예약 실행
    try:
        db.add_reservation(user_id, book_code)
        flash("도서 예약에 성공했습니다!", "success")
    except Exception as e:
        flash(f"예약 처리 중 오류가 발생했습니다: {e}", "error")

    # 6. 이전 페이지로 리다이렉트
    return redirect(request.referrer or url_for('main.allbooks'))