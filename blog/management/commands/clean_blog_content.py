"""
Management command to clean blog post content - remove markdown and special characters
"""
import re
from django.core.management.base import BaseCommand
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Clean blog post content by removing markdown formatting and special characters'

    def clean_content(self, text):
        """Remove markdown formatting and special characters"""
        if not text:
            return text

        # Remove markdown headers (## ### etc)
        text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)

        # Remove bold/italic markers
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)

        # Remove markdown links [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

        # Convert markdown tables to readable format
        text = re.sub(r'^\s*\|[-:| ]+\|\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'\|\s*', '', text)

        # Remove special Unicode characters
        replacements = {
            '\u2192': ' - ',  # →
            '\u2190': ' - ',  # ←
            '\u2191': '',     # ↑
            '\u2193': '',     # ↓
            '\u25ba': '',     # ►
            '\u25b6': '',     # ▶
            '\u25cf': '-',    # ●
            '\u2022': '-',    # •
            '\u25aa': '-',    # ▪
            '\u2713': 'Yes',  # ✓
            '\u2717': 'No',   # ✗
            '\u2605': '*',    # ★
            '\u2606': '*',    # ☆
            '\u2014': '-',    # —
            '\u2013': '-',    # –
            '\u201c': '"',    # "
            '\u201d': '"',    # "
            '\u2018': "'",    # '
            '\u2019': "'",    # '
            '\u2026': '...',  # …
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        # Remove code blocks
        text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
        text = re.sub(r'`([^`]+)`', r'\1', text)

        # Clean up extra whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r' +\n', '\n', text)
        text = re.sub(r'\n +', '\n', text)

        return text.strip()

    def handle(self, *args, **options):
        posts = BlogPost.objects.all().order_by('id')
        self.stdout.write(f"Found {posts.count()} blog posts to clean\n")

        cleaned_count = 0
        for post in posts:
            self.stdout.write(f"Processing: {post.id} - {post.title[:50]}...")

            original = post.content
            cleaned = self.clean_content(original)

            if original != cleaned:
                post.content = cleaned
                post.save()
                cleaned_count += 1
                self.stdout.write(self.style.SUCCESS("  Cleaned and saved"))
            else:
                self.stdout.write("  No changes needed")

        self.stdout.write(self.style.SUCCESS(f"\nDone! Cleaned {cleaned_count} blog posts."))
