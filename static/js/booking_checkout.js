/* =========================================
   EGY360 - Booking Checkout Script
   Handles booking flow, calculations, validation
   ========================================= */

// Mock booking data
let bookingData = {
    type: 'accommodation', // or 'tour'
    id: 1,
    name: 'Cairo Pyramids Hotel',
    location: 'Giza, Cairo',
    image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400',
    rating: 4.8,
    reviewCount: 324,
    basePrice: 1200, // per night or per person
    serviceFeePercent: 10,
    taxPercent: 15
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('📝 Initializing booking checkout...');
    loadBookingData();
    setupEventListeners();
    setMinimumDates();
    calculatePrice();
});

// Load Booking Data
function loadBookingData() {
    // Get booking type and ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const type = urlParams.get('type') || 'accommodation';
    const id = urlParams.get('id') || '1';

    bookingData.type = type;
    bookingData.id = id;

    // Update property info in summary
    document.getElementById('summaryTitle').textContent = bookingData.name;
    document.getElementById('summaryLocation').innerHTML = `<i class="fas fa-map-marker-alt"></i> ${bookingData.location}`;
    document.getElementById('summaryImage').src = bookingData.image;

    // Mobile summary
    if (document.getElementById('mobileSummaryTitle')) {
        document.getElementById('mobileSummaryTitle').textContent = bookingData.name;
        document.getElementById('mobileSummaryLocation').innerHTML = `<i class="fas fa-map-marker-alt"></i> ${bookingData.location}`;
        document.getElementById('mobileSummaryImage').src = bookingData.image;
    }

    // Show/hide fields based on type
    if (type === 'tour') {
        document.getElementById('accommodationDates').style.display = 'none';
        document.getElementById('accommodationDatesOut').style.display = 'none';
        document.getElementById('roomSelection').style.display = 'none';
        document.getElementById('tourDate').style.display = 'block';
    }

    console.log('✅ Booking data loaded:', bookingData);
}

// Setup Event Listeners
function setupEventListeners() {
    // Date changes
    const checkInDate = document.getElementById('checkInDate');
    const checkOutDate = document.getElementById('checkOutDate');
    const tourDateInput = document.getElementById('tourDateInput');

    if (checkInDate) checkInDate.addEventListener('change', calculatePrice);
    if (checkOutDate) checkOutDate.addEventListener('change', calculatePrice);
    if (tourDateInput) tourDateInput.addEventListener('change', calculatePrice);

    // Guest count change
    document.getElementById('guestCount').addEventListener('change', calculatePrice);

    // Room type change
    const roomType = document.getElementById('roomType');
    if (roomType) {
        roomType.addEventListener('change', function() {
            const selected = this.options[this.selectedIndex];
            const priceMatch = selected.text.match(/(\d+,?\d*)\s*EGP/);
            if (priceMatch) {
                bookingData.basePrice = parseInt(priceMatch[1].replace(',', ''));
                calculatePrice();
            }
        });
    }

    // Payment method toggle
    const paymentMethods = document.querySelectorAll('input[name="paymentMethod"]');
    paymentMethods.forEach(method => {
        method.addEventListener('change', function() {
            const cardForm = document.getElementById('cardForm');
            if (this.value === 'card') {
                cardForm.style.display = 'block';
            } else {
                cardForm.style.display = 'none';
            }
        });
    });

    // Card number formatting
    const cardNumber = document.getElementById('cardNumber');
    if (cardNumber) {
        cardNumber.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s/g, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            e.target.value = formattedValue;
        });
    }

    // Expiry date formatting
    const cardExpiry = document.getElementById('cardExpiry');
    if (cardExpiry) {
        cardExpiry.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.slice(0, 2) + '/' + value.slice(2, 4);
            }
            e.target.value = value;
        });
    }

    // CVV - numbers only
    const cardCvv = document.getElementById('cardCvv');
    if (cardCvv) {
        cardCvv.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, '');
        });
    }

    console.log('✅ Event listeners set up');
}

// Set Minimum Dates
function setMinimumDates() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const todayStr = today.toISOString().split('T')[0];
    const tomorrowStr = tomorrow.toISOString().split('T')[0];

    const checkInDate = document.getElementById('checkInDate');
    const checkOutDate = document.getElementById('checkOutDate');
    const tourDateInput = document.getElementById('tourDateInput');

    if (checkInDate) {
        checkInDate.min = todayStr;
        checkInDate.value = todayStr;
    }

    if (checkOutDate) {
        checkOutDate.min = tomorrowStr;
        checkOutDate.value = tomorrowStr;
    }

    if (tourDateInput) {
        tourDateInput.min = todayStr;
        tourDateInput.value = todayStr;
    }
}

