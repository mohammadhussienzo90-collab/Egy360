"""
Custom template filters for blog content
"""
import re
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()


@register.filter(name='clean_markdown')
def clean_markdown(text):
    """Remove markdown formatting and convert to clean HTML"""
    if not text:
        return text

    # Escape HTML first for security
    text = escape(text)

    # Remove markdown headers (## ### etc) - keep the text
    text = re.sub(r'^#{1,6}\s*(.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)

    # Convert bold **text** to <strong>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # Convert italic *text* to <em>
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

    # Convert __text__ to <strong>
    text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)

    # Convert _text_ to <em>
    text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)

    # Remove markdown links [text](url) -> just text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Remove markdown table separators
    text = re.sub(r'^\s*\|[-:| ]+\|\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\|\s*', '', text)

    # Remove special Unicode characters
    replacements = {
        '\u2192': ' - ',  # right arrow
        '\u2190': ' - ',  # left arrow
        '\u2191': '',     # up arrow
        '\u2193': '',     # down arrow
        '\u25ba': '',     # play
        '\u25b6': '',     # play
        '\u25cf': '-',    # bullet
        '\u2022': '-',    # bullet
        '\u25aa': '-',    # small square
        '\u2713': 'Yes',  # checkmark
        '\u2717': 'No',   # x mark
        '\u2605': '*',    # star
        '\u2606': '*',    # star outline
        '\u2014': '-',    # em dash
        '\u2013': '-',    # en dash
        '\u201c': '"',    # left quote
        '\u201d': '"',    # right quote
        '\u2018': "'",    # left single quote
        '\u2019': "'",    # right single quote
        '\u2026': '...',  # ellipsis
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove code blocks
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Convert bullet points - dash at start of line
    text = re.sub(r'^-\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)

    # Convert numbered lists
    text = re.sub(r'^\d+\.\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)

    # Convert line breaks to paragraphs
    paragraphs = text.split('\n\n')
    cleaned_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p:
            # Check if it's already wrapped in HTML tags
            if p.startswith('<h') or p.startswith('<li'):
                cleaned_paragraphs.append(p)
            else:
                # Replace single newlines with <br>
                p = p.replace('\n', '<br>')
                cleaned_paragraphs.append(f'<p>{p}</p>')

    text = '\n'.join(cleaned_paragraphs)

    # Wrap consecutive <li> items in <ul>
    text = re.sub(r'(<li>.*?</li>\s*)+', lambda m: '<ul>' + m.group(0) + '</ul>', text)

    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'<br>\s*<br>\s*<br>', '<br><br>', text)

    return mark_safe(text)
