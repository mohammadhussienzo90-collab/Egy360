/* =========================================
   EGY360 - User Dashboard Script
   Dashboard navigation, bookings, favorites, reviews
   ========================================= */

// Mock User Data
let userData = {
    firstName: "John",
    lastName: "Doe",
    email: "john.doe@email.com",
    phone: "+20 123 456 7890",
    country: "EG",
    city: "Cairo",
    bio: "Travel enthusiast exploring Egypt's wonders!",
    stats: {
        upcomingTrips: 2,
        completedTrips: 8,
        favorites: 12,
        reviews: 5
    },
    bookings: {
        upcoming: [
            {
                id: 1,
                type: "accommodation",
                name: "Pyramids View Hotel",
                location: "Giza, Egypt",
                checkIn: "2024-12-25",
                checkOut: "2024-12-28",
                guests: 2,
                status: "confirmed",
                price: 7500,
                image: "https://source.unsplash.com/400x300/?hotel,pyramids"
            },
            {
                id: 2,
                type: "tour",
                name: "Luxor Valley of the Kings Tour",
                location: "Luxor, Egypt",
                date: "2024-12-26",
                time: "9:00 AM",
                travelers: 2,
                status: "confirmed",
                price: 3600,
                image: "https://source.unsplash.com/400x300/?luxor,valley"
            }
        ],
        past: [
            {
                id: 3,
                type: "tour",
                name: "Pyramids of Giza Tour",
                location: "Giza, Egypt",
                date: "2024-10-15",
                status: "completed",
                price: 1600,
                image: "https://source.unsplash.com/400x300/?pyramids,giza"
            },
            {
                id: 4,
                type: "accommodation",
                name: "Nile Riverside Resort",
                location: "Cairo, Egypt",
                checkIn: "2024-09-10",
                checkOut: "2024-09-13",
                status: "completed",
                price: 5400,
                image: "https://source.unsplash.com/400x300/?nile,hotel"
            }
        ],
        cancelled: [
            {
                id: 5,
                type: "tour",
                name: "White Desert Safari",
                location: "Farafra, Egypt",
                date: "2024-08-20",
                status: "cancelled",
                price: 7000,
                image: "https://source.unsplash.com/400x300/?desert,white"
            }
        ]
    },
    favorites: [
        {
            id: 1,
            type: "accommodation",
            name: "Red Sea Beach Resort",
            location: "Hurghada",
            price: 2800,
            rating: 8.9,
            image: "https://source.unsplash.com/400x300/?beach,resort,redsea"
        },
        {
            id: 2,
            type: "tour",
            name: "Nile Dinner Cruise",
            location: "Cairo",
            price: 1200,
            rating: 8.8,
            image: "https://source.unsplash.com/400x300/?nile,cruise"
        },
        {
            id: 3,
            type: "accommodation",
            name: "Alexandria Palace Hotel",
            location: "Alexandria",
            price: 2200,
            rating: 9.1,
            image: "https://source.unsplash.com/400x300/?alexandria,hotel"
        },
        {
            id: 4,
            type: "tour",
            name: "Egyptian Museum Tour",
            location: "Cairo",
            price: 950,
            rating: 9.2,
            image: "https://source.unsplash.com/400x300/?egyptian,museum"
        }
    ],
    reviews: [
        {
            id: 1,
            propertyName: "Pyramids View Hotel",
            propertyType: "accommodation",
            rating: 9,
            date: "2024-10-20",
            text: "Amazing experience! The view of the pyramids from our room was breathtaking. Staff was incredibly helpful."
        },
        {
            id: 2,
            propertyName: "Pyramids of Giza Tour",
            propertyType: "tour",
            rating: 10,
            date: "2024-10-15",
            text: "Best tour ever! Our guide was so knowledgeable and the pyramids are even more impressive in person."
        }
    ]
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('👤 Initializing user dashboard...');
    loadUserData();
    setupEventListeners();
    loadDashboardData();
});

// Load User Data
function loadUserData() {
    document.getElementById('userName').textContent = `${userData.firstName} ${userData.lastName}`;
    document.getElementById('userEmail').textContent = userData.email;
    document.getElementById('welcomeName').textContent = userData.firstName;

    // Set initials in avatar
    const initials = `${userData.firstName[0]}${userData.lastName[0]}`;
    document.querySelectorAll('.user-avatar, .profile-avatar-large').forEach(avatar => {
        avatar.textContent = initials;
    });

    // Update badges
    document.getElementById('bookingsBadge').textContent = userData.stats.upcomingTrips;
    document.getElementById('favoritesBadge').textContent = userData.stats.favorites;

    console.log('✅ User data loaded');
}

// Setup Event Listeners
function setupEventListeners() {
    // Sidebar navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.dataset.section;
            switchSection(section);
        });
    });

    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.dataset.tab;
            switchTab(tab);
        });
    });

    // Mobile menu toggle
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const sidebar = document.getElementById('dashboardSidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function() {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
    }

    // Profile form
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', handleProfileSubmit);
    }

    console.log('✅ Event listeners set up');
}

