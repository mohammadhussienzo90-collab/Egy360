/**
 * Egy360 Affiliate Click Tracking
 * Tracks clicks on affiliate links for revenue analytics
 */

(function() {
    'use strict';

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

    // Track affiliate click
    function trackClick(element, event) {
        const url = element.href;
        const itemType = element.dataset.itemType || 'accommodation';
        const itemId = element.dataset.itemId;
        const platform = element.dataset.platform || detectPlatform(url);

        // Don't block the click - send tracking async
        const trackingData = {
            url: url,
            item_type: itemType,
            item_id: itemId,
            platform: platform,
        };

        // Send to tracking endpoint
        fetch('/api/track-click/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(trackingData),
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
