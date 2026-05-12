# 🌾 NLP Agriculture News Classification Dashboard

Dashboard Streamlit untuk Mini Project NLP — Klasifikasi Berita Pertanian.

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan locally
```bash
streamlit run app.py
```
Dashboard akan terbuka di `http://localhost:8501`

### 3. Deploy ke Streamlit Community Cloud (gratis)
1. Push folder ini ke GitHub repository
2. Buka https://share.streamlit.io
3. Klik **New app** → pilih repo & branch → set `app.py` sebagai Main file
4. Klik **Deploy** — dapat domain `https://nama-app.streamlit.app`

### 4. Deploy ke server sendiri (VPS/domain custom)
```bash
# Install
pip install -r requirements.txt

# Jalankan di background (port 8501)
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &

# Atau pakai screen
screen -S dashboard
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```
Kemudian arahkan domain/subdomain kamu ke server dengan reverse proxy Nginx:

```nginx
server {
    listen 80;
    server_name dashboard.namadomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

## Struktur File
```
nlp_dashboard/
├── app.py           ← file utama Streamlit
├── requirements.txt ← dependencies
└── README.md        ← panduan ini
```

## Fitur Dashboard
- **Tab 1** · Hasil 6 eksperimen (bar chart + radar chart + tabel)
- **Tab 2** · Dataset info, distribusi kategori, sample 25 data
- **Tab 3** · Pipeline preprocessing step-by-step + contoh transformasi
- **Tab 4** · Perbandingan antar metode representasi & algoritma