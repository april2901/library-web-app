from flask import Blueprint, render_template
from app import db
from flask import request, redirect, url_for, flash, session

mypage_bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@mypage_bp.route('/', methods=['GET', 'POST'])
def mypage():

    if 'user_id' not in session:
        flash("로그인이 필요한 서비스입니다.")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    #반납하기 눌렀을 때
    if request.method == 'POST':
        rent_id_to_return = request.form.get('rent_id')
        if rent_id_to_return:
            db.return_book(rent_id_to_return)
            flash("책이 성공적으로 반납되었습니다.")
        return redirect(url_for('mypage.mypage'))


    reservations = db.get_user_reservations(user_id)
    rentals = db.get_user_rentals(user_id)

    return render_template('mypage/mypage.html', reservations=reservations, rentals=rentals)

@mypage_bp.route('/admin')
def adminpage():
    users_list = db.get_all_users()
    ghost_users_list = db.get_ghost_users()
    return render_template('mypage/adminpage.html', users = users_list, ghost_users = ghost_users_list)


@mypage_bp.route('admin/dbedit', methods=['GET', 'POST'])
def dbeditpage():

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'add_book':
            title = request.form.get('title')
            author = request.form.get('author')
            category_ids = request.form.getlist('categories') 
            db.add_book(title, author, category_ids)
            flash("새로운 책이 추가되었습니다.")
            print('책 추가', title, author, category_ids)
        
        elif form_type == 'delete_book':
            book_id = request.form.get('book_id')
            db.delete_book(book_id)
            flash("책이 삭제되었습니다.")
            print('책 삭제, id=', book_id)

        elif form_type == 'add_category':
            if db.is_category_exists(request.form.get('category_name')):
                flash("이미 존재하는 카테고리입니다.")
                
                return redirect(url_for('mypage.dbeditpage'))
            
            category_name = request.form.get('category_name')
            db.add_category(category_name)
            flash("새로운 카테고리가 추가되었습니다.")
            print('카테고리 추가', category_name)
            
        elif form_type == 'delete_category':
            category_id = request.form.get('category_id')
            db.delete_category(category_id)
            flash("카테고리가 삭제되었습니다.")
            print('카테고리 삭제, id=', category_id)
        
        return redirect(url_for('mypage.dbeditpage'))

    all_books = db.get_all_books_with_categories()
    all_categories = db.get_all_categories_with_count()
    
    return render_template('mypage/dbeditpage.html', books=all_books, categories=all_categories)