/* =========================================
   EGY360 - Tour Listing Page Script
   Dynamic filtering, sorting, and API integration for tours
   ========================================= */

// State Management
let searchState = {
    page: 1,
    perPage: 20,
    sortBy: 'recommended',
    filters: {
        city: '',
        date: '',
        category: '',
        travelers: 2,
        minPrice: 0,
        maxPrice: 5000,
        categories: [],
        durations: [],
        difficulties: [],
        languages: [],
        groups: [],
        included: [],
        minRating: 0
    },
    viewMode: 'grid',
    allTours: [] // Store all results for client-side filtering
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎭 Initializing tour listing page...');
    initializeSearch();
    setupEventListeners();
    loadTours();
});

// Initialize search from URL parameters
function initializeSearch() {
    const urlParams = new URLSearchParams(window.location.search);

    // Get search parameters from URL
    searchState.filters.city = urlParams.get('city') || '';
    searchState.filters.date = urlParams.get('date') || '';
    searchState.filters.category = urlParams.get('category') || '';
    searchState.filters.travelers = parseInt(urlParams.get('travelers')) || 2;

    // Update form fields
    const cityInput = document.getElementById('cityInput');
    const dateInput = document.getElementById('dateInput');
    const categoryInput = document.getElementById('categoryInput');
    const travelersInput = document.getElementById('travelersInput');

    if (cityInput && searchState.filters.city) {
        cityInput.value = searchState.filters.city;
    }
    if (dateInput && searchState.filters.date) {
        dateInput.value = searchState.filters.date;
    }
    if (categoryInput && searchState.filters.category) {
        categoryInput.value = searchState.filters.category;
    }
    if (travelersInput) {
        travelersInput.value = searchState.filters.travelers;
    }

    console.log('✅ Search initialized with filters:', searchState.filters);
}

// Setup Event Listeners
function setupEventListeners() {
    console.log('🔧 Setting up event listeners...');

    // Search form
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', handleSearchSubmit);
    }

    // Sort dropdown
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', handleSortChange);
    }

    // View toggle
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', handleViewToggle);
    });

    // Price sliders
    const minPriceSlider = document.getElementById('minPrice');
    const maxPriceSlider = document.getElementById('maxPrice');

    if (minPriceSlider) {
        minPriceSlider.addEventListener('input', updatePriceDisplay);
        minPriceSlider.addEventListener('change', applyFilters);
    }

    if (maxPriceSlider) {
        maxPriceSlider.addEventListener('input', updatePriceDisplay);
        maxPriceSlider.addEventListener('change', applyFilters);
    }

    // Filter checkboxes
    document.querySelectorAll('.filter-checkbox input').forEach(checkbox => {
        checkbox.addEventListener('change', applyFilters);
    });

    // Rating radio buttons
    document.querySelectorAll('input[name="rating"]').forEach(radio => {
        radio.addEventListener('change', applyFilters);
    });

    // Reset filters
    const resetBtn = document.getElementById('resetFilters');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetAllFilters);
    }

    // Mobile filter toggle
    const filterToggle = document.getElementById('filterToggle');
    const filtersSidebar = document.getElementById('filtersSidebar');
    const applyFiltersBtn = document.getElementById('applyFilters');

    if (filterToggle && filtersSidebar) {
        filterToggle.addEventListener('click', () => {
            filtersSidebar.classList.toggle('active');
        });
    }

    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', () => {
            if (filtersSidebar) {
                filtersSidebar.classList.remove('active');
            }
            applyFilters();
        });
    }

    console.log('✅ All event listeners set up!');
}

// Handle Search Form Submission
function handleSearchSubmit(e) {
    e.preventDefault();

    const cityInput = document.getElementById('cityInput');
    const dateInput = document.getElementById('dateInput');
    const categoryInput = document.getElementById('categoryInput');
    const travelersInput = document.getElementById('travelersInput');

    searchState.filters.city = cityInput ? cityInput.value : '';
    searchState.filters.date = dateInput ? dateInput.value : '';
    searchState.filters.category = categoryInput ? categoryInput.value : '';
    searchState.filters.travelers = travelersInput ? parseInt(travelersInput.value) : 2;
    searchState.page = 1;

    console.log('🔍 New search submitted:', searchState.filters);
    loadTours();
}

// Handle Sort Change
function handleSortChange(e) {
    searchState.sortBy = e.target.value;
    searchState.page = 1;
    console.log('🔄 Sort changed to:', searchState.sortBy);
    applyFilters();
}

