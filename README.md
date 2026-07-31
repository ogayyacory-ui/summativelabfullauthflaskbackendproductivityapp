# Full Auth Flask Backend - Productivity Tool

A Flask-based backend for a productivity application with full authentication support, note management, and user-specific protected routes.

## Project Description

This project provides a RESTful API for a productivity tool where users can sign up, log in, and manage personal notes. Authentication is handled using JSON Web Tokens (JWT), and note resources are linked to the authenticated user.

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd summativelabfullauthflaskbackendproductivityapp
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install pipenv
   pipenv install
   ```

4. Set environment variables if desired:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export SECRET_KEY="your_secret_key"
   export JWT_SECRET_KEY="your_jwt_secret_key"
   export DATABASE_URL="sqlite:///app.db"
   ```

5. Initialize the database and seed sample data:
   ```bash
   pipenv run python seed.py
   ```

## Run Instructions

Start the Flask application with:
```bash
pipenv run flask run --port 5000
```

Or run directly with Python:
```bash
pipenv run python app.py
```

## API Endpoints

- `POST /register`
  - Create a new user account.
  - Request body: `username`, `email`, `password`
  - Response: created user object with `id`, `username`, and `email`

- `POST /login`
  - Authenticate an existing user.
  - Request body: `email`, `password`
  - Response: JWT access token

- `GET /me`
  - Retrieve the currently authenticated user.
  - Requires `Authorization: Bearer <token>` header or authenticated JWT cookie.
  - Response: user object with `id`, `username`, and `email`

- `POST /logout`
  - Log out the current user and clear JWT cookies.
  - Response: success message.

- `GET /notes`
  - List notes for the authenticated user.
  - Supports pagination with `page` and `per_page` query params.
  - Requires JWT authorization.

- `POST /notes`
  - Create a new note for the authenticated user.
  - Request body: `title`, `content`
  - Requires JWT authorization.

- `GET /notes/<note_id>`
  - Retrieve a single note by ID.
  - Requires JWT authorization and ownership of the note.

- `PATCH /notes/<note_id>`
  - Update the title and/or content of a note.
  - Requires JWT authorization and ownership of the note.

- `DELETE /notes/<note_id>`
  - Delete a note.
  - Requires JWT authorization and ownership of the note.

## Notes

- The app uses `Flask-RESTful` for API resources.
- Authentication uses `Flask-JWT-Extended`.
- Passwords are hashed with `Flask-Bcrypt`.
- `seed.py` creates sample users and notes for quick testing.
