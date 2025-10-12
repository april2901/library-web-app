from flask import Blueprint, render_template
from app import db

mypage_bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@mypage_bp.route('/')
def mypage():

    return render_template('mypage/mypage.html')