// Handle View Toggle
function handleViewToggle(e) {
    const viewMode = e.currentTarget.dataset.view;

    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    e.currentTarget.classList.add('active');

    const resultsGrid = document.getElementById('resultsGrid');

    if (viewMode === 'list') {
        resultsGrid.classList.add('list-view');
        searchState.viewMode = 'list';
    } else {
        resultsGrid.classList.remove('list-view');
        searchState.viewMode = 'grid';
    }

    console.log('👁️ View changed to:', viewMode);
}

// Update Price Display
function updatePriceDisplay() {
    const minPrice = parseInt(document.getElementById('minPrice').value);
    const maxPrice = parseInt(document.getElementById('maxPrice').value);

    document.getElementById('minPriceDisplay').textContent = `${minPrice.toLocaleString()} EGP`;
    document.getElementById('maxPriceDisplay').textContent = `${maxPrice.toLocaleString()} EGP`;

    searchState.filters.minPrice = minPrice;
    searchState.filters.maxPrice = maxPrice;
}

// Apply Filters
function applyFilters() {
    console.log('🎯 Applying filters...');

    // Get checked categories
    searchState.filters.categories = Array.from(
        document.querySelectorAll('input[name="category"]:checked')
    ).map(cb => cb.value);

    // Get checked durations
    searchState.filters.durations = Array.from(
        document.querySelectorAll('input[name="duration"]:checked')
    ).map(cb => cb.value);

    // Get checked difficulties
    searchState.filters.difficulties = Array.from(
        document.querySelectorAll('input[name="difficulty"]:checked')
    ).map(cb => cb.value);

    // Get checked languages
    searchState.filters.languages = Array.from(
        document.querySelectorAll('input[name="language"]:checked')
    ).map(cb => cb.value);

    // Get checked groups
    searchState.filters.groups = Array.from(
        document.querySelectorAll('input[name="group"]:checked')
    ).map(cb => cb.value);

    // Get checked included
    searchState.filters.included = Array.from(
        document.querySelectorAll('input[name="included"]:checked')
    ).map(cb => cb.value);

    // Get minimum rating
    const ratingChecked = document.querySelector('input[name="rating"]:checked');
    searchState.filters.minRating = ratingChecked ? parseInt(ratingChecked.value) : 0;

    // Get price range
    searchState.filters.minPrice = parseInt(document.getElementById('minPrice').value);
    searchState.filters.maxPrice = parseInt(document.getElementById('maxPrice').value);

    console.log('📊 Filters:', searchState.filters);

    // Filter the tours
    let filtered = [...searchState.allTours];
    console.log('📦 Starting with', filtered.length, 'tours');

    // Apply price filter
    filtered = filtered.filter(tour => {
        const price = tour.price || 0;
        return price >= searchState.filters.minPrice && price <= searchState.filters.maxPrice;
    });
    console.log('💰 After price filter:', filtered.length);

    // Apply category filter
    if (searchState.filters.categories.length > 0) {
        filtered = filtered.filter(tour => {
            return searchState.filters.categories.includes(tour.category);
        });
        console.log('🎭 After category filter:', filtered.length);
    }

    // Apply duration filter
    if (searchState.filters.durations.length > 0) {
        filtered = filtered.filter(tour => {
            return searchState.filters.durations.includes(tour.duration);
        });
        console.log('⏱️ After duration filter:', filtered.length);
    }

    // Apply difficulty filter
    if (searchState.filters.difficulties.length > 0) {
        filtered = filtered.filter(tour => {
            return searchState.filters.difficulties.includes(tour.difficulty);
        });
        console.log('💪 After difficulty filter:', filtered.length);
    }

    // Apply language filter
    if (searchState.filters.languages.length > 0) {
        filtered = filtered.filter(tour => {
            return searchState.filters.languages.some(lang => tour.languages.includes(lang));
        });
        console.log('🗣️ After language filter:', filtered.length);
    }

    // Apply group filter
    if (searchState.filters.groups.length > 0) {
        filtered = filtered.filter(tour => {
            return searchState.filters.groups.includes(tour.group_type);
        });
        console.log('👥 After group filter:', filtered.length);
    }

    // Apply rating filter
    if (searchState.filters.minRating > 0) {
        filtered = filtered.filter(tour => {
            return (tour.rating || 0) >= searchState.filters.minRating;
        });
        console.log('⭐ After rating filter:', filtered.length);
    }

    // Apply sorting
    filtered = sortTours(filtered);

    console.log('✅ Final filtered count:', filtered.length);

    // Display results
    displayTours(filtered);
    updateResultsCount(filtered.length);

    // Show empty state if no results
    const emptyState = document.getElementById('emptyState');
    const resultsGrid = document.getElementById('resultsGrid');

    if (filtered.length === 0) {
        emptyState.style.display = 'flex';
        resultsGrid.style.display = 'none';
    } else {
        emptyState.style.display = 'none';
        resultsGrid.style.display = 'grid';
    }
}

