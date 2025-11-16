from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .models import Review, ReviewImage, ReviewResponse, ReviewReport

"""
REVIEWS SERIALIZERS
===================
These serializers handle conversion between:
- Django Review models (Python objects)
- JSON format (API responses)

CRITICAL IMPORTANCE:
Reviews are the TRUST FOUNDATION of Egy360.
- Tourists trust verified reviews more than marketing
- Reviews drive booking decisions
- Reviews protect tourists from scams
- Reviews hold providers accountable

This is where authenticity lives.

Pattern: Includes response handling, flagging, and trust signals
"""


class ReviewImageSerializer(serializers.ModelSerializer):
    """
    Serializer for review images (proof photos)

    WHAT IT DOES:
    - Handles photos tourists upload with reviews
    - Proof that they actually visited
    - Increases review credibility

    WHY IMAGES MATTER:
    - Text review = anyone can write
    - Text + photos = proof of visit
    - Fake reviews usually have no photos
    - Real tourists upload photos

    TRUST SIGNAL:
    - Reviews with images = more trusted
    - Tourists see image count in review
    """

    class Meta:
        model = ReviewImage
        fields = ('id', 'image', 'caption')
        read_only_fields = ('id',)


class ReviewResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for provider responses to reviews

    WHAT IT DOES:
    - Hotel/tour responds to negative review
    - Shows they care about feedback
    - Demonstrates customer service

    TRUST BUILDING:
    - Negative review + no response = bad
    - Negative review + response = good
    - Shows provider is listening
    - Shows provider wants to fix issues

    BUSINESS VALUE:
    - Tourist sees provider cares
    - Converts potential negative to positive
    - Shows professional management
    """

    responder_name = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = ReviewResponse
        fields = (
            'id',
            'responder_name',
            'response_text',
            'is_approved',
            'is_owner',
            'created_at',
        )
        read_only_fields = (
            'id',
            'responder_name',
            'is_owner',
            'created_at',
        )

    def get_responder_name(self, obj):
        """Get responder's name"""
        return obj.responder.get_full_name() or obj.responder.username

    def get_is_owner(self, obj):
        """
        Mark if responder is the property owner

        WHY:
        - Tourists want to know: is this the owner or staff?
        - Owner response = more credible than support staff
        """
        return obj.responder.user_type == 'provider'


class ReviewReportSerializer(serializers.ModelSerializer):
    """
    Serializer for reporting fake/inappropriate reviews

    WHAT IT DOES:
    - Tourist reports suspicious review
    - Marks review for admin investigation
    - Protects platform from fake reviews

    FAKE REVIEW PROTECTION:
    - Competitors post bad reviews (fake)
    - Hotels pay for good reviews (fake)
    - This system catches them
    - Admin investigates flagged reviews

    LEARNING POINT:
    - Trust system requires moderation
    - Community helps moderate
    """

    reporter_name = serializers.SerializerMethodField()

    class Meta:
        model = ReviewReport
        fields = (
            'id',
            'reason',
            'description',
            'reporter_name',
            'is_resolved',
            'created_at',
        )
        read_only_fields = (
            'id',
            'reporter_name',
            'is_resolved',
            'created_at',
        )

    def get_reporter_name(self, obj):
        """Get reporter's name"""
        return obj.reporter.get_full_name() or obj.reporter.username


class ReviewListSerializer(serializers.ModelSerializer):
    """
    List view serializer - reviews in search results

    WHAT IT DOES:
    - Shows review summary for browsing
    - Includes: rating, title, helpful count, verified badge
    - Minimal data for fast loading

    SORT ORDER:
    - Most helpful reviews first (helpful_count desc)
    - Verified purchases first (is_verified_purchase)
    - Recent reviews visible

    LEARNING POINT:
    - Reviews sorted by trust signals
    - Most useful reviews show first
    - Fake reviews (no verification) show lower
    """

    reviewer_name = serializers.SerializerMethodField()
    image_count = serializers.SerializerMethodField()
    has_response = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'rating',
            'reviewer_name',
            'is_verified_purchase',
            'helpful_count',
            'unhelpful_count',
            'image_count',
            'has_response',
            'created_at',
        )
        read_only_fields = (
            'id',
            'reviewer_name',
            'image_count',
            'has_response',
            'created_at',
        )

    def get_reviewer_name(self, obj):
        """Get reviewer's display name"""
        return obj.reviewer.get_full_name() or obj.reviewer.username

    def get_image_count(self, obj):
        """How many photos in this review"""
        return obj.images.count()

    def get_has_response(self, obj):
        """Does provider have response to this review"""
        return hasattr(obj, 'response') and obj.response is not None


