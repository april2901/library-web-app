# run.py
from app import create_app
import os
import mysql.connector
import click # Flask CLI 기능을 위해 import

# 1. create_app()을 호출하여 Flask 앱 객체를 만듭니다.
app = create_app()

# 2. @app.cli.command 데코레이터를 사용하여 새로운 명령어를 정의합니다.
@app.cli.command("db-init")
@click.argument("filename", default="test.sql") # 기본 파일 이름을 'test.sql'로 수정
def db_init_command(filename):
    """지정된 SQL 파일을 실행하여 데이터베이스를 초기화합니다."""
    
    # .env 파일에서 DB 접속 정보 가져오기 (database 이름은 제외)
    db_config = {
        'host': os.environ.get('DB_HOST'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD')
    }
    
    conn = None
    cursor = None
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        click.echo(f"'{filename}' 파일을 실행합니다...")
        
        # SQL 파일 열기
        with open(filename, 'r', encoding='utf-8') as f:
            # 여러 SQL 문장이 포함된 스크립트를 한 번에 실행
            for result in cursor.execute(f.read(), multi=True):
                if result.with_rows:
                    click.echo(f"Rows produced by statement '{result.statement}':")
                    click.echo(result.fetchall())
            
        conn.commit()
        click.echo("데이터베이스가 성공적으로 초기화되었습니다.")
        
    except FileNotFoundError:
        click.echo(f"오류: '{filename}' 파일을 찾을 수 없습니다.")
    except mysql.connector.Error as err:
        click.echo(f"데이터베이스 초기화 실패: {err}")
        # 오류 발생 시 롤백 (선택사항이지만 권장)
        if conn:
            conn.rollback() 
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 3. 개발 서버 실행 (기존 코드)
if __name__ == '__main__':
    app.run(debug=True)