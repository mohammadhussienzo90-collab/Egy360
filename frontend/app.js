// =========================================
// EGY360 - Interactive JavaScript
// =========================================

document.addEventListener('DOMContentLoaded', function() {
    initializeSearchTabs();
    initializeNavbar();
    initializeMobileMenu();
    initializeSmoothScroll();
    initializeDateInputs();
    initializeFormSubmissions();
});

// =========================================
// Search Tabs Functionality
// =========================================
function initializeSearchTabs() {
    const tabs = document.querySelectorAll('.search-tab');
    const forms = document.querySelectorAll('.search-form');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabType = this.getAttribute('data-tab');

            // Remove active class from all tabs and forms
            tabs.forEach(t => t.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));

            // Add active class to clicked tab
            this.classList.add('active');

            // Show corresponding form
            const activeForm = document.getElementById(`${tabType}-form`);
            if (activeForm) {
                activeForm.classList.add('active');
            }
        });
    });
}

// =========================================
// Navbar Scroll Effect
// =========================================
function initializeNavbar() {
    const navbar = document.getElementById('navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });
}

// =========================================
// Mobile Menu Toggle
// =========================================
function initializeMobileMenu() {
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.getElementById('navMenu');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');

            // Change icon
            const icon = this.querySelector('i');
            if (navMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
}

// =========================================
// Smooth Scroll
// =========================================
function initializeSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);

                if (target) {
                    const offsetTop = target.offsetTop - 80; // Account for navbar height
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}

// =========================================
// Date Input Initialization
// =========================================
function initializeDateInputs() {
    // Set minimum date to today for check-in/check-out
    const today = new Date().toISOString().split('T')[0];
    const dateInputs = document.querySelectorAll('input[type="date"]');

    dateInputs.forEach(input => {
        input.setAttribute('min', today);
    });

    // Auto-set check-out date when check-in is selected
    const checkInInput = document.getElementById('check-in');
    const checkOutInput = document.getElementById('check-out');

    if (checkInInput && checkOutInput) {
        checkInInput.addEventListener('change', function() {
            const checkInDate = new Date(this.value);
            const checkOutDate = new Date(checkInDate);
            checkOutDate.setDate(checkOutDate.getDate() + 1);

            checkOutInput.value = checkOutDate.toISOString().split('T')[0];
            checkOutInput.setAttribute('min', checkOutDate.toISOString().split('T')[0]);
        });
    }
}

// =========================================
// Form Submissions
// =========================================
function initializeFormSubmissions() {
    const forms = document.querySelectorAll('.search-form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const formId = this.id;
            const formData = new FormData(this);

            console.log(`${formId} submitted:`, Object.fromEntries(formData));

            // In a real application, this would send data to the backend
            // For now, we'll just show a message
            showNotification('Searching for the best options...', 'info');

            // Simulate search and redirect
            setTimeout(() => {
                if (formId === 'accommodations-form') {
                    // window.location.href = '/search/accommodations/';
                    showNotification('Accommodation search completed!', 'success');
                } else if (formId === 'tours-form') {
                    // window.location.href = '/search/tours/';
                    showNotification('Tour search completed!', 'success');
                } else if (formId === 'transportation-form') {
                    // window.location.href = '/search/transportation/';
                    showNotification('Transportation search completed!', 'success');
                }
            }, 1500);
        });
    });
}

