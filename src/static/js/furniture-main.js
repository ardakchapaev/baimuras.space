
/**
 * BaiMuras Furniture Theme JavaScript
 * Основной JavaScript файл для мебельной темы
 */

class FurnitureTheme {
    constructor() {
        this.navbar = document.querySelector('.furniture-navbar');
        this.scrollToTopBtn = document.getElementById('scrollToTop');
        this.mobileToggler = document.querySelector('.furniture-toggler');
        this.navbarCollapse = document.querySelector('.navbar-collapse');
        
        this.isScrolled = false;
        this.lastScrollTop = 0;
        
        this.init();
    }
    
    static init() {
        new FurnitureTheme();
    }
    
    init() {
        this.bindEvents();
        this.initLazyLoading();
        this.initSmoothScroll();
        this.initFormValidation();
        this.initTooltips();
        this.initImageGallery();
        this.initCounters();
        this.initParallax();
    }
    
    bindEvents() {
        // Scroll events
        window.addEventListener('scroll', () => {
            this.handleScroll();
        });
        
        // Scroll to top button
        if (this.scrollToTopBtn) {
            this.scrollToTopBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.scrollToTop();
            });
        }
        
        // Mobile menu toggle animation
        if (this.mobileToggler) {
            this.mobileToggler.addEventListener('click', () => {
                this.toggleMobileMenu();
            });
        }
        
        // Close mobile menu when clicking on links
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    this.closeMobileMenu();
                }
            });
        });
        
        // Form submissions
        document.querySelectorAll('form[data-furniture-form]').forEach(form => {
            form.addEventListener('submit', (e) => {
                this.handleFormSubmit(e);
            });
        });
        
        // Service card hover effects
        document.querySelectorAll('.service-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.animateServiceCard(card, true);
            });
            
            card.addEventListener('mouseleave', () => {
                this.animateServiceCard(card, false);
            });
        });
        
        // Portfolio item hover effects
        document.querySelectorAll('.portfolio-item').forEach(item => {
            item.addEventListener('mouseenter', () => {
                this.animatePortfolioItem(item, true);
            });
            
            item.addEventListener('mouseleave', () => {
                this.animatePortfolioItem(item, false);
            });
        });
        
        // Resize events
        window.addEventListener('resize', () => {
            this.handleResize();
        });
        
        // Page load completion
        window.addEventListener('load', () => {
            this.onPageLoad();
        });
    }
    
    handleScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Navbar scroll effect
        if (scrollTop > 100 && !this.isScrolled) {
            this.navbar.classList.add('scrolled');
            this.isScrolled = true;
        } else if (scrollTop <= 100 && this.isScrolled) {
            this.navbar.classList.remove('scrolled');
            this.isScrolled = false;
        }
        
        // Scroll to top button visibility
        if (this.scrollToTopBtn) {
            if (scrollTop > 500) {
                this.scrollToTopBtn.classList.add('visible');
            } else {
                this.scrollToTopBtn.classList.remove('visible');
            }
        }
        
        // Parallax effects
        this.updateParallax(scrollTop);
        
        // Update progress indicators
        this.updateScrollProgress();
        
        this.lastScrollTop = scrollTop;
    }
    
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
    
    toggleMobileMenu() {
        const lines = this.mobileToggler.querySelectorAll('.toggler-line');
        
        if (this.navbarCollapse.classList.contains('show')) {
            // Closing animation
            lines[0].style.transform = 'rotate(0deg) translateY(0)';
            lines[1].style.opacity = '1';
            lines[2].style.transform = 'rotate(0deg) translateY(0)';
        } else {
            // Opening animation
            lines[0].style.transform = 'rotate(45deg) translateY(8px)';
            lines[1].style.opacity = '0';
            lines[2].style.transform = 'rotate(-45deg) translateY(-8px)';
        }
    }
    
    closeMobileMenu() {
        if (this.navbarCollapse.classList.contains('show')) {
            const collapseInstance = bootstrap.Collapse.getInstance(this.navbarCollapse);
            if (collapseInstance) {
                collapseInstance.hide();
            }
        }
    }
    
    animateServiceCard(card, isEntering) {
        const image = card.querySelector('.service-image img');
        const overlay = card.querySelector('.service-overlay');
        const icon = card.querySelector('.service-icon');
        
        if (isEntering) {
            if (image) {
                image.style.transform = 'scale(1.1)';
            }
            if (overlay) {
                overlay.style.opacity = '1';
            }
            if (icon) {
                icon.style.transform = 'translateY(-5px)';
            }
        } else {
            if (image) {
                image.style.transform = 'scale(1)';
            }
            if (overlay) {
                overlay.style.opacity = '0';
            }
            if (icon) {
                icon.style.transform = 'translateY(0)';
            }
        }
    }
    
    animatePortfolioItem(item, isEntering) {
        const image = item.querySelector('.portfolio-image img');
        const overlay = item.querySelector('.portfolio-overlay');
        
        if (isEntering) {
            if (image) {
                image.style.transform = 'scale(1.1)';
            }
            if (overlay) {
                overlay.style.opacity = '1';
            }
        } else {
            if (image) {
                image.style.transform = 'scale(1)';
            }
            if (overlay) {
                overlay.style.opacity = '0';
            }
        }
    }
    
    initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const lazyImages = document.querySelectorAll('img[data-src]');
            
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            lazyImages.forEach(img => imageObserver.observe(img));
        }
    }
    
    initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                
                if (target) {
                    const offset = 80; // Учитываем высоту фиксированной навигации
                    const targetPosition = target.offsetTop - offset;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    initFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        
        forms.forEach(form => {
            form.addEventListener('submit', (event) => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }
    
    initTooltips() {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => 
            new bootstrap.Tooltip(tooltipTriggerEl)
        );
    }
    
    initImageGallery() {
        // Простая галерея изображений
        document.querySelectorAll('.image-gallery img').forEach(img => {
            img.addEventListener('click', () => {
                this.openImageModal(img.src, img.alt);
            });
        });
    }
    
    openImageModal(src, alt) {
        const modal = document.createElement('div');
        modal.className = 'furniture-image-modal';
        modal.innerHTML = `
            <div class="modal-backdrop" onclick="this.parentElement.remove()">
                <div class="modal-content" onclick="event.stopPropagation()">
                    <button class="modal-close" onclick="this.closest('.furniture-image-modal').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                    <img src="${src}" alt="${alt}" class="modal-image">
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        document.body.style.overflow = 'hidden';
        
        // Удаление модального окна при нажатии Escape
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                modal.remove();
                document.body.style.overflow = '';
                document.removeEventListener('keydown', handleEscape);
            }
        };
        
        document.addEventListener('keydown', handleEscape);
    }
    
    initCounters() {
        const counters = document.querySelectorAll('[data-count]');
        
        if (counters.length > 0) {
            const counterObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.animateCounter(entry.target);
                        counterObserver.unobserve(entry.target);
                    }
                });
            });
            
            counters.forEach(counter => counterObserver.observe(counter));
        }
    }
    
    animateCounter(element) {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000; // 2 секунды
        const increment = target / (duration / 16); // 60 FPS
        let current = 0;
        
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                element.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        };
        
        updateCounter();
    }
    
    initParallax() {
        this.parallaxElements = document.querySelectorAll('[data-parallax]');
    }
    
    updateParallax(scrollTop) {
        this.parallaxElements.forEach(element => {
            const speed = element.getAttribute('data-parallax') || 0.5;
            const yPos = -(scrollTop * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    }
    
    updateScrollProgress() {
        const progressBars = document.querySelectorAll('.scroll-progress');
        
        progressBars.forEach(bar => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            bar.style.width = scrolled + '%';
        });
    }
    
    handleFormSubmit(event) {
        const form = event.target;
        const submitBtn = form.querySelector('[type="submit"]');
        
        if (submitBtn) {
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
            
            // Удаляем состояние загрузки через 3 секунды (в реальном приложении это будет после ответа сервера)
            setTimeout(() => {
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
            }, 3000);
        }
    }
    
    handleResize() {
        // Обновляем размеры элементов при изменении размера окна
        this.updateElementSizes();
    }
    
    updateElementSizes() {
        // Обновление размеров для адаптивных элементов
        const adaptiveElements = document.querySelectorAll('.adaptive-height');
        
        adaptiveElements.forEach(element => {
            if (window.innerWidth < 768) {
                element.style.height = 'auto';
            } else {
                element.style.height = '';
            }
        });
    }
    
    onPageLoad() {
        // Действия после полной загрузки страницы
        document.body.classList.add('page-loaded');
        
        // Запуск анимаций
        this.triggerAnimations();
    }
    
    triggerAnimations() {
        // Анимация появления элементов
        const animatedElements = document.querySelectorAll('.animate-on-load');
        
        animatedElements.forEach((element, index) => {
            setTimeout(() => {
                element.classList.add('animated');
            }, index * 100);
        });
    }
    
    // Утилитарные методы
    static showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `furniture-notification furniture-notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info'}-circle"></i>
                <span>${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Автоматическое удаление через 5 секунд
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }
    
    static formatPrice(amount, currency = 'сом') {
        return new Intl.NumberFormat('ru-RU').format(amount) + ' ' + currency;
    }
    
    static formatDate(date, options = {}) {
        const defaultOptions = {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };
        
        return new Intl.DateTimeFormat('ru-RU', { ...defaultOptions, ...options }).format(new Date(date));
    }
    
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    static throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// Глобальные функции для использования в HTML
window.showModal = function(modalId) {
    FurnitureTheme.showNotification('Функция в разработке', 'info');
};

window.FurnitureTheme = FurnitureTheme;

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', () => {
    FurnitureTheme.init();
});

// Дополнительные стили для уведомлений
const notificationStyles = `
.furniture-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    max-width: 400px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(139, 69, 19, 0.2);
    transform: translateX(100%);
    animation: slideInNotification 0.3s ease-out forwards;
}

.furniture-notification-success {
    border-left: 4px solid #228B22;
}

.furniture-notification-error {
    border-left: 4px solid #DC3545;
}

.furniture-notification-info {
    border-left: 4px solid #8B4513;
}

.notification-content {
    display: flex;
    align-items: center;
    padding: 1rem 1.5rem;
    gap: 1rem;
}

.notification-content i:first-child {
    font-size: 1.25rem;
}

.notification-content span {
    flex: 1;
    color: var(--furniture-text);
}

.notification-close {
    background: none;
    border: none;
    color: var(--furniture-text-light);
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    transition: background-color 0.2s ease;
}

.notification-close:hover {
    background: var(--furniture-bg-alt);
}

@keyframes slideInNotification {
    to {
        transform: translateX(0);
    }
}

.furniture-image-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.9);
    opacity: 0;
    animation: fadeInModal 0.3s ease-out forwards;
}

.modal-backdrop {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.modal-content {
    position: relative;
    max-width: 90vw;
    max-height: 90vh;
}

.modal-close {
    position: absolute;
    top: -3rem;
    right: 0;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    color: white;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1.25rem;
    transition: background-color 0.2s ease;
}

.modal-close:hover {
    background: rgba(255, 255, 255, 0.2);
}

.modal-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 8px;
}

@keyframes fadeInModal {
    to {
        opacity: 1;
    }
}

@media (max-width: 768px) {
    .furniture-notification {
        top: 10px;
        right: 10px;
        left: 10px;
        max-width: none;
    }
    
    .modal-backdrop {
        padding: 1rem;
    }
    
    .modal-close {
        top: -2.5rem;
        right: -0.5rem;
    }
}
`;

// Добавление стилей в head
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);
