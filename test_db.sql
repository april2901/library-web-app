
USE april2901hanyang$init;

create table users(
    user_id int auto_increment primary key ,
    user_name varchar(50),
    user_pw varchar(20) not null,
    user_role int not null -- 0: 일반 사용자, 1: 관리자
);

create table book_data(
    book_code int auto_increment primary key,
    title varchar(100) not null,
    author varchar(50) not null
);

create table book_status(
    book_id int auto_increment primary key,
    book_code int not null,
    is_rent boolean default false,

    FOREIGN KEY (book_code) REFERENCES book_data(book_code) ON DELETE CASCADE
);

create table category(
    category_id int auto_increment primary key,
    category_name varchar(50) not null
);

create table book_category(
    book_code int not null,
    category_id int not null,

    FOREIGN KEY (book_code) REFERENCES book_data(book_code) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE,
    PRIMARY KEY (book_code, category_id)
);


create table rent(
    rent_id int auto_increment primary key,
    book_id int not null,
    user_id int not null,
    rent_date datetime default current_timestamp,
    return_date datetime,

    foreign key (book_id) references book_status(book_id),
    foreign key (user_id) references users(user_id)
);

create table reservation(
    reservation_id int auto_increment primary key,
    book_code int not null,
    user_id int not null,
    reservation_date datetime default current_timestamp,

    foreign key (book_code) references book_data(book_code),
    foreign key (user_id) references users(user_id)
);

-- 유저
INSERT INTO users(user_name, user_pw, user_role) VALUES('admin1', 'admin_pw_1', 1);
INSERT INTO users(user_name, user_pw, user_role) VALUES('admin2', 'admin_pw_2', 1);
INSERT INTO users(user_name, user_pw, user_role) VALUES('user1', 'user_pw_1', 0);
INSERT INTO users(user_name, user_pw, user_role) VALUES('user2', 'user_pw_2', 0);
INSERT INTO users(user_name, user_pw, user_role) VALUES('user3', 'user_pw_3', 0);
INSERT INTO users(user_name, user_pw, user_role) VALUES('user4', 'user_pw_4', 0);
INSERT INTO users(user_name, user_pw, user_role) VALUES('user5', 'user_pw_5', 0);
INSERT INTO users(user_name, user_pw, user_role) VALUES('user6', 'user_pw_6', 0);
INSERT INTO users(user_name, user_pw, user_role) VALUES('user7', 'user_pw_7', 0);
INSERT INTO users(user_name, user_pw, user_role) VALUES('user8', 'user_pw_8', 0);

-- 카테고리
INSERT INTO category(category_name) VALUES('소설');
INSERT INTO category(category_name) VALUES('과학');
INSERT INTO category(category_name) VALUES('역사');
INSERT INTO category(category_name) VALUES('자기계발');
INSERT INTO category(category_name) VALUES('컴퓨터 공학');
INSERT INTO category(category_name) VALUES('에세이');

-- 서적 정보 데이터 (책 종류)
INSERT INTO book_data(title, author) VALUES('모래 언덕', '프랭크 허버트');
INSERT INTO book_data(title, author) VALUES('파운데이션', '아이작 아시모프');
INSERT INTO book_data(title, author) VALUES('1984', '조지 오웰');
INSERT INTO book_data(title, author) VALUES('멋진 신세계', '올더스 헉슬리');
INSERT INTO book_data(title, author) VALUES('이기적 유전자', '리처드 도킨스');
INSERT INTO book_data(title, author) VALUES('코스모스', '칼 세이건');
INSERT INTO book_data(title, author) VALUES('사피엔스', '유발 하라리');
INSERT INTO book_data(title, author) VALUES('총, 균, 쇠', '재레드 다이아몬드');
INSERT INTO book_data(title, author) VALUES('클린 코드', '로버트 C. 마틴');
INSERT INTO book_data(title, author) VALUES('객체지향의 사실과 오해', '조영호');
INSERT INTO book_data(title, author) VALUES('데일 카네기 인간관계론', '데일 카네기');
INSERT INTO book_data(title, author) VALUES('아주 작은 습관의 힘', '제임스 클리어');
INSERT INTO book_data(title, author) VALUES('아몬드', '손원평');
INSERT INTO book_data(title, author) VALUES('여행의 이유', '김영하');
INSERT INTO book_data(title, author) VALUES('죽은 시인의 사회', 'N. H. 클라인바움');
INSERT INTO book_data(title, author) VALUES('마션', '앤디위어');
INSERT INTO book_data(title, author) VALUES('프로젝트헤일메리', '앤디위어');
INSERT INTO book_data(title, author) VALUES('아르테미스', '앤디위어');

