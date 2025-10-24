# 도서관 웹 애플리케이션
학교 데이터베이스 수업의 과제로 만든 프로젝트 입니다.
Flask와 MySQL을 사용하여 도서관의 도서, 사용자, 대출 및 예약을 관리하는 웹 애플리케이션입니다. 

## ✨ 주요 기능

* **사용자 인증**:
    * 회원가입 및 로그인 기능 제공.
    * **관리자**와 **일반 사용자** 역할 구분.
    * 관리자 가입 시 특정 코드(학번) 요구.
* **도서 목록**:
    * 전체 도서 목록 표시 (제목, 저자, 카테고리, 총 보유 수량, 대출 가능 수량).
    * **검색**: 제목, 저자, 카테고리로 도서 검색.
    * **정렬**: 제목, 저자, 카테고리 기준 오름차순/내림차순 정렬.
* **대출 및 반납**:
    * 사용자는 대출 가능한 도서를 빌릴 수 있습니다.
    * **대출 규칙**:
        * 사용자당 동시에 최대 3권까지 대출 가능.
        * 동일한 종류의 책을 동시에 2권 이상 대출 불가.
        * 연체 중인 도서(7일 이상 미반납)가 있는 경우 대출 불가.
    * 사용자는 대출 중인 도서를 반납할 수 있습니다.
* **예약**:
    * 사용자는 현재 대출 가능한 재고가 없는 도서를 예약할 수 있습니다.
    * 대출 시 예약자 우선권 부여 (가장 먼저 예약한 사용자만 대출 가능).
    * 도서 대출 성공 시 해당 예약은 자동으로 삭제됨.
    * 연체 중인 사용자는 예약 불가.
* **마이페이지**:
    * 현재 예약 중인 도서 목록 확인.
    * 개인 대출 기록 확인 (날짜순 정렬, 반납 여부 표시).
    * 현재 대출 중인 도서 반납 기능.
* **관리자 기능**:
    * **DB 관리 페이지**:
        * 새로운 책 종류 추가 (제목, 저자, 카테고리).
        * 기존 책 종류의 재고(개별 도서) 추가.
        * 개별 도서 삭제 (대출 중이 아닐 경우에만 가능). 마지막 재고 삭제 시 카테고리 연결 및 책 종류 자동 삭제.
        * 새로운 카테고리 추가.
        * 카테고리 삭제 (해당 카테고리로 분류된 책이 없을 경우에만 가능).
    * **사용자 관리 페이지**:
        * 전체 사용자 목록 확인 (ID, 이름, 역할).
    * **통계/보고서 (추가 기능)**:
        * 유령 회원 식별 (대출 기록 없는 사용자).
        * 다독왕 표시 (대출 횟수 가장 많은 사용자).
* **랭킹 및 차트**:
    * **다독왕 페이지**: 총 대출 횟수 기준 상위 5명 사용자 표시.
    * **인기 도서 페이지**: 최근 3개월간 가장 많이 대출된 도서 종류 및 카테고리 차트 표시.
* **동적 UI**:
    * 홈페이지 '신규 도서' 슬라이더 기능.
    * 사용자 로그인 상태, 대출 상태, 재고 여부, 예약 상태에 따른 버튼(로그인/로그아웃, 대출/예약/대출중/대출불가) 조건부 표시.
    * 사용자 피드백을 위한 토스트 알림 (로그인 성공/실패, 대출 성공/실패 등).

## 🛠️ 기술 스택

* **백엔드**: Python, Flask
* **데이터베이스**: MySQL
* **프론트엔드**: HTML, CSS, JavaScript (Vanilla JS)
* **DB 연결**: `mysql-connector-python`
* **환경 변수 관리**: `python-dotenv`
* **배포**: PythonAnywhere 

## 💾 데이터베이스 스키마

데이터베이스는 다음과 같은 주요 테이블로 구성됩니다:

* `user`: 사용자 정보 저장 (ID, 이름, 해시된 비밀번호, 역할).
* `book_data`: 책 종류 정보 저장 (코드, 제목, 저자).
* `book_status`: 개별 실물 도서 정보 저장 (ID, 책 코드, 대출 상태).
* `category`: 카테고리 이름 저장.
* `book_category`: 책과 카테고리 연결 (다대다 관계).
* `rent`: 대출 기록 저장 (ID, 개별 도서 ID, 사용자 ID, 대출일, 반납일).
* `reservation`: 예약 기록 저장 (ID, 책 코드, 사용자 ID, 예약일).

*(자세한 스키마 및 `ON DELETE CASCADE` 규칙은 `test_db.sql` 파일을 참조하세요).*

## ⚙️ 설정 및 설치 (로컬 개발 환경)

로컬 컴퓨터에서 프로젝트를 설정하는 방법은 다음과 같습니다:

1.  **사전 준비**:
    * Python 3.x 설치.
    * `pip` (Python 패키지 설치 관리자) 설치.
    * MySQL 서버.

2.  **저장소 복제**:
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

