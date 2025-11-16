/* =========================================
   EGY360 - Accommodation Search
   Matches Backend Fields Exactly
   ========================================= */

document.addEventListener('DOMContentLoaded', async function() {
    console.log('✅ Accommodation Search Page Loaded');
    await initSearchPage();
});

let currentFilters = {
    city_name: '',
    min_price: 0,
    max_price: 10000,
    star_rating: null,
    amenities: [],
    min_rating: null,
    page: 1
};

let accommodations = [];

async function initSearchPage() {
    loadURLParams();
    setupFilters();
    setupSearch();
    await performSearch();
}

function loadURLParams() {
    const params = new URLSearchParams(window.location.search);
    currentFilters.city_name = params.get('city') || '';
    if (document.getElementById('cityInput')) {
        document.getElementById('cityInput').value = currentFilters.city_name;
    }
}

async function performSearch() {
    showLoading();
    try {
        const data = await EgyAPI.searchAccommodations(currentFilters);
        accommodations = data.results || data;
        displayResults(accommodations);
        updateCount(data.count || accommodations.length);
    } catch (error) {
        console.error('Search error:', error);
        showEmptyState();
    }
}

function displayResults(items) {
    hideLoading();
    const grid = document.getElementById('resultsGrid');
    const empty = document.getElementById('emptyState');

    if (!items || items.length === 0) {
        showEmptyState();
        return;
    }

    empty.style.display = 'none';
    grid.style.display = 'grid';
    grid.innerHTML = items.map(acc => createCard(acc)).join('');
}

function createCard(acc) {
    const img = acc.main_image || 'https://via.placeholder.com/400x300';
    const stars = '⭐'.repeat(acc.star_rating || 0);

    return `
        <div class="accommodation-card" onclick="location.href='/accommodations/${acc.id}/'">
            <div class="card-image">
                <img src="${img}" alt="${acc.name}">
                ${acc.is_verified ? '<div class="card-badge verified"><i class="fas fa-check-circle"></i> Verified</div>' : ''}
            </div>
            <div class="card-content">
                <div class="card-header">
                    <div>
                        <h3 class="card-title">${acc.name}</h3>
                        <p class="card-location"><i class="fas fa-map-marker-alt"></i> ${acc.city_name}</p>
                    </div>
                    <div class="card-rating">
                        <span class="rating-score">${(acc.average_rating || 0).toFixed(1)}</span>
                        <div class="rating-stars">${stars}</div>
                        <span class="rating-count">(${acc.total_reviews || 0})</span>
                    </div>
                </div>
                ${acc.safety_score ? `
                <div class="card-safety">
                    <div class="safety-badge">
                        <i class="fas fa-shield-alt"></i>
                        <span>Safety: ${acc.safety_score}/100</span>
                    </div>
                </div>
                ` : ''}
                <div class="card-footer">
                    <div class="card-price">
                        <span class="price-label">From</span>
                        <span class="price-amount">${acc.price_per_night}</span>
                        <span class="price-period">EGP/night</span>
                    </div>
                    <button class="btn-book">View Details</button>
                </div>
            </div>
        </div>
    `;
}

function setupFilters() {
    const minPrice = document.getElementById('minPrice');
    const maxPrice = document.getElementById('maxPrice');

    if (minPrice) {
        minPrice.addEventListener('input', (e) => {
            currentFilters.min_price = parseInt(e.target.value);
            document.getElementById('minPriceDisplay').textContent = `${currentFilters.min_price} EGP`;
        });
    }

    if (maxPrice) {
        maxPrice.addEventListener('input', (e) => {
            currentFilters.max_price = parseInt(e.target.value);
            document.getElementById('maxPriceDisplay').textContent = `${currentFilters.max_price} EGP`;
        });
    }

    document.querySelectorAll('input[name="stars"]').forEach(cb => {
        cb.addEventListener('change', (e) => {
            currentFilters.star_rating = e.target.checked ? e.target.value : null;
            if (e.target.checked) {
                document.querySelectorAll('input[name="stars"]').forEach(other => {
                    if (other !== e.target) other.checked = false;
                });
            }
        });
    });

    const resetBtn = document.getElementById('resetFilters');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            currentFilters = { city_name: '', min_price: 0, max_price: 10000, page: 1 };
            document.querySelectorAll('.filter-checkbox').forEach(cb => cb.checked = false);
            performSearch();
        });
    }

    const applyBtn = document.getElementById('applyFilters');
    if (applyBtn) {
        applyBtn.addEventListener('click', performSearch);
    }
}

function setupSearch() {
    const form = document.getElementById('searchForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            currentFilters.city_name = document.getElementById('cityInput').value;
            await performSearch();
        });
    }
}

function updateCount(count) {
    const el = document.getElementById('totalResults');
    if (el) el.textContent = count;
}

function showLoading() {
    document.getElementById('loadingState').style.display = 'flex';
    document.getElementById('resultsGrid').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
}

function showEmptyState() {
    hideLoading();
    document.getElementById('resultsGrid').style.display = 'none';
    document.getElementById('emptyState').style.display = 'flex';
}

console.log('✅ Search script ready');