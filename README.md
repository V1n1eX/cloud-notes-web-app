# Cloud Notes

A Django web app for creating and organizing notes in folders, sharing notes with other users, and generating AI-powered summaries.

## Features

- User registration, login, and logout
- Create, edit, sort, and organize notes in folders
- Share notes with read-only or write access
- Recover deleted notes and folders from the recycle bin, or delete them permanently
- Generate and save note summaries using the Together AI API

## Requirements

- Python 3.11 (see `runtime.txt`)
- pip

## Run locally

1. Clone the repository and move into its directory:

   ```bash
   git clone https://github.com/V1n1eX/cloud-notes-web-app.git
   cd cloud-notes-web-app
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables. You can copy `.env.example` to `.env` and update its values. At minimum, set a private `SECRET_KEY` for your environment. For local development, set `DEBUG=True` and include `localhost,127.0.0.1` in `ALLOWED_HOSTS`. The app uses SQLite by default; set `DATABASE_URL` if you want to use another supported database. To enable AI summaries, set `TOGETHER_API_KEY` to a Together AI API key.

5. Apply database migrations and start the development server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. The root page redirects to the notes area; sign in or register to use the app.

## Deployment

The repository includes a `render.yaml` for deploying the web service on Render. It installs the requirements, collects static files, and runs the app with Gunicorn. Configure production environment variables in Render, including a secure `SECRET_KEY`, `DEBUG=False`, and the appropriate `ALLOWED_HOSTS`. Set `DATABASE_URL` if using a managed database, and `TOGETHER_API_KEY` if you want AI summaries.

## Tech stack

- Django 5.2
- SQLite by default, with database URL configuration available
- Gunicorn and WhiteNoise for deployment and static files
- Together AI for note summaries (optional)
