/* =========================================
   EGY360 - Accommodation Detail Page Script
   Image gallery, booking, reviews, dynamic content
   ========================================= */

// Mock data for the accommodation
let accommodationData = {
    id: 1,
    name: "Pyramids View Hotel",
    city: "Giza",
    country: "Egypt",
    accommodation_type: "hotel",
    star_rating: 5,
    average_rating: 9.2,
    reviews_count: 450,
    price_per_night: 2500,
    max_guests: 4,
    bedrooms: 2,
    bathrooms: 2,
    safety_score: 98,
    is_verified: true,
    description: "Experience luxury and comfort at this stunning property located in the heart of Giza with breathtaking views of the Great Pyramids. Perfect for both business and leisure travelers, our accommodation offers world-class amenities and exceptional service that will make your stay unforgettable.",
    amenities: {
        wifi: true,
        pool: true,
        parking: true,
        gym: true,
        restaurant: true,
        spa: true,
        beach: false,
        room_service: true,
        concierge: true,
        laundry: true,
        bar: true,
        breakfast: true
    },
    images: [
        "https://source.unsplash.com/800x600/?luxury,hotel,pyramids,egypt",
        "https://source.unsplash.com/800x600/?hotel,room,luxury",
        "https://source.unsplash.com/800x600/?hotel,lobby,elegant",
        "https://source.unsplash.com/800x600/?hotel,pool,luxury",
        "https://source.unsplash.com/800x600/?hotel,restaurant",
        "https://source.unsplash.com/800x600/?hotel,spa",
        "https://source.unsplash.com/800x600/?hotel,gym",
        "https://source.unsplash.com/800x600/?hotel,bar",
        "https://source.unsplash.com/800x600/?hotel,breakfast",
        "https://source.unsplash.com/800x600/?hotel,view,night"
    ]
};

// Gallery state
let currentImageIndex = 0;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏨 Initializing accommodation detail page...');
    loadAccommodationData();
    setupBookingForm();
    setupDateDefaults();
    animateSafetyScore();
});

