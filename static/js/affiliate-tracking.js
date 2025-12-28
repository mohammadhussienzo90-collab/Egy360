/**
 * Egy360 Affiliate Click Tracking
 * ================================
 *
 * This script tracks clicks on affiliate links for revenue analytics.
 * It is essential for measuring the effectiveness of social media campaigns
 * and understanding which traffic sources generate the most bookings.
 *
 * Key Features:
 * - Automatic detection of affiliate partner links (Booking.com, Viator, etc.)
 * - UTM parameter tracking for social media campaign attribution
 * - Google Analytics 4 event integration
 * - Non-blocking async requests (doesn't slow down user navigation)
 * - CSRF-protected API calls
 *
 * Usage:
 * - Links are automatically tracked if they match affiliate domain patterns
 * - Add data-affiliate="true" to any link for manual tracking
 * - Add data-item-type and data-item-id for detailed analytics
 *
 * Revenue Model:
 * - Each click is assigned an estimated commission value
 * - Conversion tracking happens on the affiliate partner side
 * - Commission rates: Hotels 2.5-5%, Tours 8%, Activities 15%
 */

(function() {
    'use strict';

    // ==========================================================================
    // UTM PARAMETER TRACKING
    // ==========================================================================
    // UTM parameters help attribute revenue to specific social media campaigns
    // Format: ?utm_source=instagram&utm_medium=social&utm_campaign=egypt_tours
    //
    // This data is crucial for understanding which social media efforts
    // are driving actual bookings and revenue.
    // ==========================================================================

    /**
     * Extract UTM parameters from the current page URL
     * These are stored and sent with each affiliate click for attribution
     *
     * @returns {Object} UTM parameters object
     */
    function getUtmParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            utm_source: params.get('utm_source') || '',      // e.g., 'instagram', 'facebook', 'tiktok'
            utm_medium: params.get('utm_medium') || '',      // e.g., 'social', 'email', 'cpc'
            utm_campaign: params.get('utm_campaign') || '',  // e.g., 'egypt_tours_jan2025'
            utm_content: params.get('utm_content') || '',    // e.g., 'pyramids_reel', 'hotel_story'
            utm_term: params.get('utm_term') || ''           // Search terms (for paid ads)
        };
    }

    /**
     * Get CSRF token from cookie for secure API calls
     * Django requires CSRF token for POST requests
     *
     * @returns {string|null} CSRF token value
     */
    function getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Platform detection from URL
    function detectPlatform(url) {
        const platformPatterns = {
            'booking_com': /booking\.com/i,
            'hotellook': /hotellook\.com|search\.hotellook/i,
            'agoda': /agoda\.com/i,
            'hotels_com': /hotels\.com/i,
            'viator': /viator\.com|tp\.media.*viator/i,
            'getyourguide': /getyourguide\.com/i,
            'travelpayouts': /tp\.media|travelpayouts/i,
            'aviasales': /aviasales/i,
            'discovercars': /discovercars/i,
            'world_nomads': /worldnomads/i,
        };

        for (const [platform, pattern] of Object.entries(platformPatterns)) {
            if (pattern.test(url)) {
                return platform;
            }
        }
        return 'other';
    }

    // ==========================================================================
    // CLICK TRACKING
    // ==========================================================================
    // This is the core function that captures affiliate link clicks.
    // Each click represents potential revenue and is tracked for analytics.
    // ==========================================================================

    /**
     * Track an affiliate link click
     * Sends data to our API and Google Analytics without blocking navigation
     *
     * @param {HTMLElement} element - The clicked link element
     * @param {Event} event - The click event (not prevented, user navigates normally)
     */
    function trackClick(element, event) {
        const url = element.href;
        const itemType = element.dataset.itemType || 'accommodation';
        const itemId = element.dataset.itemId;
        const platform = element.dataset.platform || detectPlatform(url);

        // Get UTM parameters for social media attribution
        // This helps us understand which Instagram post or TikTok video drove the booking
        const utmParams = getUtmParams();

        // Build tracking payload - this is sent to /api/track-click/
        // Don't block the click - send tracking async so user isn't delayed
        const trackingData = {
            url: url,
            item_type: itemType,
            item_id: itemId,
            platform: platform,
            // UTM parameters for campaign attribution
            utm_source: utmParams.utm_source,
            utm_medium: utmParams.utm_medium,
            utm_campaign: utmParams.utm_campaign,
            utm_content: utmParams.utm_content,
            // Additional context
            referrer: document.referrer,
            page_url: window.location.href,
        };

        // Send to tracking endpoint with CSRF protection
        const csrfToken = getCsrfToken();
        const headers = {
            'Content-Type': 'application/json',
        };
        if (csrfToken) {
            headers['X-CSRFToken'] = csrfToken;
        }

        fetch('/api/track-click/', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(trackingData),
            credentials: 'same-origin',  // Include cookies for CSRF
            keepalive: true  // Ensure request completes even if page navigates
        }).catch(function(error) {
            console.log('Click tracking error:', error);
        });

        // Also send to Google Analytics if available
        if (typeof gtag === 'function') {
            gtag('event', 'affiliate_click', {
                'event_category': 'Affiliate',
                'event_label': platform,
                'item_type': itemType,
                'item_id': itemId,
                'value': 1
            });
        }
    }

    // Initialize tracking on page load
    function initTracking() {
        // Track all affiliate links (external links to partner sites)
        document.querySelectorAll('a[href*="booking.com"], a[href*="hotellook"], a[href*="viator"], a[href*="getyourguide"], a[href*="tp.media"], a[href*="agoda"], a.affiliate-link, a.book-now-btn, a.booking-link').forEach(function(link) {
            link.addEventListener('click', function(e) {
                trackClick(this, e);
            });
        });

        // Also track links with data-affiliate attribute
        document.querySelectorAll('[data-affiliate="true"]').forEach(function(link) {
            link.addEventListener('click', function(e) {
                trackClick(this, e);
            });
        });
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTracking);
    } else {
        initTracking();
    }

    // Expose function globally for dynamic content
    window.Egy360 = window.Egy360 || {};
    window.Egy360.trackAffiliateClick = trackClick;
    window.Egy360.initAffiliateTracking = initTracking;

})();
