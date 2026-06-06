# Monitoring API (FastAPI)

Project ini adalah API sederhana untuk monitoring resource (CPU & memory) dan endpoint webhook Telegram.

## Fitur

- GET `/cpu` → statistik CPU
- GET `/memory` → statistik memory
- POST `/api/webhook` → endpoint webhook (untuk menerima update Telegram)
- Swagger UI: `/docs`

## Struktur Singkat

- `app/main.py` → entrypoint FastAPI
- `app/router/` → routing (`vps.py`, `telegram.py`)
- `app/service/` → logic service (`vps.py`, `telegram.py`)
- `app/schema/` → schema response (Pydantic)

## Menjalankan Tanpa Docker (Windows)

Dijalankan dari folder `app` (karena import di kode memakai `router.*` dan `service.*`).

```powershell
cd C:\Project\monitoring\app
.\venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8015 --reload
```

Buka:

- `http://127.0.0.1:8015/docs`
- `http://127.0.0.1:8015/cpu`
- `http://127.0.0.1:8015/memory`

## Menjalankan Dengan Docker Compose

Pastikan Docker Desktop sudah running (Linux containers).

```powershell
cd C:\Project\monitoring\app
docker compose up -d --build
```

Stop:

```powershell
docker compose down
```

## Konfigurasi Environment (Telegram)

Kode di `app/main.py` menjalankan background task `alert()` yang mencoba kirim alert Telegram.
Siapkan file `app/.env` untuk environment berikut:

- `TELEGRAM_TOKEN` → bot token
- `TELEGRAM_CHAT_ID` → chat id tujuan alert

Webhook endpoint ada di:

- `POST /api/webhook`

