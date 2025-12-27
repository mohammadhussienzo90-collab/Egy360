# reviews/web_views.py
"""
Web views for reviews (non-API)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Count

from .models import Review, ReviewHelpful
from .forms import ReviewForm


def get_reviews_for_object(content_object):
    """Get approved reviews for any object"""
    content_type = ContentType.objects.get_for_model(content_object)
    reviews = Review.objects.filter(
        content_type=content_type,
        object_id=content_object.id,
        status='approved'
    ).select_related('user').order_by('-created_at')

    # Calculate stats
    stats = reviews.aggregate(
        avg_rating=Avg('rating'),
        total_count=Count('id'),
        avg_cleanliness=Avg('cleanliness_rating'),
        avg_location=Avg('location_rating'),
        avg_value=Avg('value_rating'),
        avg_service=Avg('service_rating'),
    )

    # Rating distribution
    distribution = {}
    for i in range(1, 6):
        distribution[i] = reviews.filter(rating=i).count()

    return {
        'reviews': reviews,
        'stats': stats,
        'distribution': distribution,
    }


@login_required
def submit_review(request, item_type, item_id):
    """Submit a new review"""
    # Get the item being reviewed
    if item_type == 'accommodation':
        from accommodations.models import Accommodation
        item = get_object_or_404(Accommodation, id=item_id)
        redirect_url = 'accommodations:detail'
        redirect_arg = item.slug
    elif item_type == 'tour':
        from tours.models import Tour
        item = get_object_or_404(Tour, id=item_id)
        redirect_url = 'tours:detail'
        redirect_arg = item.slug
    else:
        messages.error(request, 'Invalid item type.')
        return redirect('home:home')

    content_type = ContentType.objects.get_for_model(item)

    # Check if user already reviewed this item
    existing_review = Review.objects.filter(
        user=request.user,
        content_type=content_type,
        object_id=item_id
    ).first()

    if existing_review:
        messages.warning(request, 'You have already reviewed this item.')
        return redirect(redirect_url, redirect_arg)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.content_type = content_type
            review.object_id = item_id

            # Check for verified booking
            try:
                from bookings.models import Booking
                has_booking = Booking.objects.filter(
                    user=request.user,
                    content_type=content_type,
                    object_id=item_id,
                    status__in=['confirmed', 'completed']
                ).exists()
                review.is_verified_booking = has_booking
            except:
                pass

            review.save()
            messages.success(request, 'Thank you! Your review has been submitted and is pending approval.')
            return redirect(redirect_url, redirect_arg)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'item': item,
        'item_type': item_type,
    }
    return render(request, 'reviews/submit_review.html', context)


@require_POST
@login_required
def vote_helpful(request, review_id):
    """Vote a review as helpful/not helpful (AJAX)"""
    review = get_object_or_404(Review, id=review_id, status='approved')
    is_helpful = request.POST.get('is_helpful', 'true').lower() == 'true'

    # Can't vote on own review
    if review.user == request.user:
        return JsonResponse({
            'success': False,
            'error': 'Cannot vote on your own review'
        }, status=400)

    # Check existing vote
    existing_vote = ReviewHelpful.objects.filter(
        review=review,
        user=request.user
    ).first()

    if existing_vote:
        if existing_vote.is_helpful == is_helpful:
            # Remove vote
            existing_vote.delete()
            message = 'Vote removed'
        else:
            # Change vote
            existing_vote.is_helpful = is_helpful
            existing_vote.save()
            message = 'Vote updated'
    else:
        # New vote
        ReviewHelpful.objects.create(
            review=review,
            user=request.user,
            is_helpful=is_helpful
        )
        message = 'Vote recorded'

    return JsonResponse({
        'success': True,
        'message': message,
        'helpful_count': review.helpful_count,
        'not_helpful_count': review.not_helpful_count,
    })


@require_POST
@login_required
def report_review(request, review_id):
    """Report a review (AJAX)"""
    from .models import ReviewReport

    review = get_object_or_404(Review, id=review_id, status='approved')
    reason = request.POST.get('reason', 'other')
    details = request.POST.get('details', '')

    # Can't report own review
    if review.user == request.user:
        return JsonResponse({
            'success': False,
            'error': 'Cannot report your own review'
        }, status=400)

    # Check if already reported
    existing = ReviewReport.objects.filter(
        review=review,
        reported_by=request.user
    ).exists()

    if existing:
        return JsonResponse({
            'success': False,
            'error': 'You have already reported this review'
        }, status=400)

    ReviewReport.objects.create(
        review=review,
        reported_by=request.user,
        reason=reason,
        details=details
    )

    return JsonResponse({
        'success': True,
        'message': 'Review has been reported for investigation'
    })
