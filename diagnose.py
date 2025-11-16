"""
Egy360 Diagnostic Script
Run this to find out what's wrong!

Save as: diagnose.py in your project root
Run: python diagnose.py
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("🔍 EGY360 DIAGNOSTIC TOOL")
print("=" * 60)

# Get project root
BASE_DIR = Path(__file__).resolve().parent
print(f"\n📂 Project Root: {BASE_DIR}\n")

# Check Python version
print(f"🐍 Python Version: {sys.version}")

# Check Django
try:
    import django

    print(f"✅ Django Version: {django.get_version()}")
except ImportError:
    print("❌ Django NOT installed!")
    sys.exit(1)

print("\n" + "=" * 60)
print("📁 FOLDER CHECK")
print("=" * 60)

folders_to_check = {
    'Egy360': BASE_DIR / 'Egy360',
    'core': BASE_DIR / 'core',
    'templates': BASE_DIR / 'templates',
    'static': BASE_DIR / 'static',
    'static/css': BASE_DIR / 'static' / 'css',
    'static/js': BASE_DIR / 'static' / 'js',
}

for name, path in folders_to_check.items():
    if path.exists():
        print(f"✅ {name}: EXISTS")
    else:
        print(f"❌ {name}: MISSING - {path}")

print("\n" + "=" * 60)
print("📄 FILE CHECK")
print("=" * 60)

files_to_check = {
    'Egy360/settings.py': BASE_DIR / 'Egy360' / 'settings.py',
    'Egy360/urls.py': BASE_DIR / 'Egy360' / 'urls.py',
    'core/__init__.py': BASE_DIR / 'core' / '__init__.py',
    'core/views.py': BASE_DIR / 'core' / 'views.py',
    'templates/home.html': BASE_DIR / 'templates' / 'home.html',
    'static/css/home_styles.css': BASE_DIR / 'static' / 'css' / 'home_styles.css',
    'static/js/home_script.js': BASE_DIR / 'static' / 'js' / 'home_script.js',
}

for name, path in files_to_check.items():
    if path.exists():
        size = path.stat().st_size / 1024
        print(f"✅ {name}: {size:.1f} KB")
    else:
        print(f"❌ {name}: MISSING")

print("\n" + "=" * 60)
print("⚙️  SETTINGS.PY CHECK")
print("=" * 60)

settings_path = BASE_DIR / 'Egy360' / 'settings.py'
if settings_path.exists():
    content = settings_path.read_text()

    # Check for critical settings
    checks = {
        'BASE_DIR': 'BASE_DIR = ' in content,
        'TEMPLATES DIRS': "'DIRS': [BASE_DIR / 'templates']" in content or '"DIRS": [BASE_DIR / \'templates\']' in content,
        'STATIC_URL': 'STATIC_URL' in content,
        'STATICFILES_DIRS': 'STATICFILES_DIRS' in content,
        'core in APPS': "'core'" in content,
    }

    for check_name, result in checks.items():
        if result:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}: NOT FOUND")
else:
    print("❌ settings.py not found!")

print("\n" + "=" * 60)
print("🔗 URLS.PY CHECK")
print("=" * 60)

urls_path = BASE_DIR / 'Egy360' / 'urls.py'
if urls_path.exists():
    content = urls_path.read_text()

    checks = {
        'admin path': "path('admin/" in content,
        'home import': 'from core.views import home' in content or 'core.views' in content,
        'home path': "path('', home" in content or 'path("", home' in content,
    }

    for check_name, result in checks.items():
        if result:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}: NOT FOUND")
else:
    print("❌ urls.py not found!")

print("\n" + "=" * 60)
print("🎯 CORE/VIEWS.PY CHECK")
print("=" * 60)

views_path = BASE_DIR / 'core' / 'views.py'
if views_path.exists():
    content = views_path.read_text()

    checks = {
        'home function': 'def home(' in content,
        'render import': 'from django.shortcuts import render' in content,
    }

    for check_name, result in checks.items():
        if result:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}: NOT FOUND")
else:
    print("❌ views.py not found!")

print("\n" + "=" * 60)
print("📋 SUMMARY & NEXT STEPS")
print("=" * 60)

# Count issues
all_folders_exist = all(path.exists() for path in folders_to_check.values())
all_files_exist = all(path.exists() for path in files_to_check.values())

if all_folders_exist and all_files_exist:
    print("\n✅ ALL CHECKS PASSED!")
    print("\n🚀 Next Steps:")
    print("   1. Run: python manage.py runserver")
    print("   2. Visit: http://127.0.0.1:8000/")
    print("   3. Visit: http://127.0.0.1:8000/admin/")
else:
    print("\n❌ ISSUES FOUND!")
    print("\n🔧 To Fix:")

    if not (BASE_DIR / 'core').exists():
        print("   1. Run: python manage.py startapp core")

    if not (BASE_DIR / 'templates').exists():
        print("   2. Create: templates/ folder")

    if not (BASE_DIR / 'templates' / 'home.html').exists():
        print("   3. Place home.html in templates/")

    if not (BASE_DIR / 'static' / 'css').exists():
        print("   4. Create: static/css/ folder")

    if not (BASE_DIR / 'static' / 'css' / 'home_styles.css').exists():
        print("   5. Place home_styles.css in static/css/")

    if not (BASE_DIR / 'static' / 'js' / 'home_script.js').exists():
        print("   6. Place home_script.js in static/js/")

print("\n" + "=" * 60)