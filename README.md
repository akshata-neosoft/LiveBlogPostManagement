# Live BlogPost Management
# Blogging Platform API

This is a Django REST Framework-based API for a blogging platform with  and JWT-based single-session authentication.
# 🧰 Requirements

    Python 3.9+
    pip
    PostgreSQL
    virtualenv (recommended)

# 🚀 Setup Instructions

    # 1. Clone the repository
    git clone {{repo link}}
    
    # 2. Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # 3. Install dependencies
    pip install -r requirements.txt

    # 4. Load Fixtures
    py manage.py loaddata .\blogpost_management\fixtures\status.json

    # 5. Run migrations
    python manage.py makemigrations
    python manage.py migrate

    # 6. Start the development server
    python manage.py runserver

