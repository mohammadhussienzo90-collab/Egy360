/* =========================================
   EGY360 - Homepage Script
   Search tabs, navigation, auth modals
   ========================================= */

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏠 Initializing homepage...');

    setupSearchTabs();
    setupNavigation();
    setupMobileMenu();
    setupDateDefaults();

    console.log('✅ Homepage initialized successfully');
});

// Setup Search Tabs
function setupSearchTabs() {
    const tabs = document.querySelectorAll('.search-tab');
    const forms = document.querySelectorAll('.search-form');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabName = this.dataset.tab;

            // Remove active class from all tabs and forms
            tabs.forEach(t => t.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));

            // Add active class to clicked tab and corresponding form
            this.classList.add('active');
            const activeForm = document.getElementById(`${tabName}-form`);
            if (activeForm) {
                activeForm.classList.add('active');
            }

            console.log('🔄 Switched to tab:', tabName);
        });
    });

    console.log('✅ Search tabs initialized');
}

// Setup Navigation
function setupNavigation() {
    const navbar = document.getElementById('navbar');

    if (!navbar) return;

    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            // Don't prevent default for just "#"
            if (href === '#') return;

            e.preventDefault();

            const target = document.querySelector(href);
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    console.log('✅ Navigation initialized');
}

// Setup Mobile Menu
function setupMobileMenu() {
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.getElementById('navMenu');

    if (!mobileToggle || !navMenu) return;

    mobileToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');

        // Toggle icon
        const icon = this.querySelector('i');
        if (icon) {
            if (navMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!navMenu.contains(e.target) && !mobileToggle.contains(e.target)) {
            navMenu.classList.remove('active');
            const icon = mobileToggle.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    });

    console.log('✅ Mobile menu initialized');
}

// Setup Date Defaults
function setupDateDefaults() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const formatDate = (date) => {
        return date.toISOString().split('T')[0];
    };

    // Accommodation dates
    const checkInInput = document.getElementById('check-in');
    const checkOutInput = document.getElementById('check-out');

    if (checkInInput) {
        checkInInput.value = formatDate(today);
        checkInInput.min = formatDate(today);
    }

    if (checkOutInput) {
        checkOutInput.value = formatDate(tomorrow);
        checkOutInput.min = formatDate(tomorrow);
    }

    // Update min checkout date when checkin changes
    if (checkInInput && checkOutInput) {
        checkInInput.addEventListener('change', function() {
            const checkInDate = new Date(this.value);
            const nextDay = new Date(checkInDate);
            nextDay.setDate(nextDay.getDate() + 1);
            checkOutInput.min = formatDate(nextDay);

            if (new Date(checkOutInput.value) <= checkInDate) {
                checkOutInput.value = formatDate(nextDay);
            }
        });
    }

    // Tour date
    const tourDateInput = document.getElementById('tour-date');
    if (tourDateInput) {
        tourDateInput.value = formatDate(today);
        tourDateInput.min = formatDate(today);
    }

    // Transportation date
    const travelDateInput = document.getElementById('travel-date');
    if (travelDateInput) {
        travelDateInput.value = formatDate(today);
        travelDateInput.min = formatDate(today);
    }

    console.log('✅ Date defaults set');
}

// Auth Modal Functions
function showAuthModal(type) {
    const modal = document.getElementById('authModal');
    if (!modal) {
        console.error('❌ Auth modal not found');
        return;
    }

    // Simple modal content for now
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeAuthModal()"></div>
        <div class="modal-content">
            <button class="modal-close" onclick="closeAuthModal()">
                <i class="fas fa-times"></i>
            </button>
            <h2>${type === 'signin' ? 'Sign In' : 'Sign Up'}</h2>
            <p>Authentication feature coming soon!</p>
        </div>
    `;

    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    console.log('🔐 Auth modal opened:', type);
}

function closeAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }

    console.log('🔐 Auth modal closed');
}

// Make functions globally available
window.showAuthModal = showAuthModal;
window.closeAuthModal = closeAuthModal;

console.log('✅ Homepage script loaded successfully!');