// Sort Tours
function sortTours(tours) {
    const sorted = [...tours];

    switch (searchState.sortBy) {
        case 'price_low':
            sorted.sort((a, b) => (a.price || 0) - (b.price || 0));
            break;
        case 'price_high':
            sorted.sort((a, b) => (b.price || 0) - (a.price || 0));
            break;
        case 'rating':
            sorted.sort((a, b) => (b.rating || 0) - (a.rating || 0));
            break;
        case 'duration_short':
            sorted.sort((a, b) => (a.duration_hours || 0) - (b.duration_hours || 0));
            break;
        case 'duration_long':
            sorted.sort((a, b) => (b.duration_hours || 0) - (a.duration_hours || 0));
            break;
        default: // recommended
            break;
    }

    console.log('🔄 Sorted by:', searchState.sortBy);
    return sorted;
}

// Reset All Filters
function resetAllFilters() {
    console.log('🔄 Resetting all filters...');

    // Reset sliders
    document.getElementById('minPrice').value = 0;
    document.getElementById('maxPrice').value = 5000;
    updatePriceDisplay();

    // Uncheck all checkboxes and radios
    document.querySelectorAll('.filter-checkbox input, input[name="rating"]').forEach(input => {
        input.checked = false;
    });

    // Reset state
    searchState.filters = {
        ...searchState.filters,
        minPrice: 0,
        maxPrice: 5000,
        categories: [],
        durations: [],
        difficulties: [],
        languages: [],
        groups: [],
        included: [],
        minRating: 0
    };

    applyFilters();
}

// Load Tours
async function loadTours() {
    const loadingState = document.getElementById('loadingState');
    const resultsGrid = document.getElementById('resultsGrid');
    const emptyState = document.getElementById('emptyState');

    loadingState.style.display = 'flex';
    resultsGrid.style.display = 'none';
    emptyState.style.display = 'none';

    console.log('📡 Loading tours...');

    // For now, load mock data
    setTimeout(() => {
        loadMockData();
    }, 500);
}

