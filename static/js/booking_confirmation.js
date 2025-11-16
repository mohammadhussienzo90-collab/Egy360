/* =========================================
   EGY360 - Booking Confirmation Script
   Displays booking details and confirmation
   ========================================= */

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Loading booking confirmation...');
    loadBookingDetails();
});

// Load Booking Details
function loadBookingDetails() {
    // Get booking ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const bookingId = urlParams.get('id');

    // Try to load from sessionStorage
    let bookingData = null;
    try {
        const storedData = sessionStorage.getItem('latestBooking');
        if (storedData) {
            bookingData = JSON.parse(storedData);
            console.log('✅ Booking data loaded:', bookingData);
        }
    } catch (error) {
        console.error('Error loading booking data:', error);
    }

    // If no data found, use mock data
    if (!bookingData) {
        bookingData = getMockBookingData(bookingId);
        console.log('⚠️ Using mock booking data');
    }

    // Display booking details
    displayBookingDetails(bookingData);
}

// Get Mock Booking Data
function getMockBookingData(bookingId) {
    return {
        bookingId: bookingId || 'BK12345678',
        status: 'confirmed',
        type: 'accommodation',

        // Property details
        propertyId: 1,
        propertyName: 'Cairo Pyramids Hotel',
        propertyLocation: 'Giza, Cairo, Egypt',
        propertyImage: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400',
        propertyRating: 4.8,

        // Dates
        checkIn: '2024-12-25',
        checkOut: '2024-12-28',
        tourDate: null,

        // Guests
        guests: '2',
        roomType: 'Standard Room',

        // Guest info
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@email.com',
        phone: '+20 123 456 7890',
        country: 'Egypt',

        // Special requests
        earlyCheckin: true,
        lateCheckout: false,
        airportPickup: true,
        nonSmoking: true,
        additionalRequests: 'Please provide a room with a pyramid view',

        // Price
        total: '4,500 EGP',

        // Timestamp
        bookingDate: new Date().toISOString()
    };
}

// Display Booking Details
function displayBookingDetails(booking) {
    // Booking reference
    document.getElementById('bookingReference').textContent = booking.bookingId;

    // Email
    document.getElementById('confirmEmail').textContent = booking.email;

    // Property details
    document.getElementById('confirmPropertyName').textContent = booking.propertyName;
    document.getElementById('confirmLocation').innerHTML = `<i class="fas fa-map-marker-alt"></i> ${booking.propertyLocation}`;
    document.getElementById('confirmImage').src = booking.propertyImage;

    // Guest name
    const guestName = `${booking.firstName} ${booking.lastName}`;
    document.getElementById('guestName').textContent = guestName;
    document.getElementById('guestEmail').textContent = booking.email;
    document.getElementById('guestPhone').textContent = booking.phone;

    // Handle accommodation vs tour
    if (booking.type === 'accommodation') {
        // Show accommodation fields
        document.getElementById('checkInInfo').style.display = 'flex';
        document.getElementById('checkOutInfo').style.display = 'flex';
        document.getElementById('tourDateInfo').style.display = 'none';

        // Format dates
        const checkIn = new Date(booking.checkIn);
        const checkOut = new Date(booking.checkOut);

        document.getElementById('checkInDate').textContent = formatDate(checkIn);
        document.getElementById('checkOutDate').textContent = formatDate(checkOut);

        // Calculate nights
        const nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
        document.getElementById('duration').textContent = `${nights} Night${nights !== 1 ? 's' : ''}`;

        // Room type
        document.getElementById('roomType').textContent = booking.roomType || 'Standard Room';
    } else {
        // Show tour fields
        document.getElementById('checkInInfo').style.display = 'none';
        document.getElementById('checkOutInfo').style.display = 'none';
        document.getElementById('tourDateInfo').style.display = 'flex';

        const tourDate = new Date(booking.tourDate);
        document.getElementById('tourDate').textContent = formatDate(tourDate);
        document.getElementById('duration').textContent = 'Full Day';
    }

    // Guests
    document.getElementById('guestCount').textContent = `${booking.guests} Guest${booking.guests !== '1' ? 's' : ''}`;

    // Total price
    document.getElementById('totalPrice').textContent = booking.total;

    // Special requests
    displaySpecialRequests(booking);

    console.log('✅ Booking details displayed');
}

// Display Special Requests
function displaySpecialRequests(booking) {
    const requests = [];

    if (booking.earlyCheckin) requests.push('Early check-in requested');
    if (booking.lateCheckout) requests.push('Late check-out requested');
    if (booking.airportPickup) requests.push('Airport pickup service requested');
    if (booking.nonSmoking) requests.push('Non-smoking room requested');
    if (booking.additionalRequests && booking.additionalRequests.trim()) {
        requests.push(booking.additionalRequests);
    }

    if (requests.length > 0) {
        const section = document.getElementById('specialRequestsSection');
        const list = document.getElementById('requestsList');

        list.innerHTML = '';
        requests.forEach(request => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="fas fa-check-circle"></i> ${request}`;
            list.appendChild(li);
        });

        section.style.display = 'block';
    }
}

// Format Date
function formatDate(date) {
    const options = { month: 'short', day: 'numeric', year: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Copy Reference Number
function copyReference() {
    const reference = document.getElementById('bookingReference').textContent;

    // Copy to clipboard
    if (navigator.clipboard) {
        navigator.clipboard.writeText(reference).then(() => {
            // Show success feedback
            const btn = document.querySelector('.btn-copy');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            btn.style.background = 'white';
            btn.style.color = 'var(--success-green)';

            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.style.background = 'rgba(255, 255, 255, 0.2)';
                btn.style.color = 'white';
            }, 2000);

            console.log('✅ Reference copied:', reference);
        }).catch(err => {
            console.error('Failed to copy:', err);
            alert('Failed to copy reference number');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = reference;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            alert('Reference number copied: ' + reference);
        } catch (err) {
            alert('Failed to copy reference number');
        }
        document.body.removeChild(textArea);
    }
}

// Download Confirmation
function downloadConfirmation() {
    console.log('📥 Downloading confirmation...');

    // In a real app, this would generate a PDF
    // For now, show a message
    alert('Your confirmation will be downloaded as a PDF.\n\nFeature coming soon!');

    // Simulate download
    console.log('✅ Download initiated');
}

// Email Confirmation
function emailConfirmation() {
    console.log('📧 Sending confirmation email...');

    const email = document.getElementById('guestEmail').textContent;

    // Show loading state
    const btn = event.target;
    const originalHTML = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

    // Simulate API call
    setTimeout(() => {
        btn.innerHTML = '<i class="fas fa-check"></i> Sent!';

        setTimeout(() => {
            btn.innerHTML = originalHTML;
            btn.disabled = false;
        }, 2000);

        console.log('✅ Confirmation email sent to:', email);
    }, 1500);
}

// Make functions global
window.copyReference = copyReference;
window.downloadConfirmation = downloadConfirmation;
window.emailConfirmation = emailConfirmation;

console.log('✅ Booking confirmation script loaded!');