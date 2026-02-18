/**
 * Egy360 Trip Planner - Interactive Wizard & Itinerary Renderer
 * Vanilla JS IIFE - no framework dependencies
 */
var TripPlanner = (function() {
    'use strict';

    // ============================================================
    // STATE
    // ============================================================
    var state = {
        currentStep: 1,
        totalSteps: 3,
        destinations: [],
        duration: 5,
        travelDate: '',
        interests: [],
        budget: 'mid',
        travelers: 2,
        itinerary: null,
    };

    var config = window.TRIP_PLANNER_CONFIG || {};

    // ============================================================
    // INITIALIZATION
    // ============================================================
    function init() {
        bindEvents();
        checkPreset();
    }

    function bindEvents() {
        // City card checkboxes
        document.querySelectorAll('.tp-city-card__input').forEach(function(input) {
            input.addEventListener('change', function() {
                updateDestinations();
            });
        });

        // Duration slider
        var slider = document.getElementById('durationSlider');
        if (slider) {
            slider.addEventListener('input', function() {
                state.duration = parseInt(this.value);
                document.getElementById('durationValue').textContent = state.duration;
            });
        }

        // Travel date
        var dateInput = document.getElementById('travelDate');
        if (dateInput) {
            dateInput.addEventListener('change', function() {
                state.travelDate = this.value;
            });
        }

        // Interest chips
        document.querySelectorAll('input[name="interests"]').forEach(function(input) {
            input.addEventListener('change', function() {
                updateInterests();
            });
        });

        // Budget radio buttons
        document.querySelectorAll('input[name="budget"]').forEach(function(input) {
            input.addEventListener('change', function() {
                state.budget = this.value;
                // Update visual selection
                document.querySelectorAll('.tp-budget-card').forEach(function(card) {
                    card.classList.remove('tp-budget-card--selected');
                });
                this.closest('.tp-budget-card').classList.add('tp-budget-card--selected');
            });
        });
    }

    function checkPreset() {
        var params = new URLSearchParams(window.location.search);
        var preset = params.get('preset');
        if (preset) {
            loadPreset(preset);
        }
    }

    // ============================================================
    // STATE UPDATES
    // ============================================================
    function updateDestinations() {
        state.destinations = [];
        document.querySelectorAll('.tp-city-card__input:checked').forEach(function(input) {
            state.destinations.push(input.value);
        });
    }

    function updateInterests() {
        state.interests = [];
        document.querySelectorAll('input[name="interests"]:checked').forEach(function(input) {
            state.interests.push(input.value);
        });
    }

    // ============================================================
    // WIZARD NAVIGATION
    // ============================================================
    function showStep(step) {
        // Hide all steps
        document.querySelectorAll('.tp-step').forEach(function(el) {
            el.style.display = 'none';
        });

        // Show target step
        var target = document.getElementById('step' + step);
        if (target) {
            target.style.display = 'block';
        }

        // Update progress
        state.currentStep = step;
        var progressFill = document.getElementById('progressFill');
        if (progressFill) {
            progressFill.style.width = (step / state.totalSteps * 100) + '%';
        }

        // Update step indicators
        document.querySelectorAll('.tp-progress__step').forEach(function(el) {
            var stepNum = parseInt(el.getAttribute('data-step'));
            el.classList.remove('active', 'completed');
            if (stepNum === step) {
                el.classList.add('active');
            } else if (stepNum < step) {
                el.classList.add('completed');
            }
        });

        // Scroll to wizard
        var wizard = document.getElementById('wizard');
        if (wizard) {
            wizard.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    function nextStep() {
        // Validate current step
        if (state.currentStep === 1) {
            updateDestinations();
            if (state.destinations.length === 0) {
                alert('Please select at least one destination.');
                return;
            }
        }

        if (state.currentStep < state.totalSteps) {
            showStep(state.currentStep + 1);
        }
    }

    function prevStep() {
        if (state.currentStep > 1) {
            showStep(state.currentStep - 1);
        }
    }

    // ============================================================
    // TRAVELERS CONTROL
    // ============================================================
    function adjustTravelers(delta) {
        state.travelers = Math.max(1, Math.min(20, state.travelers + delta));
        document.getElementById('travelersCount').textContent = state.travelers;
    }

    // ============================================================
    // GENERATE ITINERARY
    // ============================================================
    function generate() {
        updateDestinations();
        updateInterests();

        if (state.destinations.length === 0) {
            alert('Please select at least one destination.');
            showStep(1);
            return;
        }

        if (state.interests.length === 0) {
            state.interests = ['history'];
        }

        // Show loading
        document.querySelectorAll('.tp-step').forEach(function(el) {
            el.style.display = 'none';
        });
        document.getElementById('loadingState').style.display = 'block';

        var payload = {
            destinations: state.destinations,
            duration: state.duration,
            interests: state.interests,
            budget: state.budget,
            travelers: state.travelers,
            travel_dates: state.travelDate || null,
        };

        fetch(config.generateUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': config.csrfToken,
            },
            body: JSON.stringify(payload),
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            document.getElementById('loadingState').style.display = 'none';

            if (data.success) {
                state.itinerary = data;
                renderItinerary(data);
                trackGeneration(data);
            } else {
                alert(data.error || 'Could not generate itinerary. Please try again.');
                showStep(1);
            }
        })
        .catch(function(err) {
            document.getElementById('loadingState').style.display = 'none';
            alert('Network error. Please check your connection and try again.');
            showStep(1);
        });
    }

    // ============================================================
    // RENDER ITINERARY
    // ============================================================
    function renderItinerary(data) {
        // Hide wizard, show results
        document.querySelector('.tp-wizard-section').style.display = 'none';
        var results = document.getElementById('results');
        results.style.display = 'block';

        // Render summary header
        renderSummary(data.summary);

        // Render flight widget
        renderFlightWidget(data);

        // Render day-by-day timeline
        renderTimeline(data);

        // Render cost breakdown
        renderCostBreakdown(data);

        // Show book all CTA
        renderBookAllCta(data);

        // Scroll to results
        results.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function renderSummary(summary) {
        var el = document.getElementById('resultsSummary');
        var html = '<h2 style="margin-bottom:0.5rem;">Your Egypt Itinerary</h2>';
        html += '<div class="tp-results__summary">';
        html += '<div class="tp-results__summary-item"><i class="fas fa-map-marker-alt"></i><span>' + summary.destinations.join(', ') + '</span></div>';
        html += '<div class="tp-results__summary-item"><i class="fas fa-clock"></i><span>' + summary.duration + ' days</span></div>';
        html += '<div class="tp-results__summary-item"><i class="fas fa-users"></i><span>' + summary.travelers + ' travelers</span></div>';
        html += '<div class="tp-results__summary-item"><i class="fas fa-tag"></i><span>' + summary.budget_label + '</span></div>';
        html += '<div class="tp-results__summary-item"><i class="fas fa-dollar-sign"></i><span>~$' + summary.total_estimate.toLocaleString() + ' total</span></div>';
        html += '</div>';
        el.innerHTML = html;
    }

    function renderFlightWidget(data) {
        var container = document.getElementById('flightWidgetContainer');
        if (!data.widget_configs) { return; }

        // Use first destination's flight widget
        var firstCity = data.summary.destination_slugs[0];
        var widgetConfig = data.widget_configs[firstCity];
        if (widgetConfig && widgetConfig.programs && widgetConfig.programs.flights) {
            var script = document.createElement('script');
            script.async = true;
            script.src = widgetConfig.programs.flights.widget_url;
            script.charset = 'utf-8';
            container.innerHTML = '';
            container.appendChild(script);
        }
    }

    function renderTimeline(data) {
        var container = document.getElementById('itineraryTimeline');
        var html = '';
        var prevCity = null;

        data.days.forEach(function(day) {
            // Check for city transition - add transport card
            if (prevCity && day.city !== prevCity) {
                html += renderTransportCard(prevCity, day.city, day.day, data.transport, data.widget_configs);
            }

            // Day card
            html += renderDayCard(day, data);

            // Hotel card for last day in each city
            var nextDay = data.days.find(function(d) { return d.day === day.day + 1; });
            var isLastDayInCity = !nextDay || nextDay.city !== day.city;
            if (isLastDayInCity && day.city) {
                html += renderHotelSection(day.city, data);
            }

            prevCity = day.city;
        });

        container.innerHTML = html;

        // Inject hotel widgets
        injectHotelWidgets(data);
    }

    function renderDayCard(day, data) {
        var cityName = getCityName(day.city);
        var html = '<div class="tp-day-card">';
        html += '<div class="tp-day-card__header">';
        html += '<div><span class="tp-day-card__day">Day ' + day.day + '</span> &mdash; <span class="tp-day-card__title">' + escapeHtml(day.title) + '</span></div>';
        html += '<span class="tp-day-card__city"><i class="fas fa-map-marker-alt me-1"></i>' + escapeHtml(cityName) + '</span>';
        html += '</div>';
        html += '<div class="tp-day-card__body">';

        // Morning
        html += renderActivity('morning', 'fa-sun', day.morning, data);
        // Afternoon
        html += renderActivity('afternoon', 'fa-cloud-sun', day.afternoon, data);
        // Evening
        html += renderActivity('evening', 'fa-moon', day.evening, data);

        html += '</div></div>';
        return html;
    }

    function renderActivity(timeLabel, icon, slot, data) {
        if (!slot) return '';
        var html = '<div class="tp-activity">';
        html += '<div class="tp-activity__time"><i class="fas ' + icon + '"></i> ' + timeLabel + '</div>';
        html += '<div class="tp-activity__content">';
        html += '<div class="tp-activity__name">' + escapeHtml(slot.activity) + '</div>';

        // If there's enriched attraction data
        if (slot.attraction_data) {
            var attr = slot.attraction_data;
            if (attr.description) {
                html += '<p class="tp-activity__desc">' + escapeHtml(attr.description) + '</p>';
            }
            if (attr.is_unesco) {
                html += '<span class="badge bg-warning text-dark" style="font-size:0.7rem;"><i class="fas fa-award me-1"></i>UNESCO</span> ';
            }
        }

        // Tour CTA for activities with attraction slugs
        if (slot.attraction_slug && !slot.is_transport) {
            var citySlug = null;
            // Find the city for this slot from data context
            if (data.widget_configs) {
                var slugs = Object.keys(data.widget_configs);
                if (slugs.length > 0) {
                    citySlug = slugs[0];
                }
            }
            var tourUrl = 'https://tpemd.com/click?shmarker=688198&promo_id=4497&source_type=deeplink&type=click&campaign_id=137&trs=477897';
            html += '<a href="' + tourUrl + '" target="_blank" rel="sponsored noopener" class="tp-activity__tour-cta" data-affiliate="true" data-item-type="tour">';
            html += '<i class="fas fa-ticket-alt me-1"></i>Book Tour for This Activity &rarr;</a>';
        }

        html += '</div></div>';
        return html;
    }

    function renderTransportCard(fromCity, toCity, day, transportData, widgetConfigs) {
        var fromName = getCityName(fromCity);
        var toName = getCityName(toCity);

        // Find matching transport info
        var info = null;
        if (transportData) {
            info = transportData.find(function(t) {
                return t.from_city === fromCity && t.to_city === toCity && t.day === day;
            });
        }

        var html = '<div class="tp-transport-card">';
        html += '<div class="tp-transport-card__title"><i class="fas fa-route me-2"></i>Getting from ' + escapeHtml(fromName) + ' to ' + escapeHtml(toName) + '</div>';

        if (info && info.options) {
            info.options.forEach(function(opt) {
                var modeIcon = {
                    'flight': 'fa-plane',
                    'train': 'fa-train',
                    'bus': 'fa-bus',
                    'car': 'fa-car',
                    'nile_cruise': 'fa-ship',
                }[opt.mode] || 'fa-arrow-right';

                html += '<div class="tp-transport-card__option">';
                html += '<span><i class="fas ' + modeIcon + ' me-2"></i>' + escapeHtml(opt.mode.replace('_', ' ').replace(/\b\w/g, function(c) { return c.toUpperCase(); })) + ' &mdash; ' + escapeHtml(opt.duration) + '</span>';
                html += '<span class="fw-semibold">~$' + opt.price_usd + '</span>';
                html += '</div>';
                if (opt.notes) {
                    html += '<small class="text-muted d-block" style="padding-left:1.75rem;margin-top:-0.25rem;">' + escapeHtml(opt.notes) + '</small>';
                }
            });
        }

        // Car rental CTA
        var carConfig = widgetConfigs && widgetConfigs[toCity] && widgetConfigs[toCity].programs && widgetConfigs[toCity].programs.car_rental;
        if (carConfig) {
            html += '<div class="mt-2"><a href="https://tp.media/click?shmarker=688198&promo_id=4506&source_type=deeplink&type=click&campaign_id=102&trs=477897" target="_blank" rel="sponsored noopener" class="btn btn-outline-primary btn-sm" data-affiliate="true" data-item-type="car_rental"><i class="fas fa-car me-1"></i>Rent a Car</a></div>';
        }

        html += '</div>';
        return html;
    }

    function renderHotelSection(citySlug, data) {
        var cityName = getCityName(citySlug);
        var hotelData = data.hotels && data.hotels[citySlug];

        var html = '<div class="tp-hotel-card">';
        html += '<div class="tp-hotel-card__header">';
        html += '<div><i class="fas fa-hotel me-2 text-primary"></i><span class="tp-hotel-card__name">Where to Stay in ' + escapeHtml(cityName) + '</span></div>';
        if (hotelData) {
            html += '<span class="tp-hotel-card__price">from $' + hotelData.price + '/night</span>';
        }
        html += '</div>';

        if (hotelData) {
            html += '<p style="margin:0.5rem 0;font-size:0.9rem;">' + escapeHtml(hotelData.name);
            html += ' <span class="tp-hotel-card__stars">';
            for (var i = 0; i < hotelData.stars; i++) {
                html += '<i class="fas fa-star"></i>';
            }
            html += '</span></p>';
        }

        // Hotel widget placeholder
        html += '<div class="tp-day-hotel-widget" id="hotel-widget-' + citySlug + '"></div>';

        // Book hotel CTA
        html += '<a href="https://tp.media/click?shmarker=688198&promo_id=4505&source_type=deeplink&type=click&campaign_id=101&trs=477897" target="_blank" rel="sponsored noopener" class="btn btn-primary btn-sm mt-2" data-affiliate="true" data-item-type="hotel">';
        html += '<i class="fas fa-search me-1"></i>Compare ' + escapeHtml(cityName) + ' Hotels</a>';

        html += '</div>';
        return html;
    }

    function injectHotelWidgets(data) {
        if (!data.widget_configs) return;

        Object.keys(data.widget_configs).forEach(function(citySlug) {
            var container = document.getElementById('hotel-widget-' + citySlug);
            if (!container) return;

            var wc = data.widget_configs[citySlug];
            if (wc && wc.programs && wc.programs.hotels) {
                var script = document.createElement('script');
                script.async = true;
                script.src = wc.programs.hotels.widget_url;
                script.charset = 'utf-8';
                container.appendChild(script);
            }
        });
    }

    function renderCostBreakdown(data) {
        var container = document.getElementById('costBreakdown');
        var content = document.getElementById('costBreakdownContent');
        if (!data.summary) return;

        var s = data.summary;
        var html = '';
        html += '<div class="tp-cost-line"><span>' + s.budget_label + ' budget</span><span>~$' + s.daily_estimate + '/day</span></div>';
        html += '<div class="tp-cost-line"><span>Duration</span><span>' + s.duration + ' days</span></div>';
        html += '<div class="tp-cost-line"><span>Travelers</span><span>' + s.travelers + '</span></div>';
        html += '<div class="tp-cost-line tp-cost-line--total"><span>Estimated Total</span><span>~$' + s.total_estimate.toLocaleString() + '</span></div>';
        html += '<small class="text-muted d-block mt-2">Excludes international flights. Actual costs vary by season.</small>';

        content.innerHTML = html;
        container.style.display = 'block';
    }

    function renderBookAllCta(data) {
        var cta = document.getElementById('bookAllCta');
        cta.style.display = 'block';

        var firstCity = data.summary.destination_slugs[0];
        var wc = data.widget_configs && data.widget_configs[firstCity];

        if (wc) {
            document.getElementById('bookFlightsBtn').href = 'https://tp.media/click?shmarker=688198&promo_id=4504&source_type=deeplink&type=click&campaign_id=100&trs=477897';
            document.getElementById('bookHotelsBtn').href = 'https://tp.media/click?shmarker=688198&promo_id=4505&source_type=deeplink&type=click&campaign_id=101&trs=477897';
            document.getElementById('bookToursBtn').href = 'https://tpemd.com/click?shmarker=688198&promo_id=4497&source_type=deeplink&type=click&campaign_id=137&trs=477897';
        }
    }

    // ============================================================
    // PRESET SUPPORT
    // ============================================================
    function loadPreset(slug) {
        // Set destinations and duration from preset data
        var presetData = null;
        if (config.presets) {
            presetData = config.presets.find(function(p) { return p.slug === slug; });
        }

        if (!presetData) {
            // Fallback: just generate with slug-based defaults
            var presetDefaults = {
                'classic-egypt': { destinations: ['cairo', 'luxor', 'aswan'], duration: 7 },
                'cairo-weekend': { destinations: ['cairo'], duration: 3 },
                'nile-valley': { destinations: ['luxor', 'aswan'], duration: 5 },
                'red-sea-relaxation': { destinations: ['cairo', 'hurghada'], duration: 5 },
                'egypt-express': { destinations: ['cairo', 'luxor'], duration: 4 },
                'complete-egypt': { destinations: ['cairo', 'luxor', 'aswan', 'hurghada'], duration: 10 },
            };
            presetData = presetDefaults[slug];
        }

        if (!presetData) return;

        // Map destination names to slugs if needed
        var destSlugs = (presetData.destinations || []).map(function(d) {
            return d.toLowerCase().replace(/ /g, '-');
        });

        state.destinations = destSlugs;
        state.duration = presetData.duration || 5;
        state.interests = ['history'];
        state.budget = 'mid';
        state.travelers = 2;

        // Scroll to wizard and generate
        var wizard = document.getElementById('wizard');
        if (wizard) {
            wizard.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        // Short delay then generate
        setTimeout(function() {
            generate();
        }, 300);
    }

    // ============================================================
    // RESET
    // ============================================================
    function reset() {
        // Reset state
        state.currentStep = 1;
        state.destinations = [];
        state.duration = 5;
        state.travelDate = '';
        state.interests = [];
        state.budget = 'mid';
        state.travelers = 2;
        state.itinerary = null;

        // Reset UI
        document.querySelectorAll('.tp-city-card__input').forEach(function(i) { i.checked = false; });
        document.querySelectorAll('input[name="interests"]').forEach(function(i) { i.checked = false; });
        document.getElementById('durationSlider').value = 5;
        document.getElementById('durationValue').textContent = '5';
        document.getElementById('travelersCount').textContent = '2';

        var midBudget = document.querySelector('input[name="budget"][value="mid"]');
        if (midBudget) midBudget.checked = true;

        // Show wizard, hide results
        document.querySelector('.tp-wizard-section').style.display = '';
        document.getElementById('results').style.display = 'none';
        document.getElementById('loadingState').style.display = 'none';

        showStep(1);

        // Clear URL params
        if (window.history.replaceState) {
            window.history.replaceState({}, '', window.location.pathname);
        }
    }

    // ============================================================
    // GA4 TRACKING
    // ============================================================
    function trackGeneration(data) {
        if (typeof gtag === 'function') {
            gtag('event', 'itinerary_generated', {
                event_category: 'Trip Planner',
                destinations: data.summary.destinations.join(', '),
                duration: data.summary.duration,
                budget: data.summary.budget_level,
                travelers: data.summary.travelers,
                total_estimate: data.summary.total_estimate,
            });
        }
    }

    // ============================================================
    // UTILITIES
    // ============================================================
    var cityNames = {
        'cairo': 'Cairo',
        'luxor': 'Luxor',
        'aswan': 'Aswan',
        'hurghada': 'Hurghada',
        'sharm-el-sheikh': 'Sharm El Sheikh',
        'alexandria': 'Alexandria',
    };

    function getCityName(slug) {
        return cityNames[slug] || slug.replace(/-/g, ' ').replace(/\b\w/g, function(c) { return c.toUpperCase(); });
    }

    function escapeHtml(str) {
        if (!str) return '';
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    // ============================================================
    // PUBLIC API
    // ============================================================
    document.addEventListener('DOMContentLoaded', init);

    return {
        nextStep: nextStep,
        prevStep: prevStep,
        showStep: showStep,
        generate: generate,
        loadPreset: loadPreset,
        adjustTravelers: adjustTravelers,
        reset: reset,
    };
})();
