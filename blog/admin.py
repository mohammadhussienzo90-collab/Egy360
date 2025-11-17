from django.contrib import admin
from .models import BlogPost, BlogCategory, BlogComment


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'published_at', 'views_count', 'likes_count']
    list_filter = ['status', 'is_featured', 'category', 'published_at', 'related_city']
    search_fields = ['title', 'content', 'excerpt', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    raw_id_fields = ['author', 'related_city']

    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'category', 'related_city')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'tags', 'featured_image')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Publishing', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'status', 'parent_comment', 'likes_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'comment', 'post__title']
    raw_id_fields = ['post', 'user', 'parent_comment', 'moderated_by']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'user', 'comment', 'parent_comment')
        }),
        ('Moderation', {
            'fields': ('status', 'moderated_by', 'moderated_at')
        }),
        ('Statistics', {
            'fields': ('likes_count',),
            'classes': ('collapse',)
        }),
    )

    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        queryset.update(status='approved')
    approve_comments.short_description = "Approve selected comments"

    def reject_comments(self, request, queryset):
        queryset.update(status='rejected')
    reject_comments.short_description = "Reject selected comments"