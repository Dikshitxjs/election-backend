Backend deployment notes

This repository contains a small Flask API for the Election app. The recommended deployment options are to deploy the backend to a service that supports Docker or a Python web process (Render, Railway, Heroku, Fly.io). The frontend (Next.js) should be deployed on Vercel and pointed to this backend via `NEXT_PUBLIC_API_URL`.

Quick Docker (local) build and run

```bash
# from backend-election/
docker build -t election-backend:latest .
docker run -e SECRET_KEY=change-this -e CORS_ORIGINS=http://localhost:3000 -p 5000:5000 election-backend:latest
```

Railway / Render (simple) - using Docker

- Create a new project on the host of choice and connect the repo.
- Set environment variables in the host dashboard:
  - `DATABASE_URL` (production DB)
  - `CORS_ORIGINS` (comma-separated frontend origins, e.g. https://your-frontend.vercel.app)
  - `SECRET_KEY`
- Configure build/start to use the Dockerfile (most hosts auto-detect Dockerfile).

Railway / Render (non-Docker)

- Set `Build Command`: `pip install -r requirements.txt`
- Set `Start Command`: `gunicorn --bind 0.0.0.0:$PORT run:app --workers 2 --threads 2`

Notes and production recommendations

- Use HTTPS endpoints for `NEXT_PUBLIC_API_URL` and add that domain to `CORS_ORIGINS`.
- Replace the in-repo SQLite `DATABASE_URL` with a managed DB for production.
- Consider adding a `fingerprint` column to `votes` and a unique constraint on `(fingerprint, candidate_id)`.
- Implement persistence or an email provider to handle contact messages instead of server logs.
- Set `SECRET_KEY` and other secrets via environment variables — DO NOT commit secrets.
