"""
Custom template filters for blog content
"""
import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='split_tags')
def split_tags(value):
    """Split comma-separated tags into a list"""
    if not value:
        return []
    return [tag.strip() for tag in value.split(',') if tag.strip()]


@register.filter(name='clean_markdown')
def clean_markdown(text):
    """Remove markdown formatting and return clean readable text as HTML"""
    if not text:
        return text

    # First, handle backslash-escaped markdown characters
    # These might appear as \# \* \[ etc in the content
    text = text.replace('\\#', '#')
    text = text.replace('\\*', '*')
    text = text.replace('\\[', '[')
    text = text.replace('\\]', ']')
    text = text.replace('\\_', '_')
    text = text.replace('\\`', '`')
    text = text.replace('\\|', '|')

    # Remove markdown headers (## ### etc) at start of lines
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)

    # Remove bold markers **text** -> text
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)

    # Remove italic markers *text* -> text
    text = re.sub(r'\*([^*]+)\*', r'\1', text)

    # Remove __text__ -> text
    text = re.sub(r'__([^_]+)__', r'\1', text)

    # Remove _text_ -> text (but not mid-word underscores)
    text = re.sub(r'(?<![a-zA-Z])_([^_]+)_(?![a-zA-Z])', r'\1', text)

    # Remove markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Remove markdown table separators
    text = re.sub(r'^\s*\|[-:| ]+\|\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\|', ' ', text)

    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)

    # Remove special Unicode characters
    replacements = {
        '\u2192': '-',   # right arrow
        '\u2190': '-',   # left arrow
        '\u2191': '',    # up arrow
        '\u2193': '',    # down arrow
        '\u25ba': '',    # play
        '\u25b6': '',    # play
        '\u25cf': '-',   # bullet
        '\u2022': '-',   # bullet
        '\u25aa': '-',   # small square
        '\u2713': 'Yes', # checkmark
        '\u2717': 'No',  # x mark
        '\u2605': '*',   # star
        '\u2606': '*',   # star outline
        '\u2014': '-',   # em dash
        '\u2013': '-',   # en dash
        '\u201c': '"',   # left quote
        '\u201d': '"',   # right quote
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u2026': '...',  # ellipsis
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Clean up multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Strip leading/trailing whitespace from lines
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    text = '\n'.join(lines)

    # Convert to HTML paragraphs
    paragraphs = text.split('\n\n')
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if p:
            # Convert single newlines to <br>
            p = p.replace('\n', '<br>')
            html_parts.append(f'<p>{p}</p>')

    return mark_safe('\n'.join(html_parts))
