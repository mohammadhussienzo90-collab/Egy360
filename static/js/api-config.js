/* =========================================
   EGY360 - API Configuration
   Django REST Framework Integration
   ========================================= */

const API_CONFIG = {
    // Determine base URL based on environment
    API_BASE: (function() {
        const hostname = window.location.hostname;

        // Development environments
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:8000/api';
        }

        // Production - Railway or custom domain
        return '/api';
    })(),

    // Get headers with CSRF token for Django
    getHeaders: function() {
        const headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };

        // Add CSRF token for unsafe methods
        const csrfToken = this.getCsrfToken();
        if (csrfToken) {
            headers['X-CSRFToken'] = csrfToken;
        }

        return headers;
    },

    // Extract CSRF token from Django cookie
    getCsrfToken: function() {
        let cookieValue = null;

        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');

            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();

                // Check if this cookie is the CSRF token
                if (cookie.substring(0, 10) === 'csrftoken=') {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }

        return cookieValue;
    },

    // Check if user is authenticated
    isAuthenticated: function() {
        // Check for session cookie or auth token
        return document.cookie.includes('sessionid') ||
               localStorage.getItem('authToken') !== null;
    },

    // Get auth token if stored
    getAuthToken: function() {
        return localStorage.getItem('authToken');
    },

    // Store auth token
    setAuthToken: function(token) {
        localStorage.setItem('authToken', token);
    },

    // Clear auth token
    clearAuthToken: function() {
        localStorage.removeItem('authToken');
    }
};

// Make globally available
window.API_CONFIG = API_CONFIG;

// Log configuration on load
console.log('✅ API Configuration loaded');
console.log('📡 Base URL:', API_CONFIG.API_BASE);
console.log('🔐 CSRF Token:', API_CONFIG.getCsrfToken() ? 'Present' : 'Not found');
console.log('👤 Authenticated:', API_CONFIG.isAuthenticated());