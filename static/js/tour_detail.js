/* =========================================
   EGY360 - Tour Detail Page Script
   Tour gallery, booking, itinerary, reviews
   ========================================= */

// Mock tour data
let tourData = {
    id: 1,
    name: "Pyramids of Giza & Sphinx Tour",
    city: "Giza",
    country: "Egypt",
    category: "Historical & Cultural",
    duration: "4 hours",
    difficulty: "Easy",
    languages: ["English", "Arabic", "French", "German", "Spanish"],
    average_rating: 9.5,
    reviews_count: 1250,
    price_per_person: 800,
    description: "Experience the wonder of ancient Egypt on this guided tour.",
    highlights: [
        "Visit the Great Pyramid of Giza",
        "See the mysterious Sphinx up close",
        "Explore all three pyramids",
        "Learn from expert Egyptologist guide",
        "Photo opportunities at the best spots"
    ],
    images: [
        "https://source.unsplash.com/800x600/?pyramids,giza,egypt",
        "https://source.unsplash.com/800x600/?sphinx,egypt",
        "https://source.unsplash.com/800x600/?pyramid,inside",
        "https://source.unsplash.com/800x600/?camel,pyramids"
    ]
};

// Gallery state
let currentImageIndex = 0;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎭 Initializing tour detail page...');
    loadTourData();
    setupBookingForm();
    setupDateDefaults();
});

// Load tour data
function loadTourData() {
    const urlPath = window.location.pathname;
    const match = urlPath.match(/\/tours\/(\d+)\//);
    const id = match ? match[1] : null;

    console.log('📊 Loading tour ID:', id);
    displayTourData(tourData);
}

// Display tour data
function displayTourData(data) {
    const tourTitle = document.getElementById('tourTitle');
    const breadcrumbTourName = document.getElementById('breadcrumbTourName');
    const ratingScore = document.getElementById('ratingScore');
    const reviewCount = document.getElementById('reviewCount');

    if (tourTitle) tourTitle.textContent = data.name;
    if (breadcrumbTourName) breadcrumbTourName.textContent = data.name;
    if (ratingScore) ratingScore.textContent = data.average_rating.toFixed(1);
    if (reviewCount) reviewCount.textContent = data.reviews_count + ' reviews';

    console.log('✅ Tour data loaded successfully');
}

// Setup booking form
function setupBookingForm() {
    const form = document.getElementById('bookingForm');
    if (!form) {
        console.log('⚠️ Booking form not found');
        return;
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Booking feature coming soon!');
    });
}

// Setup date defaults
function setupDateDefaults() {
    const today = new Date();
    const formatDate = function(date) {
        return date.toISOString().split('T')[0];
    };

    const dateInput = document.getElementById('bookDate');
    if (dateInput) {
        dateInput.value = formatDate(today);
        dateInput.min = formatDate(today);
    }
}

// Lightbox functions
function openLightbox(index) {
    currentImageIndex = index;
    console.log('🖼️ Opening lightbox:', index);

    const modal = document.getElementById('lightboxModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeLightbox() {
    console.log('🖼️ Closing lightbox');

    const modal = document.getElementById('lightboxModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % tourData.images.length;
    openLightbox(currentImageIndex);
}

function prevImage() {
    currentImageIndex = (currentImageIndex - 1 + tourData.images.length) % tourData.images.length;
    openLightbox(currentImageIndex);
}

function toggleFAQ(button) {
    const faqItem = button.closest('.faq-item');
    if (faqItem) {
        faqItem.classList.toggle('active');
    }
}

function toggleFavorite() {
    console.log('❤️ Toggle favorite');
    alert('Favorite feature coming soon!');
}

function showAuthModal(type) {
    console.log('🔐 Show auth modal:', type);
    alert('Authentication feature coming soon!');
}

function closeAuthModal() {
    console.log('🔐 Close auth modal');
}

function loadMoreReviews() {
    console.log('📖 Load more reviews');
    alert('Loading more reviews...');
}

// Make functions global
window.openLightbox = openLightbox;
window.closeLightbox = closeLightbox;
window.nextImage = nextImage;
window.prevImage = prevImage;
window.toggleFAQ = toggleFAQ;
window.toggleFavorite = toggleFavorite;
window.showAuthModal = showAuthModal;
window.closeAuthModal = closeAuthModal;
window.loadMoreReviews = loadMoreReviews;

console.log('✅ Tour detail script loaded successfully!');