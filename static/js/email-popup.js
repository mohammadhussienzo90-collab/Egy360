/**
 * Email Capture Popup for Egy360
 * Shows a newsletter signup popup to collect emails
 * Features: delay trigger, exit intent, local storage to prevent repeat shows
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        delayMs: 30000,           // Show after 30 seconds
        cookieExpireDays: 7,      // Don't show again for 7 days after dismissal
        subscribedExpireDays: 365, // Don't show for 1 year after subscribing
        showOnExitIntent: true,    // Show on mouse leave (desktop)
        storageKey: 'egy360_popup',
        apiEndpoint: '/api/newsletter/'
    };

    // State
    let popupShown = false;
    let popupElement = null;

    // Check if popup should be shown
    function shouldShowPopup() {
        const data = localStorage.getItem(CONFIG.storageKey);
        if (!data) return true;

        try {
            const parsed = JSON.parse(data);
            const expireTime = parsed.expires;
            if (expireTime && Date.now() < expireTime) {
                return false;
            }
        } catch (e) {
            return true;
        }
        return true;
    }

    // Save popup state
    function savePopupState(type) {
        const days = type === 'subscribed' ? CONFIG.subscribedExpireDays : CONFIG.cookieExpireDays;
        const expires = Date.now() + (days * 24 * 60 * 60 * 1000);
        localStorage.setItem(CONFIG.storageKey, JSON.stringify({
            type: type,
            expires: expires
        }));
    }

    // Create popup HTML
    function createPopupHTML() {
        const popup = document.createElement('div');
        popup.id = 'email-popup-overlay';
        popup.innerHTML = `
            <div id="email-popup-modal">
                <button id="popup-close" aria-label="Close popup">&times;</button>
                <div class="popup-content">
                    <div class="popup-image">
                        <img src="https://images.unsplash.com/photo-1539768942893-daf53e448371?w=300&h=200&fit=crop" alt="Egypt Pyramids">
                    </div>
                    <div class="popup-form">
                        <h3>Discover Egypt Deals</h3>
                        <p>Get exclusive travel deals, tips, and insider guides delivered to your inbox.</p>
                        <form id="popup-newsletter-form">
                            <input type="email" id="popup-email" placeholder="Enter your email" required>
                            <button type="submit">
                                <span class="btn-text">Get Deals</span>
                                <span class="btn-loading" style="display:none;">
                                    <i class="fas fa-spinner fa-spin"></i>
                                </span>
                            </button>
                        </form>
                        <p class="popup-disclaimer">No spam, unsubscribe anytime. By subscribing, you agree to our <a href="/privacy/">Privacy Policy</a>.</p>
                    </div>
                </div>
            </div>
        `;

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            #email-popup-overlay {
                position: fixed;
                inset: 0;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.3s ease, visibility 0.3s ease;
                padding: 20px;
            }
            #email-popup-overlay.active {
                opacity: 1;
                visibility: visible;
            }
            #email-popup-modal {
                background: white;
                border-radius: 16px;
                overflow: hidden;
                max-width: 500px;
                width: 100%;
                position: relative;
                transform: translateY(20px) scale(0.95);
                transition: transform 0.3s ease;
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            }
            #email-popup-overlay.active #email-popup-modal {
                transform: translateY(0) scale(1);
            }
            #popup-close {
                position: absolute;
                top: 10px;
                right: 15px;
                background: none;
                border: none;
                font-size: 28px;
                color: #666;
                cursor: pointer;
                z-index: 10;
                line-height: 1;
                padding: 5px;
                transition: color 0.2s ease;
            }
            #popup-close:hover {
                color: #c41e3a;
            }
            .popup-content {
                display: flex;
                flex-direction: column;
            }
            .popup-image {
                width: 100%;
                height: 150px;
                overflow: hidden;
            }
            .popup-image img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .popup-form {
                padding: 25px 30px 30px;
                text-align: center;
            }
            .popup-form h3 {
                margin: 0 0 10px;
                font-size: 1.5rem;
                color: #1a1a1a;
            }
            .popup-form > p {
                margin: 0 0 20px;
                color: #666;
                font-size: 0.95rem;
            }
            #popup-newsletter-form {
                display: flex;
                gap: 10px;
            }
            #popup-newsletter-form input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.2s ease;
            }
            #popup-newsletter-form input:focus {
                outline: none;
                border-color: #c41e3a;
            }
            #popup-newsletter-form button {
                background: linear-gradient(135deg, #c41e3a, #9a1830);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                white-space: nowrap;
            }
            #popup-newsletter-form button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(196, 30, 58, 0.3);
            }
            .popup-disclaimer {
                margin: 15px 0 0 !important;
                font-size: 0.75rem !important;
                color: #999 !important;
            }
            .popup-disclaimer a {
                color: #c41e3a;
            }
            .popup-success {
                text-align: center;
                padding: 20px 0;
            }
            .popup-success i {
                font-size: 3rem;
                color: #198754;
                margin-bottom: 15px;
            }
            .popup-success h4 {
                margin: 0 0 10px;
                color: #1a1a1a;
            }
            .popup-success p {
                color: #666;
                margin: 0;
            }

            @media (max-width: 500px) {
                #popup-newsletter-form {
                    flex-direction: column;
                }
                #popup-newsletter-form button {
                    width: 100%;
                }
                .popup-form {
                    padding: 20px;
                }
                .popup-form h3 {
                    font-size: 1.25rem;
                }
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(popup);
        return popup;
    }

    // Show popup
    function showPopup() {
        if (popupShown || !shouldShowPopup()) return;

        popupElement = createPopupHTML();
        popupShown = true;

        // Trigger animation after element is in DOM
        requestAnimationFrame(() => {
            popupElement.classList.add('active');
        });

        // Setup event listeners
        setupEventListeners();

        // Track popup view
        if (typeof gtag === 'function') {
            gtag('event', 'popup_view', {
                'event_category': 'Newsletter',
                'event_label': 'Email Popup Shown'
            });
        }
    }

    // Hide popup
    function hidePopup(reason) {
        if (!popupElement) return;

        popupElement.classList.remove('active');
        setTimeout(() => {
            popupElement.remove();
            popupElement = null;
        }, 300);

        // Save dismissal
        if (reason !== 'subscribed') {
            savePopupState('dismissed');
        }

        // Track popup close
        if (typeof gtag === 'function') {
            gtag('event', 'popup_close', {
                'event_category': 'Newsletter',
                'event_label': reason
            });
        }
    }

    // Setup event listeners
    function setupEventListeners() {
        // Close button
        document.getElementById('popup-close').addEventListener('click', () => {
            hidePopup('close_button');
        });

        // Click outside modal
        popupElement.addEventListener('click', (e) => {
            if (e.target === popupElement) {
                hidePopup('click_outside');
            }
        });

        // Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && popupElement) {
                hidePopup('escape_key');
            }
        });

        // Form submission
        document.getElementById('popup-newsletter-form').addEventListener('submit', handleFormSubmit);
    }

    // Handle form submission
    async function handleFormSubmit(e) {
        e.preventDefault();

        const emailInput = document.getElementById('popup-email');
        const button = e.target.querySelector('button');
        const btnText = button.querySelector('.btn-text');
        const btnLoading = button.querySelector('.btn-loading');

        // Show loading
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        button.disabled = true;

        try {
            const response = await fetch(CONFIG.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: emailInput.value
                })
            });

            const data = await response.json();

            if (data.success) {
                // Show success message
                const formContainer = document.querySelector('.popup-form');
                formContainer.innerHTML = `
                    <div class="popup-success">
                        <i class="fas fa-check-circle"></i>
                        <h4>Welcome aboard!</h4>
                        <p>${data.message || 'Check your inbox for exclusive Egypt deals.'}</p>
                    </div>
                `;

                // Save subscribed state
                savePopupState('subscribed');

                // Track conversion
                if (typeof gtag === 'function') {
                    gtag('event', 'newsletter_signup', {
                        'event_category': 'Newsletter',
                        'event_label': 'Popup Subscription'
                    });
                }

                // Auto close after 3 seconds
                setTimeout(() => {
                    hidePopup('subscribed');
                }, 3000);
            } else {
                alert(data.error || 'Something went wrong. Please try again.');
                btnText.style.display = 'inline';
                btnLoading.style.display = 'none';
                button.disabled = false;
            }
        } catch (error) {
            console.error('Newsletter signup error:', error);
            alert('Network error. Please try again.');
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            button.disabled = false;
        }
    }

    // Exit intent detection (desktop only)
    function setupExitIntent() {
        if (!CONFIG.showOnExitIntent || 'ontouchstart' in window) return;

        let triggered = false;
        document.addEventListener('mouseout', (e) => {
            if (triggered || popupShown) return;

            // Check if mouse left the viewport from the top
            if (e.clientY <= 0) {
                triggered = true;
                showPopup();
            }
        });
    }

    // Initialize
    function init() {
        // Don't show on dashboard, admin, or auth pages
        const path = window.location.pathname;
        if (path.includes('/dashboard') ||
            path.includes('/admin') ||
            path.includes('/accounts/') ||
            path.includes('/api/')) {
            return;
        }

        // Show after delay
        setTimeout(() => {
            if (!popupShown && shouldShowPopup()) {
                showPopup();
            }
        }, CONFIG.delayMs);

        // Setup exit intent
        setupExitIntent();
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