// Calculate Price
function calculatePrice() {
    let subtotal = 0;
    let nights = 0;
    let guests = parseInt(document.getElementById('guestCount').value) || 1;

    if (bookingData.type === 'accommodation') {
        // Calculate nights
        const checkIn = new Date(document.getElementById('checkInDate').value);
        const checkOut = new Date(document.getElementById('checkOutDate').value);

        if (checkIn && checkOut && checkOut > checkIn) {
            nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
            subtotal = bookingData.basePrice * nights;

            // Update nights display
            document.getElementById('nightsCount').textContent = `${nights} night${nights !== 1 ? 's' : ''}`;
            document.getElementById('nightsDisplay').style.display = 'flex';

            // Update price label
            document.getElementById('priceLabel').textContent = `${bookingData.basePrice.toLocaleString()} EGP × ${nights} night${nights !== 1 ? 's' : ''}`;
        } else {
            document.getElementById('nightsDisplay').style.display = 'none';
            document.getElementById('priceLabel').textContent = 'Select dates';
        }
    } else {
        // Tour pricing (per person)
        subtotal = bookingData.basePrice * guests;
        document.getElementById('priceLabel').textContent = `${bookingData.basePrice.toLocaleString()} EGP × ${guests} guest${guests !== 1 ? 's' : ''}`;
        document.getElementById('nightsDisplay').style.display = 'none';
    }

    // Calculate fees
    const serviceFee = Math.round(subtotal * (bookingData.serviceFeePercent / 100));
    const taxes = Math.round(subtotal * (bookingData.taxPercent / 100));
    const total = subtotal + serviceFee + taxes;

    // Update price breakdown
    document.getElementById('priceAmount').textContent = `${subtotal.toLocaleString()} EGP`;
    document.getElementById('serviceFee').textContent = `${serviceFee.toLocaleString()} EGP`;
    document.getElementById('taxes').textContent = `${taxes.toLocaleString()} EGP`;
    document.getElementById('totalPrice').textContent = `${total.toLocaleString()} EGP`;

    console.log('💰 Price calculated:', { subtotal, serviceFee, taxes, total });
}

// Complete Booking
function completeBooking() {
    console.log('🔄 Processing booking...');

    // Validate form
    if (!validateForm()) {
        console.log('❌ Form validation failed');
        return;
    }

    // Show loading state
    const bookBtn = document.getElementById('bookNowBtn');
    const originalHTML = bookBtn.innerHTML;
    bookBtn.disabled = true;
    bookBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

    // Collect booking data
    const booking = {
        type: bookingData.type,
        propertyId: bookingData.id,
        propertyName: bookingData.name,

        // Dates
        checkIn: document.getElementById('checkInDate')?.value,
        checkOut: document.getElementById('checkOutDate')?.value,
        tourDate: document.getElementById('tourDateInput')?.value,

        // Guests
        guests: document.getElementById('guestCount').value,
        roomType: document.getElementById('roomType')?.value,

        // Guest info
        firstName: document.getElementById('firstName').value,
        lastName: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        country: document.getElementById('country').value,

        // Special requests
        earlyCheckin: document.getElementById('earlyCheckin').checked,
        lateCheckout: document.getElementById('lateCheckout').checked,
        airportPickup: document.getElementById('airportPickup').checked,
        nonSmoking: document.getElementById('nonSmoking').checked,
        additionalRequests: document.getElementById('additionalRequests').value,

        // Payment
        paymentMethod: document.querySelector('input[name="paymentMethod"]:checked').value,

        // Price
        total: document.getElementById('totalPrice').textContent,

        // Timestamp
        bookingDate: new Date().toISOString()
    };

    // Simulate API call
    setTimeout(() => {
        console.log('✅ Booking completed:', booking);

        // Store booking in sessionStorage
        const bookingId = 'BK' + Date.now().toString().slice(-8);
        sessionStorage.setItem('latestBooking', JSON.stringify({
            ...booking,
            bookingId: bookingId,
            status: 'confirmed'
        }));

        // Redirect to confirmation page
        window.location.href = `/booking/confirmation/?id=${bookingId}`;
    }, 2000);
}

// Validate Form
function validateForm() {
    let isValid = true;
    const errors = [];

    // Check dates
    if (bookingData.type === 'accommodation') {
        const checkIn = document.getElementById('checkInDate').value;
        const checkOut = document.getElementById('checkOutDate').value;

        if (!checkIn || !checkOut) {
            errors.push('Please select check-in and check-out dates');
            isValid = false;
        } else if (new Date(checkOut) <= new Date(checkIn)) {
            errors.push('Check-out date must be after check-in date');
            isValid = false;
        }
    } else {
        const tourDate = document.getElementById('tourDateInput').value;
        if (!tourDate) {
            errors.push('Please select a tour date');
            isValid = false;
        }
    }

    // Check guest info
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const country = document.getElementById('country').value;

    if (!firstName) {
        errors.push('First name is required');
        isValid = false;
    }

    if (!lastName) {
        errors.push('Last name is required');
        isValid = false;
    }

    if (!email) {
        errors.push('Email is required');
        isValid = false;
    } else if (!isValidEmail(email)) {
        errors.push('Please enter a valid email address');
        isValid = false;
    }

    if (!phone) {
        errors.push('Phone number is required');
        isValid = false;
    }

    if (!country) {
        errors.push('Please select your country');
        isValid = false;
    }

    // Check payment method
    const paymentMethod = document.querySelector('input[name="paymentMethod"]:checked').value;
    if (paymentMethod === 'card') {
        const cardName = document.getElementById('cardName').value.trim();
        const cardNumber = document.getElementById('cardNumber').value.replace(/\s/g, '');
        const cardExpiry = document.getElementById('cardExpiry').value;
        const cardCvv = document.getElementById('cardCvv').value;

        if (!cardName) {
            errors.push('Cardholder name is required');
            isValid = false;
        }

        if (!cardNumber || cardNumber.length < 13) {
            errors.push('Please enter a valid card number');
            isValid = false;
        }

        if (!cardExpiry || cardExpiry.length !== 5) {
            errors.push('Please enter card expiry date (MM/YY)');
            isValid = false;
        }

        if (!cardCvv || cardCvv.length < 3) {
            errors.push('Please enter card CVV');
            isValid = false;
        }
    }

    // Check terms agreement
    if (!document.getElementById('agreeTerms').checked) {
        errors.push('You must agree to the Terms & Conditions');
        isValid = false;
    }

    // Show errors if any
    if (!isValid) {
        alert('Please fix the following errors:\n\n' + errors.join('\n'));
    }

    return isValid;
}

// Email Validation
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Make function global
window.completeBooking = completeBooking;

console.log('✅ Booking checkout script loaded!');