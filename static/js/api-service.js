/* =========================================
   EGY360 - API Service Layer
   Matches Your Django Backend Filters
   ========================================= */

class APIService {
    constructor() {
        this.baseURL = API_CONFIG.API_BASE;
    }

    // Generic API call
    async apiCall(endpoint, options = {}) {
        const url = this.baseURL + endpoint;
        const defaultOptions = {
            headers: API_CONFIG.getHeaders(),
            credentials: 'include',
        };

        const finalOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, finalOptions);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // === ACCOMMODATIONS ===

    // Search accommodations (matches your views.py filters exactly)
    async searchAccommodations(params = {}) {
        const queryParams = new URLSearchParams();

        // Filters from your views.py
        if (params.city_name) queryParams.append('city_name', params.city_name);
        if (params.min_price) queryParams.append('min_price', params.min_price);
        if (params.max_price) queryParams.append('max_price', params.max_price);
        if (params.min_rating) queryParams.append('min_rating', params.min_rating);
        if (params.star_rating) queryParams.append('star_rating', params.star_rating);
        if (params.accommodation_type) queryParams.append('accommodation_type', params.accommodation_type);
        if (params.is_verified) queryParams.append('is_verified', params.is_verified);
        if (params.is_safe) queryParams.append('is_safe', params.is_safe);
        if (params.amenities) queryParams.append('amenities', params.amenities); // comma-separated
        if (params.check_in) queryParams.append('check_in', params.check_in);
        if (params.check_out) queryParams.append('check_out', params.check_out);
        if (params.guests) queryParams.append('guests', params.guests);
        if (params.page) queryParams.append('page', params.page);

        const endpoint = `/accommodations/search/?${queryParams.toString()}`;
        return await this.apiCall(endpoint);
    }

    // Get accommodation detail
    async getAccommodationDetail(id) {
        return await this.apiCall(`/accommodations/${id}/`);
    }

    // Get featured accommodations
    async getFeaturedAccommodations() {
        return await this.apiCall('/accommodations/featured/');
    }

    // Get verified accommodations
    async getVerifiedAccommodations(page = 1) {
        return await this.apiCall(`/accommodations/verified/?page=${page}`);
    }

    // Get nearby accommodations
    async getNearbyAccommodations(lat, lng, radius = 5) {
        return await this.apiCall(`/accommodations/nearby/?lat=${lat}&lng=${lng}&radius=${radius}`);
    }

    // Check availability
    async checkAvailability(id, checkIn, checkOut) {
        return await this.apiCall(`/accommodations/${id}/availability/?check_in=${checkIn}&check_out=${checkOut}`);
    }

    // Get accommodation rooms
    async getAccommodationRooms(id) {
        return await this.apiCall(`/accommodations/${id}/rooms/`);
    }

    // Get accommodation images
    async getAccommodationImages(id) {
        return await this.apiCall(`/accommodations/${id}/images/`);
    }

    // === TYPES & AMENITIES ===

    async getAccommodationTypes() {
        return await this.apiCall('/accommodation-types/');
    }

    async getAmenities() {
        return await this.apiCall('/amenities/');
    }

    // === ROOMS ===

    async getAvailableRooms() {
        return await this.apiCall('/rooms/available/');
    }

    async getRoomsByAccommodation(accommodationId) {
        return await this.apiCall(`/rooms/by_accommodation/?accommodation_id=${accommodationId}`);
    }
}

// Create global instance
window.EgyAPI = new APIService();
console.log('✅ API Service initialized');