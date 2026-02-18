"""
Itinerary data module for Egy360 Trip Planner.
Contains pre-built itinerary templates, reference data, and generation logic.
Works with or without database data (Railway ephemeral storage compatible).
"""
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# ============================================================
# REFERENCE DATA
# ============================================================

# Travelpayouts city IDs for widget embedding
TP_CITY_IDS = {
    'cairo': 284,
    'luxor': 1026,
    'aswan': 1027,
    'hurghada': 3263,
    'sharm-el-sheikh': 3262,
    'alexandria': 285,
}

# IATA airport codes
AIRPORT_CODES = {
    'cairo': 'CAI',
    'luxor': 'LXR',
    'aswan': 'ASW',
    'hurghada': 'HRG',
    'sharm-el-sheikh': 'SSH',
    'alexandria': 'HBE',
}

# Inter-city transport options
TRANSPORT_BETWEEN = {
    ('cairo', 'luxor'): [
        {'mode': 'flight', 'duration': '1h 10m', 'price_usd': 80, 'notes': 'EgyptAir daily flights'},
        {'mode': 'train', 'duration': '9-10h', 'price_usd': 20, 'notes': 'Sleeper train overnight'},
    ],
    ('cairo', 'aswan'): [
        {'mode': 'flight', 'duration': '1h 30m', 'price_usd': 100, 'notes': 'EgyptAir daily flights'},
        {'mode': 'train', 'duration': '13h', 'price_usd': 25, 'notes': 'Sleeper train overnight'},
    ],
    ('cairo', 'hurghada'): [
        {'mode': 'flight', 'duration': '1h', 'price_usd': 70, 'notes': 'Multiple airlines daily'},
        {'mode': 'bus', 'duration': '5-6h', 'price_usd': 15, 'notes': 'Go Bus or Blue Bus'},
    ],
    ('cairo', 'sharm-el-sheikh'): [
        {'mode': 'flight', 'duration': '1h', 'price_usd': 65, 'notes': 'Multiple airlines daily'},
        {'mode': 'bus', 'duration': '6-7h', 'price_usd': 15, 'notes': 'Go Bus via Suez tunnel'},
    ],
    ('cairo', 'alexandria'): [
        {'mode': 'train', 'duration': '2.5h', 'price_usd': 8, 'notes': 'Frequent trains from Ramses Station'},
        {'mode': 'bus', 'duration': '3h', 'price_usd': 7, 'notes': 'Go Bus every 30 minutes'},
    ],
    ('luxor', 'aswan'): [
        {'mode': 'train', 'duration': '3h', 'price_usd': 8, 'notes': 'Multiple daily trains'},
        {'mode': 'nile_cruise', 'duration': '3-4 days', 'price_usd': 350, 'notes': '5-star Nile cruise with temples'},
    ],
    ('luxor', 'hurghada'): [
        {'mode': 'bus', 'duration': '4h', 'price_usd': 12, 'notes': 'Daily bus service'},
        {'mode': 'car', 'duration': '3.5h', 'price_usd': 50, 'notes': 'Private transfer or rental'},
    ],
    ('hurghada', 'luxor'): [
        {'mode': 'bus', 'duration': '4h', 'price_usd': 12, 'notes': 'Daily bus service'},
        {'mode': 'car', 'duration': '3.5h', 'price_usd': 50, 'notes': 'Private transfer or rental'},
    ],
    ('aswan', 'luxor'): [
        {'mode': 'train', 'duration': '3h', 'price_usd': 8, 'notes': 'Multiple daily trains'},
        {'mode': 'nile_cruise', 'duration': '3-4 days', 'price_usd': 350, 'notes': '5-star Nile cruise with temples'},
    ],
}

# Interest to attraction type mapping
INTEREST_MAPPING = {
    'history': ['archaeological', 'museum', 'historical'],
    'adventure': ['natural', 'diving', 'desert'],
    'culture': ['market', 'cultural', 'religious'],
    'beach': ['beach', 'natural', 'resort'],
    'food': ['market', 'cultural'],
    'diving': ['diving', 'natural', 'marine'],
    'romance': ['resort', 'cruise', 'scenic'],
    'family': ['archaeological', 'museum', 'beach', 'natural'],
}

# Budget ranges (per person per day, USD)
BUDGET_RANGES = {
    'budget': {'min': 30, 'max': 60, 'hotel_stars': '2-3', 'label': 'Budget', 'hotel_type': 'budget'},
    'mid': {'min': 80, 'max': 150, 'hotel_stars': '3-4', 'label': 'Mid-Range', 'hotel_type': 'mid'},
    'luxury': {'min': 200, 'max': 500, 'hotel_stars': '5', 'label': 'Luxury', 'hotel_type': 'luxury'},
}

