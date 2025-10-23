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
    top_books = db.get_popular_books_last_3_months(limit=10) 
    top_categories = db.get_popular_categories_last_3_months(limit=5) 
    
    return render_template('main/topbooks.html', top_books=top_books, top_categories=top_categories)



@main_bp.route('/borrow/<int:book_code>', methods=['POST'])
def borrow(book_code):

    if 'user_id' not in session:
        flash("로그인이 필요한 서비스입니다.", "error")
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    user_status = db.get_user_borrowing_status(user_id)

    
    if user_status['is_overdue']:
        flash("연체 중인 도서가 있어 대출할 수 없습니다. 먼저 반납해주세요.", "error")
        return redirect(request.referrer or url_for('main.homepage'))
    if user_status['current_loan_count'] >= 3:
        flash("최대 3권까지만 대출할 수 있습니다.", "error")
        return redirect(request.referrer or url_for('main.homepage'))
    if book_code in user_status['borrowed_book_codes']:
        flash("이미 동일한 종류의 책을 대출 중입니다.", "error")
        return redirect(request.referrer or url_for('main.homepage'))

    
    available_copy_id = db.find_available_copy(book_code)
    
    oldest_reserver_id = db.get_oldest_reservation_user(book_code)

    #예약자가 있을 떄?
    if oldest_reserver_id is not None and available_copy_id is not None:
        # 본인이 젤 빠른 예약 아니면 안돼
        if oldest_reserver_id != user_id:
            flash("해당 도서는 다른 사용자가 먼저 예약하여 대출할 수 없습니다.", "warning")
            return redirect(request.referrer or url_for('main.all_books'))
        
        
    # 아니면 대출 가능
    elif available_copy_id is None:
        flash("해당 도서의 대출 가능한 재고가 없습니다.", "error")
        return redirect(request.referrer or url_for('main.all_books'))

#대출
    try:
        db.borrow_book(user_id, available_copy_id)
        
        # 필요하면 예약 기록 삭제
        if oldest_reserver_id == user_id:
            db.delete_reservation(user_id, book_code)
            flash("예약하신 도서 대출에 성공했습니다!", "success")
        else:
            flash("도서 대출에 성공했습니다!", "success")
            
    except Exception as e:
        flash(f"대출 처리 중 오류가 발생했습니다: {e}", "error")


    return redirect(request.referrer or url_for('main.all_books'))

@main_bp.route('/reserve/<int:book_code>', methods=['POST'])
def reserve(book_code):

    if 'user_id' not in session:
        flash("로그인이 필요한 서비스입니다.", "error")
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    user_status = db.get_user_borrowing_status(user_id)


    if user_status['is_overdue']:
        flash("연체 중인 도서가 있어 예약할 수 없습니다.", "error")
        return redirect(request.referrer or url_for('main.allbooks'))


    available_copy_id = db.find_available_copy(book_code)
    if available_copy_id:
        flash("현재 대출 가능한 재고가 있어 예약할 수 없습니다. 바로 대출해주세요.", "warning")
        return redirect(request.referrer or url_for('main.allbooks'))
        
    # 이미 예약?
    if db.check_existing_reservation(user_id, book_code):
        flash("이미 해당 도서를 예약하셨습니다.", "warning")
        return redirect(request.referrer or url_for('main.allbooks'))
            
    try:
        db.add_reservation(user_id, book_code)
        flash("도서 예약에 성공했습니다!", "success")
    except Exception as e:
        flash(f"예약 처리 중 오류가 발생했습니다: {e}", "error")

    return redirect(request.referrer or url_for('main.allbooks'))