// Load Mock Data
function loadMockData() {
    console.log('📦 Loading mock tour data...');

    const mockTours = [
        {
            id: 1,
            name: "Pyramids of Giza & Sphinx Tour",
            city: "Giza",
            category: "historical",
            duration: "half-day",
            duration_hours: 4,
            difficulty: "easy",
            languages: ["english", "arabic", "french"],
            group_type: "small",
            price: 800,
            rating: 9.5,
            reviews_count: 1250,
            description: "Visit the iconic Pyramids of Giza and the Great Sphinx on this half-day tour.",
            includes_meals: false,
            includes_transport: true,
            includes_guide: true,
            includes_tickets: true,
            image: "https://source.unsplash.com/400x300/?pyramids,giza,egypt"
        },
        {
            id: 2,
            name: "Nile River Dinner Cruise",
            city: "Cairo",
            category: "cultural",
            duration: "full-day",
            duration_hours: 8,
            difficulty: "easy",
            languages: ["english", "arabic"],
            group_type: "large",
            price: 1200,
            rating: 8.8,
            reviews_count: 890,
            description: "Enjoy an evening cruise on the Nile with dinner and live entertainment.",
            includes_meals: true,
            includes_transport: true,
            includes_guide: true,
            includes_tickets: false,
            image: "https://source.unsplash.com/400x300/?nile,cruise,egypt"
        },
        {
            id: 3,
            name: "Egyptian Museum & Old Cairo",
            city: "Cairo",
            category: "historical",
            duration: "full-day",
            duration_hours: 6,
            difficulty: "easy",
            languages: ["english", "french", "german"],
            group_type: "small",
            price: 950,
            rating: 9.2,
            reviews_count: 670,
            description: "Explore ancient Egyptian artifacts and Coptic Cairo's historical sites.",
            includes_meals: false,
            includes_transport: true,
            includes_guide: true,
            includes_tickets: true,
            image: "https://source.unsplash.com/400x300/?egyptian,museum,cairo"
        },
        {
            id: 4,
            name: "Luxor Valley of the Kings",
            city: "Luxor",
            category: "historical",
            duration: "full-day",
            duration_hours: 10,
            difficulty: "moderate",
            languages: ["english", "spanish"],
            group_type: "small",
            price: 1800,
            rating: 9.7,
            reviews_count: 1420,
            description: "Discover the tombs of ancient pharaohs in the Valley of the Kings.",
            includes_meals: true,
            includes_transport: true,
            includes_guide: true,
            includes_tickets: true,
            image: "https://source.unsplash.com/400x300/?luxor,valley,kings"
        },
        {
            id: 5,
            name: "White Desert Safari Adventure",
            city: "Farafra",
            category: "adventure",
            duration: "multi-day",
            duration_hours: 48,
            difficulty: "challenging",
            languages: ["english", "arabic"],
            group_type: "private",
            price: 3500,
            rating: 9.4,
            reviews_count: 380,
            description: "2-day camping adventure in Egypt's stunning White Desert.",
            includes_meals: true,
            includes_transport: true,
            includes_guide: true,
            includes_tickets: false,
            image: "https://source.unsplash.com/400x300/?desert,white,egypt"
        },
        {
            id: 6,
            name: "Red Sea Snorkeling Adventure",
            city: "Hurghada",
            category: "adventure",
            duration: "full-day",
            duration_hours: 7,
            difficulty: "moderate",
            languages: ["english", "german"],
            group_type: "small",
            price: 1100,
            rating: 8.9,
            reviews_count: 540,
            description: "Explore vibrant coral reefs and marine life in the Red Sea.",
            includes_meals: true,
            includes_transport: true,
            includes_guide: true,
            includes_tickets: false,
            image: "https://source.unsplash.com/400x300/?redsea,snorkeling,coral"
        },
        {
            id: 7,
            name: "Cairo Street Food Tour",
            city: "Cairo",
            category: "food",
            duration: "half-day",
            duration_hours: 4,
            difficulty: "easy",
            languages: ["english", "arabic"],
            group_type: "small",
            price: 650,
            rating: 9.1,
            reviews_count: 720,
            description: "Taste authentic Egyptian cuisine on this guided food tour.",
            includes_meals: true,
            includes_transport: false,
            includes_guide: true,
            includes_tickets: false,
            image: "https://source.unsplash.com/400x300/?egyptian,food,street"
        },
        {
            id: 8,
            name: "Alexandria Day Trip",
            city: "Alexandria",
            category: "cultural",
            duration: "full-day",
            duration_hours: 12,
            difficulty: "easy",
            languages: ["english", "french"],
            group_type: "large",
            price: 1400,
            rating: 8.6,
            reviews_count: 450,
            description: "Visit the historic city of Alexandria and its Mediterranean coast.",
            includes_meals: true,
            includes_transport: true,
            includes_guide: true,
            includes_tickets: true,
            image: "https://source.unsplash.com/400x300/?alexandria,mediterranean,egypt"
        },
        {
            id: 9,
            name: "Islamic Cairo Walking Tour",
            city: "Cairo",
            category: "religious",
            duration: "half-day",
            duration_hours: 5,
            difficulty: "easy",
            languages: ["english", "arabic"],
            group_type: "small",
            price: 700,
            rating: 9.0,
            reviews_count: 310,
            description: "Explore historic mosques and Islamic architecture in old Cairo.",
            includes_meals: false,
            includes_transport: false,
            includes_guide: true,
            includes_tickets: true,
            image: "https://source.unsplash.com/400x300/?mosque,islamic,cairo"
        },
        {
            id: 10,
            name: "Aswan & Abu Simbel Temples",
            city: "Aswan",
            category: "historical",
            duration: "full-day",
            duration_hours: 14,
            difficulty: "moderate",
            languages: ["english", "spanish"],
            group_type: "small",
            price: 2200,
            rating: 9.6,
            reviews_count: 890,
            description: "Visit the magnificent temples of Abu Simbel and Philae.",
            includes_meals: true,
            includes_transport: true,
            includes_guide: true,
            includes_tickets: true,
            image: "https://source.unsplash.com/400x300/?abu,simbel,temple"
        }
    ];

    searchState.allTours = mockTours;

    console.log('✅ Loaded', mockTours.length, 'mock tours');

    document.getElementById('loadingState').style.display = 'none';

    applyFilters();
}

// Display Tours
function displayTours(tours) {
    const resultsGrid = document.getElementById('resultsGrid');
    resultsGrid.innerHTML = '';

    console.log('🎨 Displaying', tours.length, 'tours');

    tours.forEach(tour => {
        const card = createTourCard(tour);
        resultsGrid.appendChild(card);
    });
}