# City metadata for fallback (when DB is empty)
CITY_DATA = {
    'cairo': {
        'name': 'Cairo',
        'slug': 'cairo',
        'image': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800',
        'description': 'Egypt\'s capital city, home to the Pyramids and rich Islamic heritage.',
        'highlights': ['Pyramids of Giza', 'Egyptian Museum', 'Khan El-Khalili', 'Islamic Cairo'],
    },
    'luxor': {
        'name': 'Luxor',
        'slug': 'luxor',
        'image': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800',
        'description': 'The world\'s greatest open-air museum, ancient Thebes.',
        'highlights': ['Valley of the Kings', 'Karnak Temple', 'Luxor Temple', 'Hatshepsut Temple'],
    },
    'aswan': {
        'name': 'Aswan',
        'slug': 'aswan',
        'image': 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=800',
        'description': 'Egypt\'s sunniest city, gateway to Nubia and Abu Simbel.',
        'highlights': ['Abu Simbel', 'Philae Temple', 'Nubian Village', 'Felucca Sailing'],
    },
    'hurghada': {
        'name': 'Hurghada',
        'slug': 'hurghada',
        'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
        'description': 'Premier Red Sea resort destination with world-class diving.',
        'highlights': ['Giftun Islands', 'Coral Reefs', 'Desert Safari', 'Snorkeling'],
    },
    'sharm-el-sheikh': {
        'name': 'Sharm El Sheikh',
        'slug': 'sharm-el-sheikh',
        'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800',
        'description': 'Sinai Peninsula resort with world-famous diving sites.',
        'highlights': ['Ras Mohammed', 'Naama Bay', 'Tiran Island', 'Mount Sinai'],
    },
    'alexandria': {
        'name': 'Alexandria',
        'slug': 'alexandria',
        'image': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800',
        'description': 'Mediterranean jewel founded by Alexander the Great.',
        'highlights': ['Bibliotheca Alexandrina', 'Catacombs', 'Citadel of Qaitbay', 'Corniche'],
    },
}

# Hotel recommendations per city per budget
HOTEL_RECOMMENDATIONS = {
    'cairo': {
        'budget': {'name': 'Arabian Nights Hotel', 'price': 35, 'stars': 3},
        'mid': {'name': 'Steigenberger Hotel El Tahrir', 'price': 95, 'stars': 4},
        'luxury': {'name': 'Four Seasons Nile Plaza', 'price': 350, 'stars': 5},
    },
    'luxor': {
        'budget': {'name': 'Bob Marley Hostel Luxor', 'price': 20, 'stars': 2},
        'mid': {'name': 'Steigenberger Nile Palace', 'price': 120, 'stars': 5},
        'luxury': {'name': 'Sofitel Winter Palace', 'price': 280, 'stars': 5},
    },
    'aswan': {
        'budget': {'name': 'Keylany Hotel', 'price': 25, 'stars': 3},
        'mid': {'name': 'Tolip Hotel Aswan', 'price': 80, 'stars': 4},
        'luxury': {'name': 'Sofitel Legend Old Cataract', 'price': 320, 'stars': 5},
    },
    'hurghada': {
        'budget': {'name': 'Sea Star Beau Rivage', 'price': 30, 'stars': 3},
        'mid': {'name': 'Sunrise Holidays Resort', 'price': 85, 'stars': 4},
        'luxury': {'name': 'Oberoi Sahl Hasheesh', 'price': 400, 'stars': 5},
    },
    'sharm-el-sheikh': {
        'budget': {'name': 'Shark Bay Oasis Hotel', 'price': 30, 'stars': 3},
        'mid': {'name': 'Sunrise Montemare Resort', 'price': 90, 'stars': 4},
        'luxury': {'name': 'Four Seasons Resort', 'price': 450, 'stars': 5},
    },
    'alexandria': {
        'budget': {'name': 'Cherry Maryski Hotel', 'price': 30, 'stars': 3},
        'mid': {'name': 'Steigenberger Cecil Hotel', 'price': 80, 'stars': 4},
        'luxury': {'name': 'Four Seasons San Stefano', 'price': 250, 'stars': 5},
    },
}

# ============================================================
# PRE-BUILT ITINERARY TEMPLATES
# ============================================================

