from flask import Blueprint, render_template
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def homepage():
    new_book_list = db.get_newbooks()
    top_users_list = db.get_top_rent_users()
    
    return render_template('main/homepage.html', new_books = new_book_list, top_users = top_users_list)