// Create Tour Card
function createTourCard(tour) {
    const card = document.createElement('div');
    card.className = 'accommodation-card';
    card.onclick = () => {
        console.log('🔗 Navigating to tour:', tour.id);
        window.location.href = `/tours/${tour.id}/`;
    };

    // Duration label
    const durationLabel = tour.duration === 'half-day' ? '4 hours' :
                         tour.duration === 'full-day' ? '8+ hours' :
                         '2+ days';

    // Difficulty badge color
    const difficultyColor = tour.difficulty === 'easy' ? '#10B981' :
                           tour.difficulty === 'moderate' ? '#F59E0B' :
                           '#EF4444';

    card.innerHTML = `
        <div class="card-image">
            <img src="${tour.image}" alt="${tour.name}" loading="lazy">
            <button class="btn-favorite" onclick="event.stopPropagation(); toggleFavorite(${tour.id})">
                <i class="far fa-heart"></i>
            </button>
            <div class="card-badge" style="background: ${difficultyColor}">
                <i class="fas fa-hiking"></i> ${tour.difficulty.charAt(0).toUpperCase() + tour.difficulty.slice(1)}
            </div>
        </div>
        
        <div class="card-content">
            <div class="card-header">
                <div>
                    <h3 class="card-title">${tour.name}</h3>
                    <p class="card-location">
                        <i class="fas fa-map-marker-alt"></i>
                        ${tour.city}, Egypt
                    </p>
                </div>
                <div class="card-rating">
                    <span class="rating-score">${tour.rating.toFixed(1)}</span>
                    <div class="rating-stars">★★★★★</div>
                    <span class="rating-count">(${tour.reviews_count} reviews)</span>
                </div>
            </div>
            
            <div class="card-features">
                <span><i class="fas fa-clock"></i> ${durationLabel}</span>
                ${tour.includes_guide ? '<span><i class="fas fa-user-tie"></i> Guide</span>' : ''}
                ${tour.includes_meals ? '<span><i class="fas fa-utensils"></i> Meals</span>' : ''}
                ${tour.includes_transport ? '<span><i class="fas fa-bus"></i> Transport</span>' : ''}
            </div>
            
            <div class="card-footer">
                <div class="card-price">
                    <span class="price-label">From</span>
                    <span class="price-amount">${tour.price.toLocaleString()} EGP</span>
                    <span class="price-period">/person</span>
                </div>
                <button class="btn-book" onclick="event.stopPropagation(); bookNow(${tour.id})">
                    Book Now
                </button>
            </div>
        </div>
    `;

    return card;
}

// Update Results Count
function updateResultsCount(count) {
    document.getElementById('totalResults').textContent = count.toLocaleString();
}

// Toggle Favorite
function toggleFavorite(id) {
    console.log('❤️ Toggle favorite:', id);
    alert('Favorite feature coming soon!');
}

// Book Now
function bookNow(id) {
    console.log('📅 Book now:', id);
    window.location.href = `/tours/${id}/?book=true`;
}

// Auth modal functions
function showAuthModal(type) {
    const modal = document.getElementById('authModal');
    const content = document.getElementById('authModalContent');

    if (type === 'signin') {
        content.innerHTML = `
            <h2 style="margin-bottom: 24px; font-size: 24px;">Sign In to Egy360</h2>
            <form style="display: flex; flex-direction: column; gap: 16px;">
                <input type="email" placeholder="Email Address" required 
                       style="padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                <input type="password" placeholder="Password" required
                       style="padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                <button type="submit" class="btn-primary" style="padding: 14px; font-size: 16px; margin-top: 8px;">
                    Sign In
                </button>
            </form>
        `;
    } else {
        content.innerHTML = `
            <h2 style="margin-bottom: 24px; font-size: 24px;">Create Your Account</h2>
            <form style="display: flex; flex-direction: column; gap: 16px;">
                <input type="text" placeholder="Full Name" required
                       style="padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                <input type="email" placeholder="Email Address" required
                       style="padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                <input type="password" placeholder="Password" required
                       style="padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                <button type="submit" class="btn-primary" style="padding: 14px; font-size: 16px; margin-top: 8px;">
                    Create Account
                </button>
            </form>
        `;
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeAuthModal() {
    document.getElementById('authModal').classList.remove('active');
    document.body.style.overflow = '';
}

// Make functions global
window.toggleFavorite = toggleFavorite;
window.bookNow = bookNow;
window.showAuthModal = showAuthModal;
window.closeAuthModal = closeAuthModal;

console.log('✅ Tour listing script loaded successfully!');