PRESET_ITINERARIES = {
    'classic-egypt': {
        'name': 'Classic Egypt',
        'slug': 'classic-egypt',
        'duration': 7,
        'destinations': ['cairo', 'luxor', 'aswan'],
        'description': 'The essential Egypt experience: Pyramids, Nile temples, and Nubian culture.',
        'image': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=800',
        'days': [
            {
                'day': 1, 'city': 'cairo', 'title': 'Arrival & Pyramids of Giza',
                'morning': {'activity': 'Arrive at Cairo International Airport, hotel check-in', 'attraction_slug': None},
                'afternoon': {'activity': 'Pyramids of Giza & Great Sphinx', 'attraction_slug': 'pyramids-of-giza'},
                'evening': {'activity': 'Sound & Light Show at the Pyramids', 'attraction_slug': None},
            },
            {
                'day': 2, 'city': 'cairo', 'title': 'Egyptian Museum & Islamic Cairo',
                'morning': {'activity': 'Grand Egyptian Museum (GEM)', 'attraction_slug': 'egyptian-museum'},
                'afternoon': {'activity': 'Islamic Cairo & Al-Muizz Street', 'attraction_slug': None},
                'evening': {'activity': 'Khan El-Khalili Bazaar shopping & dinner', 'attraction_slug': 'khan-el-khalili'},
            },
            {
                'day': 3, 'city': 'cairo', 'title': 'Old Cairo & Travel to Luxor',
                'morning': {'activity': 'Coptic Cairo & Hanging Church', 'attraction_slug': None},
                'afternoon': {'activity': 'Fly to Luxor (1h 10m)', 'attraction_slug': None, 'is_transport': True},
                'evening': {'activity': 'Luxor Temple at sunset', 'attraction_slug': 'luxor-temple'},
            },
            {
                'day': 4, 'city': 'luxor', 'title': 'West Bank Exploration',
                'morning': {'activity': 'Valley of the Kings (3-4 tombs)', 'attraction_slug': 'valley-of-kings'},
                'afternoon': {'activity': 'Temple of Hatshepsut & Colossi of Memnon', 'attraction_slug': None},
                'evening': {'activity': 'Hot air balloon ride at sunrise (book day before)', 'attraction_slug': None},
            },
            {
                'day': 5, 'city': 'luxor', 'title': 'Karnak & Travel to Aswan',
                'morning': {'activity': 'Karnak Temple Complex', 'attraction_slug': 'karnak-temple'},
                'afternoon': {'activity': 'Train to Aswan (3h scenic Nile route)', 'attraction_slug': None, 'is_transport': True},
                'evening': {'activity': 'Aswan Corniche walk & felucca sunset sail', 'attraction_slug': None},
            },
            {
                'day': 6, 'city': 'aswan', 'title': 'Abu Simbel & Philae',
                'morning': {'activity': 'Abu Simbel Temples (early morning trip)', 'attraction_slug': 'abu-simbel'},
                'afternoon': {'activity': 'Philae Temple (Isis Temple)', 'attraction_slug': 'philae-temple'},
                'evening': {'activity': 'Nubian Village dinner experience', 'attraction_slug': None},
            },
            {
                'day': 7, 'city': 'aswan', 'title': 'Aswan Highlights & Departure',
                'morning': {'activity': 'Aswan High Dam & Unfinished Obelisk', 'attraction_slug': None},
                'afternoon': {'activity': 'Souvenir shopping at Aswan Souk', 'attraction_slug': None},
                'evening': {'activity': 'Fly back to Cairo for departure', 'attraction_slug': None, 'is_transport': True},
            },
        ],
    },

    'cairo-weekend': {
        'name': 'Cairo Weekend',
        'slug': 'cairo-weekend',
        'duration': 3,
        'destinations': ['cairo'],
        'description': 'A packed weekend exploring Cairo\'s ancient and modern wonders.',
        'image': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800',
        'days': [
            {
                'day': 1, 'city': 'cairo', 'title': 'Pyramids & Ancient Wonders',
                'morning': {'activity': 'Pyramids of Giza & Great Sphinx', 'attraction_slug': 'pyramids-of-giza'},
                'afternoon': {'activity': 'Grand Egyptian Museum', 'attraction_slug': 'egyptian-museum'},
                'evening': {'activity': 'Dinner cruise on the Nile', 'attraction_slug': None},
            },
            {
                'day': 2, 'city': 'cairo', 'title': 'Islamic & Coptic Cairo',
                'morning': {'activity': 'Coptic Cairo, Hanging Church & Ben Ezra Synagogue', 'attraction_slug': None},
                'afternoon': {'activity': 'Al-Azhar Mosque & Islamic Cairo walking tour', 'attraction_slug': None},
                'evening': {'activity': 'Khan El-Khalili Bazaar & El Fishawy Cafe', 'attraction_slug': 'khan-el-khalili'},
            },
            {
                'day': 3, 'city': 'cairo', 'title': 'Saqqara & Memphis',
                'morning': {'activity': 'Saqqara Step Pyramid & Serapeum', 'attraction_slug': None},
                'afternoon': {'activity': 'Memphis open-air museum', 'attraction_slug': None},
                'evening': {'activity': 'Final shopping & departure', 'attraction_slug': None},
            },
        ],
    },

    'nile-valley': {
        'name': 'Nile Valley Explorer',
        'slug': 'nile-valley',
        'duration': 5,
        'destinations': ['luxor', 'aswan'],
        'description': 'Explore ancient Thebes and sail the Nile to Aswan with temple stops.',
        'image': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800',
        'days': [
            {
                'day': 1, 'city': 'luxor', 'title': 'Arrival & Luxor East Bank',
                'morning': {'activity': 'Arrive in Luxor, hotel check-in', 'attraction_slug': None},
                'afternoon': {'activity': 'Karnak Temple Complex', 'attraction_slug': 'karnak-temple'},
                'evening': {'activity': 'Luxor Temple illuminated visit', 'attraction_slug': 'luxor-temple'},
            },
            {
                'day': 2, 'city': 'luxor', 'title': 'West Bank Full Day',
                'morning': {'activity': 'Hot air balloon at sunrise, then Valley of the Kings', 'attraction_slug': 'valley-of-kings'},
                'afternoon': {'activity': 'Temple of Hatshepsut & Medinet Habu', 'attraction_slug': None},
                'evening': {'activity': 'Board Nile cruise ship', 'attraction_slug': None},
            },
            {
                'day': 3, 'city': 'luxor', 'title': 'Nile Cruise: Edfu Temple',
                'morning': {'activity': 'Sail towards Edfu', 'attraction_slug': None},
                'afternoon': {'activity': 'Edfu Temple (Temple of Horus)', 'attraction_slug': None},
                'evening': {'activity': 'Onboard entertainment & Nubian show', 'attraction_slug': None},
            },
            {
                'day': 4, 'city': 'aswan', 'title': 'Kom Ombo & Aswan',
                'morning': {'activity': 'Kom Ombo Temple (dual temple)', 'attraction_slug': None},
                'afternoon': {'activity': 'Arrive Aswan, Philae Temple', 'attraction_slug': 'philae-temple'},
                'evening': {'activity': 'Felucca sailing around Elephantine Island', 'attraction_slug': None},
            },
            {
                'day': 5, 'city': 'aswan', 'title': 'Abu Simbel & Departure',
                'morning': {'activity': 'Abu Simbel day trip (early start)', 'attraction_slug': 'abu-simbel'},
                'afternoon': {'activity': 'Aswan High Dam & Unfinished Obelisk', 'attraction_slug': None},
                'evening': {'activity': 'Departure from Aswan', 'attraction_slug': None},
            },
        ],
    },

    'red-sea-relaxation': {
        'name': 'Red Sea Relaxation',
        'slug': 'red-sea-relaxation',
        'duration': 5,
        'destinations': ['cairo', 'hurghada'],
        'description': 'Quick Cairo highlights followed by beach paradise on the Red Sea.',
        'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
        'days': [
            {
                'day': 1, 'city': 'cairo', 'title': 'Cairo Highlights',
                'morning': {'activity': 'Pyramids of Giza & Great Sphinx', 'attraction_slug': 'pyramids-of-giza'},
                'afternoon': {'activity': 'Grand Egyptian Museum', 'attraction_slug': 'egyptian-museum'},
                'evening': {'activity': 'Fly to Hurghada (1h)', 'attraction_slug': None, 'is_transport': True},
            },
            {
                'day': 2, 'city': 'hurghada', 'title': 'Red Sea Diving',
                'morning': {'activity': 'Scuba diving or snorkeling trip', 'attraction_slug': 'giftun-islands'},
                'afternoon': {'activity': 'Continue diving at second reef site', 'attraction_slug': 'red-sea-reefs'},
                'evening': {'activity': 'Seafood dinner at marina', 'attraction_slug': None},
            },
            {
                'day': 3, 'city': 'hurghada', 'title': 'Desert Adventure',
                'morning': {'activity': 'Quad biking desert safari', 'attraction_slug': None},
                'afternoon': {'activity': 'Bedouin village visit & camel ride', 'attraction_slug': None},
                'evening': {'activity': 'Stargazing BBQ dinner in desert', 'attraction_slug': None},
            },
            {
                'day': 4, 'city': 'hurghada', 'title': 'Island Paradise',
                'morning': {'activity': 'Giftun Island boat trip', 'attraction_slug': 'giftun-islands'},
                'afternoon': {'activity': 'Beach relaxation & snorkeling', 'attraction_slug': None},
                'evening': {'activity': 'Hurghada Marina walk & shopping', 'attraction_slug': None},
            },
            {
                'day': 5, 'city': 'hurghada', 'title': 'Relaxation & Departure',
                'morning': {'activity': 'Resort pool & spa morning', 'attraction_slug': None},
                'afternoon': {'activity': 'Final beach time & packing', 'attraction_slug': None},
                'evening': {'activity': 'Transfer to airport, departure', 'attraction_slug': None},
            },
        ],
    },

    'egypt-express': {
        'name': 'Egypt Express',
        'slug': 'egypt-express',
        'duration': 4,
        'destinations': ['cairo', 'luxor'],
        'description': 'See Egypt\'s top highlights in just 4 action-packed days.',
        'image': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800',
        'days': [
            {
                'day': 1, 'city': 'cairo', 'title': 'Pyramids & Museum',
                'morning': {'activity': 'Pyramids of Giza & Great Sphinx', 'attraction_slug': 'pyramids-of-giza'},
                'afternoon': {'activity': 'Grand Egyptian Museum', 'attraction_slug': 'egyptian-museum'},
                'evening': {'activity': 'Khan El-Khalili Bazaar & dinner', 'attraction_slug': 'khan-el-khalili'},
            },
            {
                'day': 2, 'city': 'cairo', 'title': 'Cairo Deep Dive & Travel',
                'morning': {'activity': 'Saqqara Step Pyramid & Dahshur', 'attraction_slug': None},
                'afternoon': {'activity': 'Fly to Luxor (1h 10m)', 'attraction_slug': None, 'is_transport': True},
                'evening': {'activity': 'Luxor Temple evening visit', 'attraction_slug': 'luxor-temple'},
            },
            {
                'day': 3, 'city': 'luxor', 'title': 'Valley of the Kings',
                'morning': {'activity': 'Valley of the Kings (3-4 tombs)', 'attraction_slug': 'valley-of-kings'},
                'afternoon': {'activity': 'Temple of Hatshepsut', 'attraction_slug': None},
                'evening': {'activity': 'Karnak Temple at golden hour', 'attraction_slug': 'karnak-temple'},
            },
            {
                'day': 4, 'city': 'luxor', 'title': 'Final Exploration & Departure',
                'morning': {'activity': 'Hot air balloon sunrise ride', 'attraction_slug': None},
                'afternoon': {'activity': 'Luxor Museum & souvenir shopping', 'attraction_slug': None},
                'evening': {'activity': 'Fly to Cairo for departure', 'attraction_slug': None, 'is_transport': True},
            },
        ],
    },

    'complete-egypt': {
        'name': 'Complete Egypt',
        'slug': 'complete-egypt',
        'duration': 10,
        'destinations': ['cairo', 'luxor', 'aswan', 'hurghada'],
        'description': 'The ultimate Egypt trip: history, culture, Nile cruise, and Red Sea beaches.',
        'image': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800',
        'days': [
            {
                'day': 1, 'city': 'cairo', 'title': 'Welcome to Egypt',
                'morning': {'activity': 'Arrive Cairo, hotel check-in & rest', 'attraction_slug': None},
                'afternoon': {'activity': 'Pyramids of Giza & Great Sphinx', 'attraction_slug': 'pyramids-of-giza'},
                'evening': {'activity': 'Sound & Light Show', 'attraction_slug': None},
            },
            {
                'day': 2, 'city': 'cairo', 'title': 'Museums & Markets',
                'morning': {'activity': 'Grand Egyptian Museum', 'attraction_slug': 'egyptian-museum'},
                'afternoon': {'activity': 'Saqqara Step Pyramid', 'attraction_slug': None},
                'evening': {'activity': 'Khan El-Khalili Bazaar & street food', 'attraction_slug': 'khan-el-khalili'},
            },
            {
                'day': 3, 'city': 'cairo', 'title': 'Historic Cairo & Fly South',
                'morning': {'activity': 'Coptic & Islamic Cairo tour', 'attraction_slug': None},
                'afternoon': {'activity': 'Fly to Luxor (1h 10m)', 'attraction_slug': None, 'is_transport': True},
                'evening': {'activity': 'Luxor Temple at sunset', 'attraction_slug': 'luxor-temple'},
            },
            {
                'day': 4, 'city': 'luxor', 'title': 'Luxor West Bank',
                'morning': {'activity': 'Valley of the Kings', 'attraction_slug': 'valley-of-kings'},
                'afternoon': {'activity': 'Temple of Hatshepsut & Medinet Habu', 'attraction_slug': None},
                'evening': {'activity': 'Board Nile cruise ship', 'attraction_slug': None},
            },
            {
                'day': 5, 'city': 'luxor', 'title': 'Karnak & Set Sail',
                'morning': {'activity': 'Karnak Temple Complex', 'attraction_slug': 'karnak-temple'},
                'afternoon': {'activity': 'Cruise departs, sail to Esna Lock', 'attraction_slug': None},
                'evening': {'activity': 'Onboard galabeya party', 'attraction_slug': None},
            },
            {
                'day': 6, 'city': 'aswan', 'title': 'Edfu & Kom Ombo',
                'morning': {'activity': 'Edfu Temple (Temple of Horus)', 'attraction_slug': None},
                'afternoon': {'activity': 'Kom Ombo Temple', 'attraction_slug': None},
                'evening': {'activity': 'Arrive Aswan, Nubian music night', 'attraction_slug': None},
            },
            {
                'day': 7, 'city': 'aswan', 'title': 'Abu Simbel & Aswan',
                'morning': {'activity': 'Abu Simbel day trip', 'attraction_slug': 'abu-simbel'},
                'afternoon': {'activity': 'Philae Temple', 'attraction_slug': 'philae-temple'},
                'evening': {'activity': 'Felucca sunset & Nubian dinner', 'attraction_slug': None},
            },
            {
                'day': 8, 'city': 'aswan', 'title': 'Aswan to Hurghada',
                'morning': {'activity': 'Aswan High Dam & Unfinished Obelisk', 'attraction_slug': None},
                'afternoon': {'activity': 'Fly to Hurghada (via Cairo or direct)', 'attraction_slug': None, 'is_transport': True},
                'evening': {'activity': 'Resort check-in & beach sunset', 'attraction_slug': None},
            },
            {
                'day': 9, 'city': 'hurghada', 'title': 'Red Sea Adventure',
                'morning': {'activity': 'Snorkeling/diving at Giftun Island', 'attraction_slug': 'giftun-islands'},
                'afternoon': {'activity': 'Glass-bottom boat or parasailing', 'attraction_slug': None},
                'evening': {'activity': 'Seafood dinner at marina', 'attraction_slug': None},
            },
            {
                'day': 10, 'city': 'hurghada', 'title': 'Beach Day & Departure',
                'morning': {'activity': 'Beach & pool relaxation', 'attraction_slug': None},
                'afternoon': {'activity': 'Last swim & packing', 'attraction_slug': None},
                'evening': {'activity': 'Transfer to airport, departure', 'attraction_slug': None},
            },
        ],
    },
}

