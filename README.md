# roleRadar


A real-time job search tool. Instead of refreshing a job board, you search once and matching roles stream in live as they're found — pulled from multiple job boards and company career pages at the same time.

## How it works

1. Type a keyword.
2. RoleRadar checks what's already been scraped and shows matches instantly, while kicking off a fresh scrape of every connected source in the background.
3. New matches stream in over a websocket as they're found — no refresh, no polling.

## Sources

- [RemoteOK](https://remoteok.com) and [Jobicy](https://jobicy.com) — remote job aggregators
- [We Work Remotely](https://weworkremotely.com) — remote job board (RSS)
- Direct company career pages via [Greenhouse](https://www.greenhouse.io) and [Lever](https://www.lever.co) — no aggregator in between, straight from the source

Adding a company is a one-line edit in `backend/jobs/scrapers/companies.py`.

## Architecture

- **Backend** — Django, with [Celery](https://docs.celeryq.dev) running the scrapers as background tasks and [Django Channels](https://channels.readthedocs.io) handling the websocket connection to the frontend
- **Data layer** — PostgreSQL with the [pgvector](https://github.com/pgvector/pgvector) extension (every scraped job gets an embedding computed via `sentence-transformers`, laying the groundwork for semantic search) and Redis, backing both Celery's task queue and the Channels websocket layer
- **Frontend** — React, built with Vite

```
roleRadar/
├── backend/          Django, Celery, Channels
│   ├── config/
│   └── jobs/
│       ├── models.py
│       ├── consumers.py       websocket handling
│       ├── tasks.py           scraping and dedup logic
│       └── scrapers/          one file per source
└── frontend/         React + Vite
    └── src/
        ├── hooks/useJobSearch.js
        └── components/
```

## Running it locally

You'll need PostgreSQL (with the `vector` extension) and Redis running first.

**Backend**

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your own values
python manage.py migrate
python manage.py createsuperuser
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

In a separate terminal, start the Celery worker:

```
cd backend
source venv/bin/activate
celery -A config worker -l info
```

**Frontend**

```
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Known limitations

- Matching is currently keyword-based (title, company, and source tags) — not yet semantic, though the embeddings needed for that are already being computed and stored.
- No saved searches or alerts yet — every search starts fresh.
- Some sources (like Lever) can't distinguish "no jobs open" from "this company doesn't exist here," since both return an empty result.

## License

MIT — see [LICENSE](LICENSE).