document.addEventListener("DOMContentLoaded", () => {
    // 1. Custom Cursor Logic
    const cursor = document.querySelector('.custom-cursor');
    const interactiveElements = document.querySelectorAll('button, .bento-item, .card, .marquee');

    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
    });

    // 2. Magnetic Button Physics
    const magneticBtns = document.querySelectorAll('.magnetic');
    magneticBtns.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            // Вычисляем отклонение мыши от центра кнопки
            const x = (e.clientX - rect.left - rect.width / 2) * 0.4;
            const y = (e.clientY - rect.top - rect.height / 2) * 0.4;
            btn.style.transform = `translate(${x}px, ${y}px)`;
        });
        btn.addEventListener('mouseleave', () => {
            // Пружинный возврат в центр
            btn.style.transform = `translate(0px, 0px)`;
        });
    });

    // 3. Text Reveal Splitter (Разбиваем текст на слова для анимации)
    const revealText = document.querySelector('.reveal-text');
    if (revealText) {
        const words = revealText.innerText.split(' ');
        revealText.innerHTML = '';
        words.forEach((word, i) => {
            const span = document.createElement('span');
            span.innerText = word + ' ';
            span.style.transitionDelay = `${i * 0.05}s`; // Stagger effect
            revealText.appendChild(span);
        });
    }

    // 4. Intersection Observer for Fade-ins and Text Reveal
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { root: null, rootMargin: '0px', threshold: 0.15 });

    document.querySelectorAll('.fade-in, .reveal-text').forEach(element => {
        observer.observe(element);
    });

    // 5. 3D Tilt Effect
    const cards = document.querySelectorAll('.tilt-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -12;
            const rotateY = ((x - centerX) / centerX) * 12;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
        });
    });

    // 6. Smooth Parallax Scroll on Bento Grid Items
    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;
        const parallaxItems = document.querySelectorAll('.parallax-item');
        
        parallaxItems.forEach(item => {
            const speed = item.getAttribute('data-speed');
            // Сдвигаем элементы с разной скоростью относительно скролла
            item.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
});