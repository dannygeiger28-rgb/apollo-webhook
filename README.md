# Apollo.io Webhook — Render.com Deploy

## Deploy in 5 minutes (free, permanent public URL)

### Step 1 — Push to GitHub
1. Go to github.com → New repository → name it `apollo-webhook`
2. Upload these 3 files: `app.py`, `requirements.txt`, `Procfile`
3. Click "Commit changes"

### Step 2 — Deploy on Render
1. Go to render.com → Sign up free
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo (`apollo-webhook`)
4. Fill in:
   - **Name:** apollo-webhook
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **"Create Web Service"**

### Step 3 — Get your public URL
Render gives you a permanent URL like:
```
https://apollo-webhook.onrender.com
```

### Step 4 — Add to Apollo.io
Go to Apollo → Settings → Integrations → Webhooks
Paste your URL + `/webhook`:
```
https://apollo-webhook.onrender.com/webhook
```

## Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhook` | POST | Apollo sends enriched contacts here |
| `/contacts` | GET | View all saved contacts |
| `/health` | GET | Check server is running |
