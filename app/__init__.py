from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # .env 파일에서 환경 변수 불러오기
    app.config['DB_USER'] = os.environ.get('DB_USER')
    app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD')
    app.config['DB_HOST'] = os.environ.get('DB_HOST')
    app.config['DB_NAME'] = os.environ.get('DB_NAME')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # db.py에서 사용할 DB 설정 저장
    app.config['DB_CONFIG'] = {
        'user': app.config['DB_USER'],
        'password': app.config['DB_PASSWORD'],
        'host': app.config['DB_HOST'],
        'database': app.config['DB_NAME']
    }

    from .main import routes as main_routes
    from .auth import routes as auth_routes
    from .mypage import routes as mypage_routes
    
    app.register_blueprint(main_routes.main_bp)
    app.register_blueprint(auth_routes.auth_bp)
    app.register_blueprint(mypage_routes.mypage_bp)

    return app