3.  **가상 환경 생성 및 활성화**:
    ```bash
    # 가상 환경 생성 (권장)
    python3 -m venv venv 
    # 활성화 (macOS/Linux)
    source venv/bin/activate
    # 또는 Windows:
    # venv\Scripts\activate 
    ```

4.  **의존성 설치**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **환경 변수 설정**:
    * 프로젝트 루트 디렉토리에 `.env` 파일을 생성합니다.
    * 아래 내용을 `.env` 파일에 복사하고, **실제 로컬 MySQL 정보와 강력한 비밀 키로 값을 변경**합니다.
        ```dotenv
        DB_USER=your_local_mysql_username
        DB_PASSWORD=your_local_mysql_password
        DB_HOST=localhost # 또는 MySQL 서버 주소
        DB_NAME=library_db # 사용할 데이터베이스 이름
        SECRET_KEY=generate_a_strong_random_key # 터미널에서 python -c 'import secrets; print(secrets.token_hex(16))' 실행
        # 관리자 가입 로직에 필요하다면 학번 설정
        # ADMIN_CODE=your_student_id 
        ```

6.  **데이터베이스 초기화**:
    * MySQL 서버가 실행 중인지 확인합니다.
    * 사용자 지정 Flask 명령어를 실행하여 데이터베이스(없을 경우) 및 모든 테이블/데이터를 `test_db.sql` 스크립트를 이용해 생성합니다:
        ```bash
        flask db-init 
        # 또는 파일 이름이 다른 경우: flask db-init your_sql_file.sql
        ```
    * *대안*: MySQL 클라이언트를 사용하여 `test_db.sql` 스크립트를 직접 실행할 수 있습니다: `mysql -u your_user -p < test_db.sql`

7.  **개발 서버 실행**:
    ```bash
    python run.py
    ```
    이제 `http://127.0.0.1:5000/` 주소에서 애플리케이션이 실행됩니다.

## 🚀 배포 (PythonAnywhere 예시)

1.  [PythonAnywhere](https://www.pythonanywhere.com/)에 가입/로그인합니다.
2.  **Bash 콘솔**:
    * 저장소 복제: `git clone ...`
    * 프로젝트 디렉토리로 이동: `cd your-repo-name`
    * 가상 환경 생성 및 활성화: `python3 -m venv venv && source venv/bin/activate`
    * 의존성 설치: `pip install -r requirements.txt`
3.  **데이터베이스**:
    * "Databases" 탭으로 이동하여 새 MySQL 데이터베이스를 생성하고 비밀번호를 설정합니다.
    * **호스트 이름**, **사용자 이름**, **데이터베이스 이름**(예: `yourusername$yourdbname`)을 기록해 둡니다.
    * Bash 콘솔로 돌아갑니다.
    * `test_db.sql` 파일 수정: `DROP/CREATE DATABASE` 라인 제거, `USE \`yourusername$yourdbname\`;`가 정확한지 확인.
    * SQL 스크립트 가져오기: `mysql -u yourusername -p -h yourhostname yourusername$yourdbname < test_db.sql`
4.  **웹 앱**:
    * "Web" 탭으로 이동하여 "Add a new web app" 클릭.
    * "Manual configuration" 선택 및 Python 버전 선택.
    * **Virtualenv**: 가상 환경 경로 입력 (예: `/home/yourusername/your-repo-name/venv`).
    * **Code**: "Source code" 및 "Working directory" 경로를 프로젝트 폴더로 설정.
    * **WSGI configuration file**: 파일 편집.
        * `project_home`이 프로젝트 디렉토리를 가리키는지 확인.
        * `app` 패키지에서 `create_app`을 정확히 import하고 `application = create_app()`으로 설정하는지 확인.
        * `.env` 파일을 사용한다면 상단에 `load_dotenv()` 추가.
    * **Environment Variables**: `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `SECRET_KEY`를 PythonAnywhere 데이터베이스 정보와 일치하도록 추가.
5.  **리로드**: "Web" 탭 상단의 녹색 "Reload" 버튼 클릭. `yourusername.pythonanywhere.com` 주소에서 애플리케이션이 실행됩니다.

## 📖 사용법

* 제공된 URL을 통해 사이트에 접속합니다.
* **회원가입**: 일반 사용자 계정을 생성합니다.
* **관리자 가입**: 회원가입 시 "관리자"를 선택하고 정확한 관리자 코드를 입력합니다 (예: 학번).
* **로그인**: 사용자별 기능을 이용합니다.
* **탐색/검색**: "전체 서적" 페이지에서 책을 찾습니다.
* **대출/예약**: 각 책 옆의 버튼을 사용합니다 (가능 여부 및 규칙 적용됨).
* **마이페이지**: 현재 대출 목록 확인, 도서 반납, 예약 목록 확인.
* **관리자 페이지**: 관리자로 로그인한 경우, 헤더나 마이페이지의 링크를 통해 사용자 관리 및 DB 편집 페이지에 접근합니다.

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.