# Per-city day blocks for custom itinerary assembly
CITY_DAY_BLOCKS = {
    'cairo': [
        {
            'title': 'Pyramids & Ancient Wonders',
            'morning': {'activity': 'Pyramids of Giza & Great Sphinx', 'attraction_slug': 'pyramids-of-giza'},
            'afternoon': {'activity': 'Grand Egyptian Museum', 'attraction_slug': 'egyptian-museum'},
            'evening': {'activity': 'Sound & Light Show at the Pyramids', 'attraction_slug': None},
        },
        {
            'title': 'Islamic & Coptic Heritage',
            'morning': {'activity': 'Coptic Cairo & Hanging Church', 'attraction_slug': None},
            'afternoon': {'activity': 'Al-Azhar Mosque & Islamic Cairo', 'attraction_slug': None},
            'evening': {'activity': 'Khan El-Khalili Bazaar & dinner', 'attraction_slug': 'khan-el-khalili'},
        },
        {
            'title': 'Saqqara & Memphis',
            'morning': {'activity': 'Saqqara Step Pyramid complex', 'attraction_slug': None},
            'afternoon': {'activity': 'Memphis & Dahshur Bent Pyramid', 'attraction_slug': None},
            'evening': {'activity': 'Nile dinner cruise', 'attraction_slug': None},
        },
    ],
    'luxor': [
        {
            'title': 'Valley of the Kings & West Bank',
            'morning': {'activity': 'Valley of the Kings (3-4 tombs)', 'attraction_slug': 'valley-of-kings'},
            'afternoon': {'activity': 'Temple of Hatshepsut & Colossi of Memnon', 'attraction_slug': None},
            'evening': {'activity': 'Luxor Temple evening visit', 'attraction_slug': 'luxor-temple'},
        },
        {
            'title': 'Karnak & East Bank',
            'morning': {'activity': 'Karnak Temple Complex', 'attraction_slug': 'karnak-temple'},
            'afternoon': {'activity': 'Luxor Museum', 'attraction_slug': None},
            'evening': {'activity': 'Felucca ride on the Nile', 'attraction_slug': None},
        },
    ],
    'aswan': [
        {
            'title': 'Abu Simbel & Philae',
            'morning': {'activity': 'Abu Simbel Temples (early trip)', 'attraction_slug': 'abu-simbel'},
            'afternoon': {'activity': 'Philae Temple', 'attraction_slug': 'philae-temple'},
            'evening': {'activity': 'Nubian Village dinner', 'attraction_slug': None},
        },
        {
            'title': 'Aswan Highlights',
            'morning': {'activity': 'Aswan High Dam & Unfinished Obelisk', 'attraction_slug': None},
            'afternoon': {'activity': 'Elephantine Island & botanical garden', 'attraction_slug': None},
            'evening': {'activity': 'Felucca sunset sailing', 'attraction_slug': None},
        },
    ],
    'hurghada': [
        {
            'title': 'Red Sea Diving Day',
            'morning': {'activity': 'Boat trip to Giftun Islands', 'attraction_slug': 'giftun-islands'},
            'afternoon': {'activity': 'Snorkeling at coral reefs', 'attraction_slug': 'red-sea-reefs'},
            'evening': {'activity': 'Seafood dinner at marina', 'attraction_slug': None},
        },
        {
            'title': 'Desert & Beach',
            'morning': {'activity': 'Quad biking desert safari', 'attraction_slug': None},
            'afternoon': {'activity': 'Beach relaxation & water sports', 'attraction_slug': None},
            'evening': {'activity': 'Hurghada Marina walk', 'attraction_slug': None},
        },
    ],
    'sharm-el-sheikh': [
        {
            'title': 'Ras Mohammed & Diving',
            'morning': {'activity': 'Ras Mohammed National Park', 'attraction_slug': 'ras-mohammed'},
            'afternoon': {'activity': 'Snorkeling at coral walls', 'attraction_slug': None},
            'evening': {'activity': 'Naama Bay nightlife', 'attraction_slug': 'naama-bay'},
        },
        {
            'title': 'Tiran Island & Relaxation',
            'morning': {'activity': 'Boat trip to Tiran Island', 'attraction_slug': None},
            'afternoon': {'activity': 'Beach relaxation & spa', 'attraction_slug': None},
            'evening': {'activity': 'Old Market shopping & dinner', 'attraction_slug': None},
        },
    ],
    'alexandria': [
        {
            'title': 'Alexandria Highlights',
            'morning': {'activity': 'Bibliotheca Alexandrina', 'attraction_slug': 'bibliotheca-alexandrina'},
            'afternoon': {'activity': 'Catacombs & Citadel of Qaitbay', 'attraction_slug': 'catacombs-kom-el-shoqafa'},
            'evening': {'activity': 'Corniche walk & seafood dinner', 'attraction_slug': None},
        },
    ],
}


