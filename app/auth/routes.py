from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_pw = request.form.get('user_pw')
        print('로그인 시도')
        user = db.verify_user(user_name, user_pw) # DB에서 사용자 확인
        print(user)
        if user:
            session['user_id'] = user['user_id']
            session['user_name'] = user['user_name']
            print('로그인 성공')
            print('세션:',session)
            #flash("로그인에 성공했습니다!")
            return redirect(url_for('main.homepage'))
        else:
            print('로그인 실패')
            flash("아이디 또는 비밀번호가 올바르지 않습니다.")
            
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    print('로그아웃')
    return redirect(url_for('main.homepage'))


@auth_bp.route('/signup')
def signup():
    return render_template('auth/signup.html')