from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.utils import timezone
from .models import BlogPost, BlogCategory, BlogComment
import traceback


def debug_blog(request):
    """Debug endpoint to test blog functionality"""
    try:
        total = BlogPost.objects.count()
        published = BlogPost.objects.filter(status='published').count()
        categories = BlogCategory.objects.count()
        posts = list(BlogPost.objects.filter(status='published').values('title', 'slug')[:5])
        return JsonResponse({
            'status': 'ok',
            'total_posts': total,
            'published_posts': published,
            'categories': categories,
            'sample_posts': posts
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


def seed_pyramid_articles(request):
    """
    Seed the 9 Great Pyramid articles.
    Access via: /blog/seed-pyramids/?key=egy360seed
    """
    # Simple security check
    if request.GET.get('key') != 'egy360seed':
        return JsonResponse({'error': 'Invalid key'}, status=403)

    from django.contrib.auth.models import User

    # Get or create category
    category, _ = BlogCategory.objects.get_or_create(
        slug='ancient-egypt',
        defaults={'name': 'Ancient Egypt', 'description': 'Explore the wonders of Ancient Egypt'}
    )

    # Get author
    author = User.objects.filter(is_superuser=True).first()
    if not author:
        author = User.objects.first()
    if not author:
        return JsonResponse({'error': 'No users found'}, status=500)

    now = timezone.now()

    articles = [
        {
            'title': 'The Great Pyramid of Giza: 4,500 Years of Mystery and Marvel',
            'slug': 'great-pyramid-giza-introduction',
            'excerpt': 'Discover the mind-blowing facts about the Great Pyramid of Giza - the only surviving Wonder of the Ancient World.',
            'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=1200&q=80',
            'is_featured': True,
        },
        {
            'title': 'Building the Great Pyramid: Timeline, Workers, and the 20-Year Challenge',
            'slug': 'great-pyramid-history-timeline-workers',
            'excerpt': 'How long did it take to build the Great Pyramid? Who were the workers? Explore the complete timeline.',
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': "The Architecture of the Great Pyramid: Precision That Shouldn't Exist",
            'slug': 'great-pyramid-architecture-precision',
            'excerpt': "The Great Pyramid's precision rivals modern engineering - 99.98% symmetrical, aligned to true north.",
            'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': "The King's Chamber: Heart of the Great Pyramid",
            'slug': 'great-pyramid-kings-chamber-secrets',
            'excerpt': "Deep inside the Great Pyramid lies the King's Chamber - built of granite from 800km away.",
            'image_url': 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': 'How Was the Great Pyramid Built? Construction Methods Explained',
            'slug': 'great-pyramid-construction-methods',
            'excerpt': "No wheels, no cranes, no iron - how did ancient Egyptians build the Great Pyramid?",
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': 'Cutting Pyramid Stones: How Did They Do It With Copper Tools?',
            'slug': 'great-pyramid-stone-cutting',
            'excerpt': "The Great Pyramid's stones are cut so precisely you can't fit paper between them.",
            'image_url': 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': 'Moving Pyramid Stones: Transporting 2.3 Million Blocks Without Wheels',
            'slug': 'great-pyramid-transporting-stones',
            'excerpt': "How did the Egyptians move 80-ton blocks 800 kilometers without trucks or cranes?",
            'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': 'Great Pyramid Myths Debunked: Aliens, Slaves, and Misconceptions',
            'slug': 'great-pyramid-myths-debunked',
            'excerpt': "Aliens didn't build the pyramids. Slaves didn't either. Let's debunk the myths.",
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200&q=80',
            'is_featured': False,
        },
        {
            'title': 'Why Was the Great Pyramid Built? Purpose, Meaning, and Mysteries',
            'slug': 'great-pyramid-purpose-meaning',
            'excerpt': "The Great Pyramid took 20 years and millions of blocks. But why?",
            'image_url': 'https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=1200&q=80',
            'is_featured': False,
        },
    ]

    created = 0
    updated = 0

    for article in articles:
        content = f"""## {article['title']}

{article['excerpt']}

This is part of our comprehensive 9-part series on the Great Pyramid of Giza, exploring its history, construction, mysteries, and enduring legacy.

The Great Pyramid stands as humanity's greatest architectural achievement - built 4,500 years ago with precision that rivals modern engineering.

### Key Facts
- Built around 2560 BCE during Pharaoh Khufu's reign
- 2.3 million stone blocks, weighing 2.5 to 80 tons each
- Original height: 146.6 meters (481 feet)
- Base accuracy: 99.98% perfect symmetry
- Aligned to true north within 0.05 degrees

Visit 360egy.com for the complete article with full details, images, and interactive content.

---
*Part of the Great Pyramid Series on 360egy.com*
"""

        post, was_created = BlogPost.objects.update_or_create(
            slug=article['slug'],
            defaults={
                'title': article['title'],
                'author': author,
                'category': category,
                'excerpt': article['excerpt'],
                'content': content,
                'image_url': article['image_url'],
                'meta_description': article['excerpt'],
                'meta_keywords': 'great pyramid, giza, egypt, ancient egypt, pyramids',
                'tags': 'pyramids, giza, ancient egypt, history',
                'status': 'published',
                'is_featured': article['is_featured'],
                'published_at': now,
            }
        )
        if was_created:
            created += 1
        else:
            updated += 1

    return JsonResponse({
        'success': True,
        'created': created,
        'updated': updated,
        'total': len(articles),
        'message': f'Created {created}, updated {updated} pyramid articles'
    })


def blog_list_test(request):
    """Temporary test view - returns JSON to debug"""
    try:
        posts = list(BlogPost.objects.filter(status='published').order_by('-published_at')[:5].values('title', 'slug'))
        categories = list(BlogCategory.objects.values('name', 'slug')[:5])
        return JsonResponse({
            'status': 'ok',
            'posts': posts,
            'categories': categories,
            'total_posts': BlogPost.objects.count(),
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        import sys
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            # Print to stdout for gunicorn capture
            print(f"BLOG_ERROR: {str(e)}", file=sys.stderr)
            print(f"BLOG_TRACE: {traceback.format_exc()}", file=sys.stderr)
            # Return error as JSON for debugging
            from django.http import JsonResponse
            return JsonResponse({
                'error': str(e),
                'traceback': traceback.format_exc(),
                'view': 'BlogListView'
            }, status=500)

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published').order_by('-published_at', '-created_at')
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.filter(
            posts__status='published'
        ).distinct().order_by('name')
        context['featured_posts'] = BlogPost.objects.filter(
            status='published',
            is_featured=True
        ).order_by('-published_at')[:6]
        context['recent_posts'] = BlogPost.objects.filter(status='published')[:5]

        # New context for enhanced blog list
        context['current_category'] = self.request.GET.get('category', '')
        context['featured_post'] = BlogPost.objects.filter(
            status='published',
            is_featured=True
        ).order_by('-published_at').first()
        context['trending_posts'] = BlogPost.objects.filter(
            status='published'
        ).order_by('-views_count', '-published_at')[:5]
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(status='approved')
        context['recent_posts'] = BlogPost.objects.exclude(id=self.object.id)[:5]
        return context