# ============================================================
# CORE FUNCTIONS
# ============================================================

def generate_itinerary(destinations, duration, interests=None, budget='mid',
                       travelers=2, travel_dates=None):
    """
    Generate an itinerary based on user selections.
    First tries to match a preset template, then assembles from city day blocks.
    """
    interests = interests or ['history']
    destinations = [d.lower().strip() for d in destinations if d]

    # Try to match a preset
    matched_preset = _match_preset(destinations, duration)
    if matched_preset:
        days = matched_preset['days']
    else:
        days = _assemble_custom_itinerary(destinations, duration)

    # Calculate cost estimate
    budget_info = BUDGET_RANGES.get(budget, BUDGET_RANGES['mid'])
    avg_daily = (budget_info['min'] + budget_info['max']) / 2
    total_estimate = avg_daily * duration * travelers

    # Build hotel recommendations per city
    hotels = {}
    cities_in_trip = list(dict.fromkeys(d.get('city', '') for d in days))
    for city_slug in cities_in_trip:
        if city_slug in HOTEL_RECOMMENDATIONS:
            hotels[city_slug] = HOTEL_RECOMMENDATIONS[city_slug].get(
                budget, HOTEL_RECOMMENDATIONS[city_slug]['mid']
            )

    # Build transport info for city transitions
    transport_info = []
    prev_city = None
    for day in days:
        curr_city = day.get('city', '')
        if prev_city and curr_city != prev_city:
            key = (prev_city, curr_city)
            rev_key = (curr_city, prev_city)
            routes = TRANSPORT_BETWEEN.get(key) or TRANSPORT_BETWEEN.get(rev_key, [])
            if routes:
                transport_info.append({
                    'from_city': prev_city,
                    'to_city': curr_city,
                    'options': routes,
                    'day': day['day'],
                })
        prev_city = curr_city

    # Build widget configs per city
    widget_configs = {}
    for city_slug in cities_in_trip:
        widget_configs[city_slug] = get_affiliate_config(city_slug)

    # Build summary
    city_names = [CITY_DATA.get(c, {}).get('name', c.title()) for c in cities_in_trip]
    summary = {
        'destinations': city_names,
        'destination_slugs': cities_in_trip,
        'duration': duration,
        'budget_level': budget,
        'budget_label': budget_info['label'],
        'travelers': travelers,
        'total_estimate': round(total_estimate),
        'daily_estimate': round(avg_daily),
        'currency': 'USD',
    }

    # Add travel dates if provided
    if travel_dates:
        summary['travel_dates'] = travel_dates

    # Enrich with DB data
    days = enrich_with_db_data(days)

    return {
        'days': days,
        'summary': summary,
        'hotels': hotels,
        'transport': transport_info,
        'widget_configs': widget_configs,
    }


