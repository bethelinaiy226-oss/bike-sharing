# Bike Sharing Analysis Dashboard 🚲
Proyek analisis data penyewaan sepeda menggunakan **Bike Sharing Dataset**. Analisis dilakukan untuk memahami pola penyewaan sepeda berdasarkan musim, kondisi cuaca, jam penyewaan, serta perbedaan perilaku pengguna *casual* dan *registered* pada hari kerja dan hari nonkerja.

Proyek ini mencakup analisis data menggunakan Python dan visualisasi interaktif menggunakan Streamlit.

## Dataset

Dataset yang digunakan terdiri dari dua file:

- `day.csv`: Data penyewaan sepeda harian.
- `hour.csv`: Data penyewaan sepeda per jam.

Dataset mencakup periode Januari 2011 hingga Desember 2012.

## Key Findings

- Musim gugur (*season 3*) memiliki rata-rata penyewaan harian tertinggi.
- Penyewaan sepeda cenderung lebih tinggi ketika kondisi cuaca cerah dibandingkan saat cuaca buruk.
- Pada hari kerja, penyewaan mencapai puncak sekitar pukul 08.00 dan 17.00, yang menunjukkan pola penggunaan pada jam berangkat dan pulang kerja.
- Pada hari nonkerja, penyewaan mencapai puncak sekitar pukul 13.00.
- Pengguna *registered* mendominasi penyewaan pada hari kerja maupun hari nonkerja, dengan proporsi yang lebih besar pada hari kerja.

## Project Structure

```text
bike-sharing-analysis/
├── day.csv
├── hour.csv
├── Bike_Sharing_Analysis_Bethelina.ipynb
├── dashboard.py
├── requirements.txt
└── README.md
```

## Requirements

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

## Setup Environment

### Using Anaconda

```bash
conda create --name bike-sharing python=3.11
conda activate bike-sharing
pip install -r requirements.txt
```

### Using Shell/Terminal

Pastikan Python dan pip sudah terpasang. Buka terminal, lalu masuk ke direktori proyek:

```bash
cd bike-sharing-analysis
```

Install seluruh library yang dibutuhkan:

```bash
python -m pip install -r requirements.txt
```

Jika menggunakan Windows dengan Python Launcher, perintah berikut juga dapat digunakan:

```bash
py -3.14 -m pip install -r requirements.txt
```

## Run Streamlit Dashboard

Jalankan perintah berikut dari direktori proyek:

```bash
python -m streamlit run dashboard.py
```

Atau, pada Windows:

```bash
py -3.14 -m streamlit run dashboard.py
```

Setelah aplikasi berjalan, buka alamat lokal yang ditampilkan di terminal, biasanya:

```text
http://localhost:8501
```

Dashboard menyediakan visualisasi dan filter untuk mengeksplorasi data penyewaan sepeda berdasarkan tahun, musim, dan kondisi cuaca.

## Tools & Libraries

- **Python** — Bahasa pemrograman untuk analisis data.
- **Pandas & NumPy** — Pengolahan dan analisis data.
- **Matplotlib & Seaborn** — Visualisasi data.
- **Streamlit** — Pembuatan dashboard interaktif.