class ReviewDetailSerializer(serializers.ModelSerializer):
    """
    Detail view serializer - COMPLETE review information

    WHAT IT DOES:
    - Shows EVERYTHING about a review
    - Includes: full text, images, ratings breakdown, response
    - Tourist reads this to make booking decision

    TRUST SIGNALS:
    - Verified purchase badge
    - Photo count (fake reviews have none)
    - Helpful votes (community trusts it)
    - Response from provider (they care)
    - Specific ratings (cleanliness, comfort, etc)
    - Advantages/disadvantages detail

    PSYCHOLOGICAL FLOW:
    1. See rating (4 stars)
    2. See verified purchase (real person)
    3. See photos (proof)
    4. Read text (details)
    5. See provider response (they care)
    6. Decision: Book or not
    """

    reviewer = serializers.SerializerMethodField()
    images = ReviewImageSerializer(many=True, read_only=True)
    response = ReviewResponseSerializer(read_only=True)
    image_count = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'review_text',
            'rating',
            'reviewer',
            'is_verified_purchase',
            'cleanliness_rating',
            'comfort_rating',
            'location_rating',
            'service_rating',
            'value_for_money_rating',
            'safety_rating',
            'advantages',
            'disadvantages',
            'visit_date',
            'stay_duration_days',
            'helpful_count',
            'unhelpful_count',
            'image_count',
            'images',
            'response',
            'is_approved',
            'created_at',
        )
        read_only_fields = (
            'id',
            'reviewer',
            'image_count',
            'created_at',
        )

    def get_reviewer(self, obj):
        """Get reviewer info (name, profile)"""
        return {
            'id': obj.reviewer.id,
            'name': obj.reviewer.get_full_name() or obj.reviewer.username,
            'profile_picture': obj.reviewer.profile_picture.url if obj.reviewer.profile_picture else None,
        }

    def get_image_count(self, obj):
        """Count images in review"""
        return obj.images.count()


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new reviews

    WHAT IT DOES:
    - Tourist submits review for accommodation/tour/transport
    - Validates review quality
    - Checks for verified purchase

    QUALITY CHECKS:
    - Text must be at least reasonable length
    - Rating between 1-5
    - Optional: detailed ratings (cleanliness, service, etc)
    - Optional: photos

    LEARNING POINT:
    - New reviews start as pending
    - Admin reviews for fake/spam
    - Approved reviews show publicly
    - Fake reviews get rejected
    """

    class Meta:
        model = Review
        fields = (
            'title',
            'review_text',
            'rating',
            'cleanliness_rating',
            'comfort_rating',
            'location_rating',
            'service_rating',
            'value_for_money_rating',
            'safety_rating',
            'advantages',
            'disadvantages',
            'visit_date',
            'stay_duration_days',
        )

    def validate_title(self, value):
        """Title must have minimum length"""
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters")
        return value

    def validate_review_text(self, value):
        """
        Review text must have minimum length

        WHY:
        - Prevents one-word spam reviews
        - Ensures thoughtful feedback
        - Faker reviews are usually very short
        """
        if len(value) < 20:
            raise serializers.ValidationError(
                "Review must be at least 20 characters (be detailed!)"
            )
        return value

    def validate_rating(self, value):
        """Rating must be 1-5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate(self, data):
        """
        Cross-validation: if detailed ratings set, they must be 1-5

        BUSINESS RULE:
        - Detailed ratings optional
        - If provided, must be valid (1-5)
        - Prevents invalid data entry
        """
        optional_ratings = [
            'cleanliness_rating',
            'comfort_rating',
            'location_rating',
            'service_rating',
            'value_for_money_rating',
            'safety_rating',
        ]

        for rating_field in optional_ratings:
            if data.get(rating_field):
                rating = data[rating_field]
                if rating < 1 or rating > 5:
                    raise serializers.ValidationError(
                        f"{rating_field} must be between 1 and 5"
                    )

        return data


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing reviews

    WHAT IT DOES:
    - Tourist can edit their review
    - Can update text, ratings, images
    - Cannot change after certain period (optional business rule)

    BUSINESS LOGIC:
    - Tourist changes mind about rating
    - Wants to add more detail
    - Wants to clarify something
    - System allows edit
    """

    class Meta:
        model = Review
        fields = (
            'title',
            'review_text',
            'rating',
            'cleanliness_rating',
            'comfort_rating',
            'location_rating',
            'service_rating',
            'value_for_money_rating',
            'safety_rating',
            'advantages',
            'disadvantages',
        )


class ReviewHelpfulSerializer(serializers.Serializer):
    """
    Serializer for marking review as helpful/unhelpful

    WHAT IT DOES:
    - Tourist votes if review was helpful
    - Helpful votes shown prominently
    - Most helpful reviews rise to top

    WHY THIS MATTERS:
    - Honest reviews get more votes
    - Fake reviews don't get votes
    - Natural filtering without moderation
    - Community policing

    LEARNING POINT:
    - Not a ModelSerializer (doesn't save to model)
    - Only validates action
    - Then view updates helpful_count
    """

    is_helpful = serializers.BooleanField()

    def validate_is_helpful(self, value):
        """Must be boolean"""
        if not isinstance(value, bool):
            raise serializers.ValidationError("Must be true or false")
        return value


class ReviewVerificationSerializer(serializers.ModelSerializer):
    """
    Serializer for admin verification/moderation

    WHAT IT DOES:
    - Admin reviews flagged reviews
    - Can approve or reject
    - Can flag for fake/spam

    ADMIN-ONLY SERIALIZER:
    - Not exposed to tourists
    - Only staff can access
    - Controls what shows publicly
    """

    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'review_text',
            'rating',
            'reviewer_name',
            'is_verified_purchase',
            'is_approved',
            'is_flagged',
            'flag_reason',
            'helpful_count',
            'unhelpful_count',
            'created_at',
        )
        read_only_fields = (
            'id',
            'reviewer_name',
            'helpful_count',
            'unhelpful_count',
            'created_at',
        )

    def get_reviewer_name(self, obj):
        """Get reviewer name for admin"""
        return obj.reviewer.get_full_name() or obj.reviewer.username