-- 실제 서적 데이터 (실물 책 재고)
-- 모래 언덕 (3권)
INSERT INTO book_status(book_code, is_rent) VALUES(1, TRUE);
INSERT INTO book_status(book_code, is_rent) VALUES(1, FALSE);
INSERT INTO book_status(book_code, is_rent) VALUES(1, FALSE);
-- 파운데이션 (2권)
INSERT INTO book_status(book_code, is_rent) VALUES(2, TRUE);
INSERT INTO book_status(book_code, is_rent) VALUES(2, FALSE);
-- 1984 (1권)
INSERT INTO book_status(book_code, is_rent) VALUES(3, TRUE);
-- 멋진 신세계 (1권)
INSERT INTO book_status(book_code, is_rent) VALUES(4, TRUE);
-- 이기적 유전자 (2권)
INSERT INTO book_status(book_code, is_rent) VALUES(5, TRUE);
INSERT INTO book_status(book_code, is_rent) VALUES(5, FALSE);
-- 코스모스 (1권)
INSERT INTO book_status(book_code, is_rent) VALUES(6, TRUE);
-- 사피엔스 (2권)
INSERT INTO book_status(book_code, is_rent) VALUES(7, TRUE);
INSERT INTO book_status(book_code, is_rent) VALUES(7, FALSE); -- 12
-- 총, 균, 쇠 (1권)
INSERT INTO book_status(book_code, is_rent) VALUES(8, FALSE);
-- 클린 코드 (3권)
INSERT INTO book_status(book_code, is_rent) VALUES(9, TRUE);
INSERT INTO book_status(book_code, is_rent) VALUES(9, FALSE);
INSERT INTO book_status(book_code, is_rent) VALUES(9, FALSE);
-- 객체지향의 사실과 오해 (1권)
INSERT INTO book_status(book_code, is_rent) VALUES(10, FALSE);
-- 데일 카네기 인간관계론 (2권)
INSERT INTO book_status(book_code, is_rent) VALUES(11, FALSE);
INSERT INTO book_status(book_code, is_rent) VALUES(11, FALSE);
-- 아주 작은 습관의 힘 (2권)
INSERT INTO book_status(book_code, is_rent) VALUES(12, TRUE);
INSERT INTO book_status(book_code, is_rent) VALUES(12, FALSE);
-- 아몬드 (2권)
INSERT INTO book_status(book_code, is_rent) VALUES(13, TRUE);
INSERT INTO book_status(book_code, is_rent) VALUES(13, FALSE);
-- 여행의 이유 (1권)
INSERT INTO book_status(book_code, is_rent) VALUES(14, TRUE);
-- 죽은 시인의 사회 (1권)
INSERT INTO book_status(book_code, is_rent) VALUES(15, FALSE);
-- 마션 (2권)
INSERT INTO book_status(book_code, is_rent) VALUES(16, TRUE);
INSERT INTO book_status(book_code, is_rent) VALUES(16, TRUE);
-- 프로젝트헤일메리 (3권)
INSERT INTO book_status(book_code, is_rent) VALUES(17, FALSE);
INSERT INTO book_status(book_code, is_rent) VALUES(17, FALSE);
INSERT INTO book_status(book_code, is_rent) VALUES(17, FALSE);
-- 아르테미스 (1권)
INSERT INTO book_status(book_code, is_rent) VALUES(18, FALSE);

-- 서적-카테고리 연결 데이터
INSERT INTO book_category(book_code, category_id) VALUES(1, 1); -- 모래 언덕: 소설,과학
INSERT INTO book_category(book_code, category_id) VALUES(1, 2);
INSERT INTO book_category(book_code, category_id) VALUES(2, 1); -- 파운데이션: 소설,과학
INSERT INTO book_category(book_code, category_id) VALUES(2, 2);
INSERT INTO book_category(book_code, category_id) VALUES(3, 1); -- 1984: 소설
INSERT INTO book_category(book_code, category_id) VALUES(4, 1); -- 멋진 신세계: 소설
INSERT INTO book_category(book_code, category_id) VALUES(5, 2); -- 이기적 유전자: 과학
INSERT INTO book_category(book_code, category_id) VALUES(6, 2); -- 코스모스: 과학
INSERT INTO book_category(book_code, category_id) VALUES(7, 2); -- 사피엔스: 과학,역사
INSERT INTO book_category(book_code, category_id) VALUES(7, 3);
INSERT INTO book_category(book_code, category_id) VALUES(8, 3); -- 총, 균, 쇠: 역사
INSERT INTO book_category(book_code, category_id) VALUES(9, 5); -- 클린 코드: 컴퓨터 공학
INSERT INTO book_category(book_code, category_id) VALUES(10, 5); -- 객체지향의 사실과 오해: 컴퓨터 공학
INSERT INTO book_category(book_code, category_id) VALUES(11, 4); -- 데일 카네기 인간관계론: 자기계발
INSERT INTO book_category(book_code, category_id) VALUES(12, 4); -- 아주 작은 습관의 힘: 자기계발
INSERT INTO book_category(book_code, category_id) VALUES(13, 1); -- 아몬드: 소설
INSERT INTO book_category(book_code, category_id) VALUES(14, 6); -- 여행의 이유: 에세이
INSERT INTO book_category(book_code, category_id) VALUES(15, 1); -- 죽은 시인의 사회: 소설
INSERT INTO book_category(book_code, category_id) VALUES(16, 1); -- 마션: 소설,과학
INSERT INTO book_category(book_code, category_id) VALUES(16, 2);
INSERT INTO book_category(book_code, category_id) VALUES(17, 1); -- 프로젝트헤일메리: 소설,과학
INSERT INTO book_category(book_code, category_id) VALUES(17, 2);
INSERT INTO book_category(book_code, category_id) VALUES(18, 1); -- 아르테미스: 소설,과학
INSERT INTO book_category(book_code, category_id) VALUES(18, 2);