def _match_preset(destinations, duration):
    """Try to find a preset itinerary that matches the selections."""
    dest_set = set(destinations)
    best_match = None
    best_score = 0

    for key, preset in PRESET_ITINERARIES.items():
        preset_dests = set(preset['destinations'])
        # Check destination overlap
        overlap = len(dest_set & preset_dests)
        if overlap == 0:
            continue
        # Score: overlap ratio + duration proximity
        dest_score = overlap / max(len(dest_set), len(preset_dests))
        dur_diff = abs(preset['duration'] - duration)
        dur_score = max(0, 1 - dur_diff / 5)
        score = dest_score * 0.7 + dur_score * 0.3

        if score > best_score:
            best_score = score
            best_match = preset

    if best_match and best_score >= 0.5:
        # Adjust days to match requested duration
        days = list(best_match['days'])
        if len(days) > duration:
            days = days[:duration]
        elif len(days) < duration:
            # Pad with extra days from last city
            last_city = days[-1]['city']
            city_blocks = CITY_DAY_BLOCKS.get(last_city, [])
            block_idx = 0
            while len(days) < duration:
                block = city_blocks[block_idx % len(city_blocks)] if city_blocks else {
                    'title': 'Free Day',
                    'morning': {'activity': 'Explore at leisure', 'attraction_slug': None},
                    'afternoon': {'activity': 'Free time', 'attraction_slug': None},
                    'evening': {'activity': 'Dinner & relaxation', 'attraction_slug': None},
                }
                new_day = {
                    'day': len(days) + 1,
                    'city': last_city,
                    **{k: v for k, v in block.items() if k != 'day'},
                }
                days.append(new_day)
                block_idx += 1

        # Re-number days
        for i, day in enumerate(days):
            day['day'] = i + 1

        return {'days': days}
    return None