// =========================================
// Notification System
// =========================================
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#10B981' : type === 'error' ? '#EF4444' : '#3B82F6'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        font-weight: 600;
        animation: slideIn 0.3s ease-out;
        display: flex;
        align-items: center;
        gap: 12px;
    `;

    const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';
    notification.innerHTML = `<span style="font-size: 20px;">${icon}</span> ${message}`;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add notification animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// =========================================
// Auth Modal Functions
// =========================================
function showAuthModal(type) {
    const modal = document.getElementById('authModal');
    const modalContent = document.getElementById('authModalContent');

    if (type === 'signin') {
        modalContent.innerHTML = `
            <div style="padding: 40px;">
                <h2 style="font-size: 28px; font-weight: 700; margin-bottom: 10px;">Welcome Back</h2>
                <p style="color: #666; margin-bottom: 30px;">Sign in to access your bookings</p>
                
                <form onsubmit="handleAuthSubmit(event, 'signin')">
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 8px;">Email</label>
                        <input type="email" required style="width: 100%; padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                    </div>
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 8px;">Password</label>
                        <input type="password" required style="width: 100%; padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                    </div>
                    <button type="submit" style="width: 100%; padding: 16px; background: #E31E24; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: 700; cursor: pointer;">
                        Sign In
                    </button>
                </form>
                
                <p style="text-align: center; margin-top: 20px; color: #666;">
                    Don't have an account? 
                    <a href="#" onclick="showAuthModal('signup'); return false;" style="color: #E31E24; font-weight: 600;">Sign Up</a>
                </p>
            </div>
        `;
    } else {
        modalContent.innerHTML = `
            <div style="padding: 40px;">
                <h2 style="font-size: 28px; font-weight: 700; margin-bottom: 10px;">Create Account</h2>
                <p style="color: #666; margin-bottom: 30px;">Join Egy360 and start your journey</p>
                
                <form onsubmit="handleAuthSubmit(event, 'signup')">
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 8px;">Full Name</label>
                        <input type="text" required style="width: 100%; padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                    </div>
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 8px;">Email</label>
                        <input type="email" required style="width: 100%; padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                    </div>
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 8px;">Password</label>
                        <input type="password" required style="width: 100%; padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                    </div>
                    <button type="submit" style="width: 100%; padding: 16px; background: #E31E24; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: 700; cursor: pointer;">
                        Create Account
                    </button>
                </form>
                
                <p style="text-align: center; margin-top: 20px; color: #666;">
                    Already have an account? 
                    <a href="#" onclick="showAuthModal('signin'); return false;" style="color: #E31E24; font-weight: 600;">Sign In</a>
                </p>
            </div>
        `;
    }

    modal.classList.add('active');
}

function closeAuthModal() {
    const modal = document.getElementById('authModal');
    modal.classList.remove('active');
}

function handleAuthSubmit(event, type) {
    event.preventDefault();
    closeAuthModal();
    showNotification(type === 'signin' ? 'Signed in successfully!' : 'Account created successfully!', 'success');

    // In real application, would send to backend:
    // const formData = new FormData(event.target);
    // fetch('/api/v1/accounts/users/login/', { ... })
}

// =========================================
// Favorite Button Interaction
// =========================================
document.addEventListener('click', function(e) {
    if (e.target.closest('.btn-favorite')) {
        e.preventDefault();
        const btn = e.target.closest('.btn-favorite');
        const icon = btn.querySelector('i');

        if (icon.classList.contains('far')) {
            icon.classList.remove('far');
            icon.classList.add('fas');
            showNotification('Added to favorites!', 'success');
        } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
            showNotification('Removed from favorites', 'info');
        }
    }
});

// =========================================
// Close Modal on Outside Click
// =========================================
document.addEventListener('click', function(e) {
    const modal = document.getElementById('authModal');
    if (e.target === modal) {
        closeAuthModal();
    }
});

// =========================================
// Lazy Loading Images (Performance)
// =========================================
if ('IntersectionObserver' in window) {
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

    const lazyImages = document.querySelectorAll('img.lazy');
    lazyImages.forEach(img => imageObserver.observe(img));
}

// =========================================
// Export Functions for Global Access
// =========================================
window.showAuthModal = showAuthModal;
window.closeAuthModal = closeAuthModal;
window.handleAuthSubmit = handleAuthSubmit;
window.showNotification = showNotification;

console.log('Egy360 initialized successfully! 🎉');