// Switch Section
function switchSection(section) {
    // Update sidebar navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.section === section) {
            item.classList.add('active');
        }
    });

    // Update main content
    document.querySelectorAll('.dashboard-section').forEach(sec => {
        sec.classList.remove('active');
    });
    document.getElementById(`${section}-section`).classList.add('active');

    // Close mobile sidebar
    const sidebar = document.getElementById('dashboardSidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (sidebar) sidebar.classList.remove('active');
    if (overlay) overlay.classList.remove('active');

    console.log('📄 Switched to section:', section);
}

// Switch Tab
function switchTab(tab) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tab) {
            btn.classList.add('active');
        }
    });

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tab}-tab`).classList.add('active');

    console.log('📑 Switched to tab:', tab);
}

// Load Dashboard Data
function loadDashboardData() {
    // Update stats
    document.getElementById('upcomingTripsCount').textContent = userData.stats.upcomingTrips;
    document.getElementById('completedTripsCount').textContent = userData.stats.completedTrips;
    document.getElementById('favoritesCount').textContent = userData.stats.favorites;
    document.getElementById('reviewsCount').textContent = userData.stats.reviews;

    // Load bookings
    loadBookings();

    // Load favorites
    loadFavorites();

    // Load reviews
    loadReviews();

    console.log('✅ Dashboard data loaded');
}

// Load Bookings
function loadBookings() {
    // Upcoming bookings in overview
    const upcomingList = document.getElementById('upcomingBookingsList');
    upcomingList.innerHTML = '';
    userData.bookings.upcoming.slice(0, 2).forEach(booking => {
        upcomingList.appendChild(createBookingCard(booking));
    });

    // All upcoming bookings
    const allUpcoming = document.getElementById('allUpcomingBookings');
    allUpcoming.innerHTML = '';
    userData.bookings.upcoming.forEach(booking => {
        allUpcoming.appendChild(createBookingCard(booking));
    });

    // Past bookings
    const past = document.getElementById('pastBookings');
    past.innerHTML = '';
    userData.bookings.past.forEach(booking => {
        past.appendChild(createBookingCard(booking));
    });

    // Cancelled bookings
    const cancelled = document.getElementById('cancelledBookings');
    cancelled.innerHTML = '';
    userData.bookings.cancelled.forEach(booking => {
        cancelled.appendChild(createBookingCard(booking));
    });

    console.log('📅 Bookings loaded');
}

// Create Booking Card
function createBookingCard(booking) {
    const card = document.createElement('div');
    card.className = 'booking-card';

    const statusClass = `status-${booking.status}`;
    const statusText = booking.status.charAt(0).toUpperCase() + booking.status.slice(1);

    let dateInfo = '';
    if (booking.type === 'accommodation') {
        dateInfo = `
            <span><i class="fas fa-calendar"></i> ${formatDate(booking.checkIn)} - ${formatDate(booking.checkOut)}</span>
            <span><i class="fas fa-users"></i> ${booking.guests} guests</span>
        `;
    } else {
        dateInfo = `
            <span><i class="fas fa-calendar"></i> ${formatDate(booking.date)}</span>
            <span><i class="fas fa-clock"></i> ${booking.time || 'N/A'}</span>
            <span><i class="fas fa-users"></i> ${booking.travelers} travelers</span>
        `;
    }

    let actions = '';
    if (booking.status === 'confirmed') {
        actions = `
            <button class="btn-small btn-view" onclick="viewBooking(${booking.id})">View Details</button>
            <button class="btn-small btn-cancel" onclick="cancelBooking(${booking.id})">Cancel</button>
        `;
    } else if (booking.status === 'completed') {
        actions = `
            <button class="btn-small btn-view" onclick="viewBooking(${booking.id})">View Details</button>
            <button class="btn-small btn-view" onclick="writeReview(${booking.id})">Write Review</button>
        `;
    } else {
        actions = `<button class="btn-small btn-view" onclick="viewBooking(${booking.id})">View Details</button>`;
    }

    card.innerHTML = `
        <div class="booking-image">
            <img src="${booking.image}" alt="${booking.name}">
        </div>
        <div class="booking-info">
            <h3>${booking.name}</h3>
            <div class="booking-meta">
                <span><i class="fas fa-map-marker-alt"></i> ${booking.location}</span>
                ${dateInfo}
            </div>
            <span class="booking-status ${statusClass}">${statusText}</span>
        </div>
        <div class="booking-actions">
            ${actions}
        </div>
    `;

    return card;
}

// Load Favorites
function loadFavorites() {
    // Recent favorites in overview
    const recentFav = document.getElementById('recentFavorites');
    recentFav.innerHTML = '';
    userData.favorites.slice(0, 4).forEach(item => {
        recentFav.appendChild(createFavoriteCard(item));
    });

    // All favorites
    const allFav = document.getElementById('allFavorites');
    allFav.innerHTML = '';
    userData.favorites.forEach(item => {
        allFav.appendChild(createFavoriteCard(item));
    });

    console.log('⭐ Favorites loaded');
}

// Create Favorite Card
function createFavoriteCard(item) {
    const card = document.createElement('div');
    card.className = 'favorite-card';
    card.onclick = () => {
        if (item.type === 'accommodation') {
            window.location.href = `/accommodations/${item.id}/`;
        } else {
            window.location.href = `/tours/${item.id}/`;
        }
    };

    card.innerHTML = `
        <div class="favorite-image">
            <img src="${item.image}" alt="${item.name}">
            <button class="btn-remove-favorite" onclick="event.stopPropagation(); removeFavorite(${item.id})">
                <i class="fas fa-heart"></i>
            </button>
        </div>
        <div class="favorite-content">
            <h3 class="favorite-title">${item.name}</h3>
            <p class="favorite-location"><i class="fas fa-map-marker-alt"></i> ${item.location}, Egypt</p>
            <div class="favorite-footer">
                <div class="favorite-price">${item.price.toLocaleString()} EGP</div>
                <div class="favorite-rating">
                    <i class="fas fa-star"></i>
                    <span>${item.rating.toFixed(1)}</span>
                </div>
            </div>
        </div>
    `;

    return card;
}

// Load Reviews
function loadReviews() {
    const reviewsList = document.getElementById('userReviews');
    reviewsList.innerHTML = '';

    userData.reviews.forEach(review => {
        const card = document.createElement('div');
        card.className = 'review-card';

        const stars = '★'.repeat(review.rating);

        card.innerHTML = `
            <div class="review-header">
                <div class="review-property">
                    <h3>${review.propertyName}</h3>
                    <p class="review-date">${formatDate(review.date)}</p>
                </div>
                <div class="review-rating-display">
                    <span>${stars}</span>
                    <strong>${review.rating}/10</strong>
                </div>
            </div>
            <p class="review-text">${review.text}</p>
            <div class="review-actions">
                <button class="btn-link" onclick="editReview(${review.id})">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button class="btn-link" onclick="deleteReview(${review.id})">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </div>
        `;

        reviewsList.appendChild(card);
    });

    console.log('💬 Reviews loaded');
}

// Format Date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

// Handle Profile Submit
function handleProfileSubmit(e) {
    e.preventDefault();

    userData.firstName = document.getElementById('firstName').value;
    userData.lastName = document.getElementById('lastName').value;
    userData.email = document.getElementById('email').value;
    userData.phone = document.getElementById('phone').value;
    userData.country = document.getElementById('country').value;
    userData.city = document.getElementById('city').value;
    userData.bio = document.getElementById('bio').value;

    loadUserData();

    alert('Profile updated successfully!');
    console.log('✅ Profile updated');
}

// Booking Actions
function viewBooking(id) {
    console.log('👁️ View booking:', id);
    alert(`View booking details for ID: ${id}\n(Feature coming soon!)`);
}

function cancelBooking(id) {
    if (confirm('Are you sure you want to cancel this booking?')) {
        console.log('❌ Cancel booking:', id);
        alert('Booking cancelled! (Feature coming soon)');
    }
}

function writeReview(id) {
    console.log('✍️ Write review for booking:', id);
    alert(`Write a review for booking ID: ${id}\n(Feature coming soon!)`);
}

// Favorite Actions
function removeFavorite(id) {
    if (confirm('Remove from favorites?')) {
        console.log('💔 Remove favorite:', id);
        userData.favorites = userData.favorites.filter(f => f.id !== id);
        userData.stats.favorites = userData.favorites.length;
        loadDashboardData();
        alert('Removed from favorites!');
    }
}

// Review Actions
function editReview(id) {
    console.log('✏️ Edit review:', id);
    alert(`Edit review ID: ${id}\n(Feature coming soon!)`);
}

function deleteReview(id) {
    if (confirm('Delete this review?')) {
        console.log('🗑️ Delete review:', id);
        userData.reviews = userData.reviews.filter(r => r.id !== id);
        userData.stats.reviews = userData.reviews.length;
        loadDashboardData();
        alert('Review deleted!');
    }
}

// Settings Actions
function changePassword() {
    console.log('🔒 Change password');
    alert('Change password feature coming soon!');
}

function deleteAccount() {
    if (confirm('⚠️ WARNING: This will permanently delete your account and all data.\n\nAre you absolutely sure?')) {
        if (confirm('This action cannot be undone. Delete account?')) {
            console.log('🗑️ Delete account');
            alert('Account deletion feature coming soon!');
        }
    }
}

// Logout
function logout() {
    if (confirm('Are you sure you want to sign out?')) {
        console.log('👋 Logging out...');
        alert('Logged out! (Redirecting to home...)');
        window.location.href = '/';
    }
}

// Make functions global
window.switchSection = switchSection;
window.viewBooking = viewBooking;
window.cancelBooking = cancelBooking;
window.writeReview = writeReview;
window.removeFavorite = removeFavorite;
window.editReview = editReview;
window.deleteReview = deleteReview;
window.changePassword = changePassword;
window.deleteAccount = deleteAccount;
window.logout = logout;

console.log('✅ User dashboard script loaded!');