// Load accommodation data
function loadAccommodationData() {
    // Get ID from URL
    const urlPath = window.location.pathname;
    const id = urlPath.match(/\/accommodations\/(\d+)\//)?.[1];

    console.log('📊 Loading accommodation ID:', id);

    // In production, fetch from API
    // For now, use mock data
    displayAccommodationData(accommodationData);
}

// Display accommodation data
function displayAccommodationData(data) {
    // Header
    document.querySelector('.property-title').textContent = data.name;
    document.getElementById('starIcons').textContent = '★'.repeat(data.star_rating);
    document.getElementById('locationText').textContent = `${data.city}, ${data.country}`;
    document.getElementById('ratingScore').textContent = data.average_rating.toFixed(1);
    document.getElementById('reviewCount').textContent = `${data.reviews_count} reviews`;

    // Verified badge
    if (!data.is_verified) {
        document.getElementById('verifiedBadge').style.display = 'none';
    }

    // Quick info
    document.getElementById('maxGuests').textContent = `${data.max_guests} guests`;
    document.getElementById('bedrooms').textContent = `${data.bedrooms} bedrooms`;
    document.getElementById('bathrooms').textContent = `${data.bathrooms} bathrooms`;
    document.getElementById('propertyType').textContent = data.accommodation_type.charAt(0).toUpperCase() + data.accommodation_type.slice(1);

    // Description
    document.getElementById('propertyDescription').innerHTML = `<p>${data.description}</p>`;

    // Amenities
    displayAmenities(data.amenities);

    // Safety score
    document.getElementById('safetyScoreNumber').textContent = data.safety_score;

    // Booking card
    document.getElementById('bookingPrice').textContent = data.price_per_night.toLocaleString();
    document.getElementById('sidebarRating').textContent = data.average_rating.toFixed(1);
    document.getElementById('sidebarReviewCount').textContent = data.reviews_count;
    document.getElementById('pricePerNight').textContent = data.price_per_night.toLocaleString();

    // Reviews
    document.getElementById('overallScore').textContent = data.average_rating.toFixed(1);
    document.getElementById('totalReviews').textContent = `${data.reviews_count} reviews`;

    // Location
    document.getElementById('fullAddress').textContent = `${data.city}, ${data.country}`;

    // Images
    document.getElementById('mainImage').src = data.images[0];

    // Load rooms
    displayRooms();

    // Load reviews
    displayReviews();

    // Load similar properties
    displaySimilarProperties();

    console.log('✅ Accommodation data loaded successfully');
}

// Display amenities
function displayAmenities(amenities) {
    const amenitiesGrid = document.getElementById('amenitiesGrid');

    const amenityIcons = {
        wifi: 'fa-wifi',
        pool: 'fa-swimming-pool',
        parking: 'fa-parking',
        gym: 'fa-dumbbell',
        restaurant: 'fa-utensils',
        spa: 'fa-spa',
        beach: 'fa-umbrella-beach',
        room_service: 'fa-concierge-bell',
        concierge: 'fa-user-tie',
        laundry: 'fa-soap',
        bar: 'fa-glass-martini-alt',
        breakfast: 'fa-mug-hot'
    };

    const amenityLabels = {
        wifi: 'Free WiFi',
        pool: 'Swimming Pool',
        parking: 'Free Parking',
        gym: 'Fitness Center',
        restaurant: 'Restaurant',
        spa: 'Spa & Wellness',
        beach: 'Beach Access',
        room_service: 'Room Service',
        concierge: 'Concierge',
        laundry: 'Laundry Service',
        bar: 'Bar & Lounge',
        breakfast: 'Breakfast Included'
    };

    let html = '';

    for (const [key, value] of Object.entries(amenities)) {
        if (value) {
            html += `
                <div class="amenity-item">
                    <i class="fas ${amenityIcons[key]}"></i>
                    <span>${amenityLabels[key]}</span>
                </div>
            `;
        }
    }

    amenitiesGrid.innerHTML = html;
}

// Animate safety score circle
function animateSafetyScore() {
    const score = parseInt(document.getElementById('safetyScoreNumber').textContent);
    const circle = document.getElementById('scoreCircle');
    const circumference = 2 * Math.PI * 45; // radius = 45
    const offset = circumference - (score / 100) * circumference;

    setTimeout(() => {
        circle.style.strokeDashoffset = offset;
    }, 300);
}

// Display rooms
function displayRooms() {
    const roomsList = document.getElementById('roomsList');

    const mockRooms = [
        {
            name: "Deluxe Room with Pyramid View",
            beds: "1 King Bed",
            size: "35 m²",
            guests: "2 guests",
            price: 2500,
            image: "https://source.unsplash.com/400x300/?hotel,room,luxury,bed"
        },
        {
            name: "Premium Suite",
            beds: "1 King Bed + Sofa Bed",
            size: "50 m²",
            guests: "4 guests",
            price: 3800,
            image: "https://source.unsplash.com/400x300/?hotel,suite,luxury"
        },
        {
            name: "Family Room",
            beds: "2 Queen Beds",
            size: "42 m²",
            guests: "4 guests",
            price: 3200,
            image: "https://source.unsplash.com/400x300/?hotel,room,family"
        }
    ];

    let html = '';

    mockRooms.forEach(room => {
        html += `
            <div class="room-card">
                <div class="room-image">
                    <img src="${room.image}" alt="${room.name}">
                </div>
                <div class="room-info">
                    <h3>${room.name}</h3>
                    <div class="room-features">
                        <span><i class="fas fa-bed"></i> ${room.beds}</span>
                        <span><i class="fas fa-expand-arrows-alt"></i> ${room.size}</span>
                        <span><i class="fas fa-users"></i> ${room.guests}</span>
                    </div>
                </div>
                <div class="room-price">
                    <div class="room-price-amount">${room.price.toLocaleString()} EGP</div>
                    <div class="room-price-period">per night</div>
                </div>
            </div>
        `;
    });

    roomsList.innerHTML = html;
}

// Display reviews
function displayReviews() {
    const reviewsList = document.getElementById('reviewsList');

    const mockReviews = [
        {
            author: "Sarah Johnson",
            date: "2 days ago",
            rating: 10,
            text: "Absolutely stunning property! The view of the pyramids from our room was breathtaking. Staff was incredibly helpful and the facilities were top-notch. Highly recommend!"
        },
        {
            author: "Michael Chen",
            date: "1 week ago",
            rating: 9,
            text: "Great location and excellent service. The pool area was beautiful and the restaurant served delicious food. Only minor issue was the WiFi speed in the room."
        },
        {
            author: "Emma Williams",
            date: "2 weeks ago",
            rating: 10,
            text: "Perfect stay! Everything was immaculate and the staff went above and beyond. The spa treatments were wonderful and we loved the complimentary breakfast."
        }
    ];

    let html = '';

    mockReviews.forEach(review => {
        const initials = review.author.split(' ').map(n => n[0]).join('');
        const stars = '★'.repeat(Math.floor(review.rating));

        html += `
            <div class="review-item">
                <div class="review-header">
                    <div class="review-author">
                        <div class="author-avatar">${initials}</div>
                        <div class="author-info">
                            <div class="author-name">${review.author}</div>
                            <div class="review-date">${review.date}</div>
                        </div>
                    </div>
                    <div class="review-rating">
                        <span>${stars}</span>
                        <strong>${review.rating}/10</strong>
                    </div>
                </div>
                <p class="review-text">${review.text}</p>
            </div>
        `;
    });

    reviewsList.innerHTML = html;
}

// Load more reviews
function loadMoreReviews() {
    alert('Loading more reviews... (Feature coming soon!)');
}

// Display similar properties
function displaySimilarProperties() {
    const similarGrid = document.getElementById('similarGrid');

    const mockSimilar = [
        {
            id: 2,
            name: "Nile Riverside Resort",
            city: "Cairo",
            price: 1800,
            rating: 8.8,
            image: "https://source.unsplash.com/400x300/?hotel,nile,egypt"
        },
        {
            id: 3,
            name: "Luxor Palace Hotel",
            city: "Luxor",
            price: 2200,
            rating: 9.1,
            image: "https://source.unsplash.com/400x300/?hotel,luxor"
        },
        {
            id: 4,
            name: "Red Sea Beach Resort",
            city: "Hurghada",
            price: 2800,
            rating: 8.9,
            image: "https://source.unsplash.com/400x300/?hotel,beach,redsea"
        }
    ];

    let html = '';

    mockSimilar.forEach(property => {
        html += `
            <div class="similar-card" onclick="window.location.href='/accommodations/${property.id}/'">
                <div class="similar-image">
                    <img src="${property.image}" alt="${property.name}">
                </div>
                <div class="similar-content">
                    <h3 class="similar-title">${property.name}</h3>
                    <p class="similar-location"><i class="fas fa-map-marker-alt"></i> ${property.city}, Egypt</p>
                    <div class="similar-footer">
                        <div class="similar-price">${property.price.toLocaleString()} EGP</div>
                        <div class="similar-rating">
                            <i class="fas fa-star"></i>
                            <span>${property.rating.toFixed(1)}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    similarGrid.innerHTML = html;
}

// Setup booking form
function setupBookingForm() {
    const form = document.getElementById('bookingForm');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const checkIn = document.getElementById('bookCheckIn').value;
        const checkOut = document.getElementById('bookCheckOut').value;
        const guests = document.getElementById('bookGuests').value;

        if (!checkIn || !checkOut) {
            alert('Please select check-in and check-out dates');
            return;
        }

        if (new Date(checkOut) <= new Date(checkIn)) {
            alert('Check-out date must be after check-in date');
            return;
        }

        console.log('📅 Booking request:', { checkIn, checkOut, guests });

        // In production, submit to API
        alert('Booking request submitted! (Feature coming soon)');
    });

    // Listen for date changes to update price
    const checkInInput = document.getElementById('bookCheckIn');
    const checkOutInput = document.getElementById('bookCheckOut');

    checkInInput.addEventListener('change', calculatePrice);
    checkOutInput.addEventListener('change', calculatePrice);
}

// Set default dates
function setupDateDefaults() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const formatDate = (date) => {
        return date.toISOString().split('T')[0];
    };

    const checkInInput = document.getElementById('bookCheckIn');
    const checkOutInput = document.getElementById('bookCheckOut');

    checkInInput.value = formatDate(today);
    checkInInput.min = formatDate(today);

    checkOutInput.value = formatDate(tomorrow);
    checkOutInput.min = formatDate(tomorrow);

    // Update min date when check-in changes
    checkInInput.addEventListener('change', function() {
        const checkInDate = new Date(this.value);
        const nextDay = new Date(checkInDate);
        nextDay.setDate(nextDay.getDate() + 1);
        checkOutInput.min = formatDate(nextDay);

        // If check-out is before new check-in, update it
        if (new Date(checkOutInput.value) <= checkInDate) {
            checkOutInput.value = formatDate(nextDay);
        }

        calculatePrice();
    });

    // Calculate initial price
    calculatePrice();
}

// Calculate booking price
function calculatePrice() {
    const checkIn = document.getElementById('bookCheckIn').value;
    const checkOut = document.getElementById('bookCheckOut').value;

    if (!checkIn || !checkOut) {
        return;
    }

    const checkInDate = new Date(checkIn);
    const checkOutDate = new Date(checkOut);

    // Calculate number of nights
    const nights = Math.ceil((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24));

    if (nights <= 0) {
        return;
    }

    const pricePerNight = accommodationData.price_per_night;
    const subtotal = pricePerNight * nights;
    const serviceFee = Math.round(subtotal * 0.1); // 10% service fee
    const total = subtotal + serviceFee;

    // Update display
    document.getElementById('numNights').textContent = nights;
    document.getElementById('subtotal').textContent = `${subtotal.toLocaleString()} EGP`;
    document.getElementById('serviceFee').textContent = `${serviceFee.toLocaleString()} EGP`;
    document.getElementById('totalPrice').textContent = `${total.toLocaleString()} EGP`;

    console.log('💰 Price calculated:', { nights, subtotal, serviceFee, total });
}

// Lightbox functions
function openLightbox(index) {
    currentImageIndex = index;
    const modal = document.getElementById('lightboxModal');
    const img = document.getElementById('lightboxImage');
    const counter = document.getElementById('lightboxCounter');

    img.src = accommodationData.images[index];
    counter.textContent = `${index + 1} / ${accommodationData.images.length}`;
    modal.classList.add('active');

    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const modal = document.getElementById('lightboxModal');
    modal.classList.remove('active');

    // Restore body scroll
    document.body.style.overflow = '';
}

function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % accommodationData.images.length;
    openLightbox(currentImageIndex);
}

function prevImage() {
    currentImageIndex = (currentImageIndex - 1 + accommodationData.images.length) % accommodationData.images.length;
    openLightbox(currentImageIndex);
}

// Keyboard navigation for lightbox
document.addEventListener('keydown', function(e) {
    const modal = document.getElementById('lightboxModal');
    if (!modal.classList.contains('active')) return;

    if (e.key === 'Escape') {
        closeLightbox();
    } else if (e.key === 'ArrowRight') {
        nextImage();
    } else if (e.key === 'ArrowLeft') {
        prevImage();
    }
});

// Toggle favorite
function toggleFavorite() {
    console.log('❤️ Toggle favorite');
    alert('Favorite feature coming soon!');
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
                <p style="text-align: center; margin-top: 16px; color: #666;">
                    Don't have an account? 
                    <a href="#" onclick="showAuthModal('signup'); return false;" style="color: #E31E24; font-weight: 600;">Sign Up</a>
                </p>
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
                <input type="password" placeholder="Confirm Password" required
                       style="padding: 14px; border: 2px solid #E0E0E0; border-radius: 8px; font-size: 16px;">
                <button type="submit" class="btn-primary" style="padding: 14px; font-size: 16px; margin-top: 8px;">
                    Create Account
                </button>
                <p style="text-align: center; margin-top: 16px; color: #666;">
                    Already have an account? 
                    <a href="#" onclick="showAuthModal('signin'); return false;" style="color: #E31E24; font-weight: 600;">Sign In</a>
                </p>
            </form>
        `;
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeAuthModal() {
    const modal = document.getElementById('authModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

// Make functions global
window.openLightbox = openLightbox;
window.closeLightbox = closeLightbox;
window.nextImage = nextImage;
window.prevImage = prevImage;
window.toggleFavorite = toggleFavorite;
window.showAuthModal = showAuthModal;
window.closeAuthModal = closeAuthModal;
window.loadMoreReviews = loadMoreReviews;

console.log('✅ Accommodation detail script loaded successfully!');