-- 대출 기록 데이터 (현재 대출중인 책 + 과거 기록)
-- 현재 대출중인 책들 (is_rent가 TRUE인 book_id와 일치)
INSERT INTO rent(book_id, user_id, rent_date) VALUES(9, 1, '2025-10-01 09:00:00'); -- 이기적유전자
INSERT INTO rent(book_id, user_id, rent_date) VALUES(1, 3, '2025-10-11 10:00:00'); -- 모래 언덕
INSERT INTO rent(book_id, user_id, rent_date) VALUES(4, 4, '2025-10-05 14:00:00'); -- 파운데이션
INSERT INTO rent(book_id, user_id, rent_date) VALUES(6, 5, '2025-09-20 11:00:00'); -- 1984
INSERT INTO rent(book_id, user_id, rent_date) VALUES(7, 3, '2025-10-10 18:00:00'); -- 멋진 신세계
INSERT INTO rent(book_id, user_id, rent_date) VALUES(8, 6, '2025-10-13 09:30:00'); -- 이기적유전자
INSERT INTO rent(book_id, user_id, rent_date) VALUES(10, 6, '2025-10-11 09:00:00'); -- 코스모스
INSERT INTO rent(book_id, user_id, rent_date) VALUES(11, 7, '2025-10-08 13:00:00'); -- 사피엔스
INSERT INTO rent(book_id, user_id, rent_date) VALUES(14, 8, '2025-10-09 16:00:00'); -- 클린코드
INSERT INTO rent(book_id, user_id, rent_date) VALUES(20, 5, '2025-10-12 12:00:00'); -- 아주 작은 습관의 힘
INSERT INTO rent(book_id, user_id, rent_date) VALUES(22, 4, '2025-10-07 15:30:00'); -- 아몬드
INSERT INTO rent(book_id, user_id, rent_date) VALUES(24, 3, '2025-10-06 11:30:00'); -- 여행의 이유
INSERT INTO rent(book_id, user_id, rent_date) VALUES(26, 2, '2025-10-02 10:00:00'); -- 마션
INSERT INTO rent(book_id, user_id, rent_date) VALUES(27, 1, '2025-10-03 14:00:00'); -- 마션

-- 과거 대출 기록 (반납 완료)
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(2, 3, '2025-09-01 10:00:00', '2025-09-08 11:00:00');
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(5, 4, '2025-09-02 12:00:00', '2025-09-05 15:00:00');
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(10, 5, '2025-09-10 17:00:00', '2025-09-15 18:00:00');
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(1, 3, '2025-08-20 10:00:00', '2025-08-27 10:30:00');
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(12, 6, '2025-09-15 14:00:00', '2025-09-22 16:00:00');
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(15, 7, '2025-09-18 09:00:00', '2025-09-25 10:00:00');
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(18, 8, '2025-09-20 11:00:00', '2025-09-27 12:00:00');
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(3, 4, '2025-08-05 13:00:00', '2025-08-12 14:00:00');
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(7, 5, '2025-08-10 15:00:00', '2025-08-17 16:00:00');
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(13, 6, '2025-09-25 10:00:00', '2025-10-02 11:00:00');
INSERT INTO rent(book_id, user_id, rent_date, return_date) VALUES(17, 7, '2025-09-28 12:00:00', '2025-10-05 13:00:00');

-- 예약 데이터 (모든 실물 책이 대출중인 책에 대한 예약)
INSERT INTO reservation(book_code, user_id) VALUES(3, 4); -- 1984 (user 4가 예약)
INSERT INTO reservation(book_code, user_id) VALUES(3, 7); -- 1984 (user 7도 예약)
INSERT INTO reservation(book_code, user_id) VALUES(4, 2); -- 멋진 신세계 (user 2가 예약)
INSERT INTO reservation(book_code, user_id) VALUES(5, 1); -- 이기적 유전자 (user 1이 예약)
INSERT INTO reservation(book_code, user_id) VALUES(16, 8); -- 마션 (user 8이 예약)
INSERT INTO reservation(book_code, user_id) VALUES(16, 3); -- 마션 (user 3도 예약)