def _assemble_custom_itinerary(destinations, duration):
    """Assemble a custom itinerary from per-city day blocks."""
    if not destinations:
        destinations = ['cairo']

    # Allocate days per city
    days_per_city = {}
    base_days = max(1, duration // len(destinations))
    remainder = duration - base_days * len(destinations)

    for i, city in enumerate(destinations):
        days_per_city[city] = base_days + (1 if i < remainder else 0)

    # Build day list
    days = []
    day_num = 1
    for city in destinations:
        city_blocks = CITY_DAY_BLOCKS.get(city, [])
        allocated = days_per_city[city]

        for d in range(allocated):
            if city_blocks:
                block = city_blocks[d % len(city_blocks)]
            else:
                block = {
                    'title': f'Exploring {CITY_DATA.get(city, {}).get("name", city.title())}',
                    'morning': {'activity': 'Morning sightseeing', 'attraction_slug': None},
                    'afternoon': {'activity': 'Afternoon exploration', 'attraction_slug': None},
                    'evening': {'activity': 'Evening entertainment', 'attraction_slug': None},
                }
            day_entry = {
                'day': day_num,
                'city': city,
                **{k: v for k, v in block.items()},
            }
            days.append(day_entry)
            day_num += 1

    return days


def enrich_with_db_data(days):
    """
    Enrich itinerary days with real database data when available.
    Gracefully falls back to static data if DB is empty or unavailable.
    """
    try:
        from destinations.models import Attraction
        attractions_by_slug = {}
        slugs = set()
        for day in days:
            for period in ['morning', 'afternoon', 'evening']:
                slot = day.get(period, {})
                if slot and slot.get('attraction_slug'):
                    slugs.add(slot['attraction_slug'])

        if slugs:
            for attr in Attraction.objects.filter(slug__in=slugs).select_related('city'):
                attractions_by_slug[attr.slug] = {
                    'name': attr.name,
                    'slug': attr.slug,
                    'description': attr.description[:200] if attr.description else '',
                    'image_url': getattr(attr, 'image_url', ''),
                    'attraction_type': getattr(attr, 'attraction_type', ''),
                    'city': attr.city.name if attr.city else '',
                    'is_unesco': getattr(attr, 'is_unesco', False),
                }

        # Enrich each day
        for day in days:
            for period in ['morning', 'afternoon', 'evening']:
                slot = day.get(period, {})
                if slot and slot.get('attraction_slug'):
                    db_data = attractions_by_slug.get(slot['attraction_slug'])
                    if db_data:
                        slot['attraction_data'] = db_data

    except Exception as e:
        logger.debug(f"Could not enrich itinerary with DB data: {e}")

    return days


def get_affiliate_config(city_slug, program=None):
    """Return Travelpayouts widget params for a city and program."""
    tp_id = TP_CITY_IDS.get(city_slug, 284)
    airport = AIRPORT_CODES.get(city_slug, 'CAI')
    city_name = CITY_DATA.get(city_slug, {}).get('name', city_slug.title())

    config = {
        'city_id': tp_id,
        'airport_code': airport,
        'city_name': city_name,
        'city_slug': city_slug,
        'shmarker': '688198',
        'trs': '477897',
        'programs': {
            'flights': {
                'campaign_id': 100,
                'promo_id': 4504,
                'widget_url': f'https://tp.media/content?currency=usd&trs=477897&shmarker=688198&searchTypeFlights=true&destination={airport}&destination_label={city_name}%20({airport})&lang=en&powered_by=true&promo_id=4504&campaign_id=100',
            },
            'hotels': {
                'campaign_id': 101,
                'promo_id': 4505,
                'widget_url': f'https://tp.media/content?currency=usd&trs=477897&shmarker=688198&searchTypeHotels=true&city={tp_id}&city_label={city_name}%2C%20Egypt&lang=en&powered_by=true&promo_id=4505&campaign_id=101',
            },
            'tours': {
                'campaign_id': 137,
                'promo_id': 4497,
                'widget_url': f'https://tpemd.com/content?currency=USD&trs=477897&shmarker=688198&locale=en&city_id={tp_id}&category=4&amount=3&powered_by=true&campaign_id=137&promo_id=4497',
            },
            'car_rental': {
                'campaign_id': 102,
                'promo_id': 4506,
                'widget_url': f'https://tp.media/content?currency=usd&trs=477897&shmarker=688198&searchTypeCars=true&location_name={city_name}%2C%20Egypt&lang=en&powered_by=true&promo_id=4506&campaign_id=102',
            },
            'insurance': {
                'campaign_id': 104,
                'promo_id': 4508,
                'click_url': 'https://tp.media/click?shmarker=688198&promo_id=4508&source_type=banner&type=click&campaign_id=104&trs=477897',
            },
        },
    }

    if program and program in config['programs']:
        return config['programs'][program]
    return config


def get_cities_for_form():
    """Get city list for the wizard form, with DB fallback."""
    cities = []
    try:
        from destinations.models import City
        db_cities = City.objects.filter(is_popular=True).order_by('name')
        if db_cities.exists():
            for city in db_cities:
                slug = city.slug
                cities.append({
                    'name': city.name,
                    'slug': slug,
                    'image': getattr(city, 'image_url', '') or CITY_DATA.get(slug, {}).get('image', ''),
                    'description': city.description[:100] if city.description else '',
                    'has_airport': getattr(city, 'has_airport', True),
                })
            return cities
    except Exception as e:
        logger.debug(f"Could not load cities from DB: {e}")

    # Fallback to static data
    for slug, data in CITY_DATA.items():
        cities.append({
            'name': data['name'],
            'slug': slug,
            'image': data['image'],
            'description': data['description'][:100],
            'has_airport': True,
        })
    return cities
