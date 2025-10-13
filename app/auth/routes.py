from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app import db
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_pw = request.form.get('user_pw')
        print('로그인 시도 user:', end=' ')
        user = db.verify_user(user_name, user_pw) # DB에서 사용자 확인
        print(user)
        if user:
            session['user_id'] = user['user_id']
            session['user_name'] = user['user_name']
            session['user_role'] = user['user_role']
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
    session.pop('user_role', None)
    print('로그아웃')
    return redirect(url_for('main.homepage'))


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_pw = request.form.get('user_pw')
        user_pw_confirm = request.form.get('user_pw_confirm')
        user_role = int(request.form.get('role'))

        print('회원가입 시도:', user_name, user_pw, user_pw_confirm, user_role)
        
        if user_pw != user_pw_confirm:
            flash("비밀번호가 일치하지 않습니다. 다시 확인해주세요.")
            return redirect(url_for('auth.signup'))

        if db.is_user_exists(user_name):
            flash("이미 사용 중인 아이디입니다.")
            return redirect(url_for('auth.signup'))
        
        if user_role == 0:  # 일반 사용자
            print('일반 사용자로 회원가입')
            db.create_user(user_name, user_pw, user_role)
            flash("회원가입에 성공했습니다. 로그인해주세요.")
            return redirect(url_for('auth.login'))
        elif user_role == 1:  # 관리자
            print('관리자로 회원가입')
            input_admin_code = request.form.get('admin_code')
            additional_key = os.environ.get('ADDITIONAL_KEY')
            if input_admin_code != additional_key:
                flash("관리자 코드가 올바르지 않습니다.")
                return redirect(url_for('auth.signup'))
            db.create_user(user_name, user_pw, user_role)
            flash("회원가입에 성공했습니다. 로그인해주세요.")
            return redirect(url_for('auth.login'))

        
        

    return render_template('auth/signup.html')