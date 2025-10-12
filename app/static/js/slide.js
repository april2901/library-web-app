document.addEventListener('DOMContentLoaded', function() {
                const wrapper = document.querySelector('.slider-wrapper');
                const prevBtn = document.querySelector('.prev-btn');
                const nextBtn = document.querySelector('.next-btn');
                let slides = document.querySelectorAll('.book-slide');
                
                const slidesPerView = 3;
                const slideCount = slides.length;
                let currentIndex = slidesPerView;
                let isMoving = false; // 애니메이션 동작 중에는 클릭을 막는 '잠금장치'

                // 1. 슬라이드 복제본 만들기
                for (let i = 0; i < slidesPerView; i++) {
                    let cloneFirst = slides[i].cloneNode(true);
                    let cloneLast = slides[slideCount - 1 - i].cloneNode(true);
                    wrapper.append(cloneFirst);
                    wrapper.prepend(cloneLast);
                }
                
                // 2. 초기 위치 설정
                function updatePosition(withAnimation = true) {
                    if (!withAnimation) {
                        wrapper.style.transition = 'none'; // 애니메이션 끔
                    }
                    const offset = -currentIndex * (100 / slidesPerView);
                    wrapper.style.transform = `translateX(${offset}%)`;
                    
                    if (!withAnimation) {
                        // 브라우저가 'none' 상태를 처리할 시간을 준 뒤, 바로 애니메이션을 다시 켬
                        setTimeout(() => {
                            wrapper.style.transition = 'transform 0.5s ease-in-out';
                        }, 50);
                    }
                }
                updatePosition(false); // 첫 로딩 시 애니메이션 없이 초기화

                // 3. 버튼 클릭 이벤트
                nextBtn.addEventListener('click', () => {
                    if (isMoving) return;
                    isMoving = true;
                    currentIndex++;
                    updatePosition();
                });

                prevBtn.addEventListener('click', () => {
                    if (isMoving) return;
                    isMoving = true;
                    currentIndex--;
                    updatePosition();
                });

                // 4. ✨ 여기가 핵심! ✨ 애니메이션이 끝나면 실행될 함수
                wrapper.addEventListener('transitionend', () => {
                    isMoving = false; // 잠금 해제

                    // 가짜 '마지막 페이지'에 도달했다면
                    if (currentIndex >= slideCount + slidesPerView) {
                        currentIndex = slidesPerView;
                        updatePosition(false); // 애니메이션 없이 진짜 '첫 페이지'로 순간이동
                    }
                    
                    // 가짜 '첫 페이지'에 도달했다면
                    if (currentIndex <= slidesPerView - 1) {
                        currentIndex = slideCount + slidesPerView - 1;
                        updatePosition(false); // 애니메이션 없이 진짜 '마지막 페이지'로 순간이동
                    }
                });
            });