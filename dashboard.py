from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

SEASON_LABELS = {
    1: "Musim semi",
    2: "Musim panas",
    3: "Musim gugur",
    4: "Musim dingin"
}

WEATHER_LABELS = {
    1: "Cerah / sedikit awan",
    2: "Berkabut / berawan",
    3: "Hujan ringan / cuaca buruk",
    4: "Cuaca ekstrem"
}


# ==========================================
# 2. MEMUAT DATASET
# ==========================================
@st.cache_data
def load_data():
    day = pd.read_csv(BASE_DIR / "day.csv")
    hour = pd.read_csv(BASE_DIR / "hour.csv")

    day["dteday"] = pd.to_datetime(day["dteday"])
    hour["dteday"] = pd.to_datetime(hour["dteday"])

    day["Tahun"] = day["yr"].map({0: 2011, 1: 2012})
    hour["Tahun"] = hour["yr"].map({0: 2011, 1: 2012})

    day["Musim"] = day["season"].map(SEASON_LABELS)
    hour["Musim"] = hour["season"].map(SEASON_LABELS)

    day["Kondisi Cuaca"] = day["weathersit"].map(WEATHER_LABELS)
    hour["Kondisi Cuaca"] = hour["weathersit"].map(WEATHER_LABELS)

    day["Jenis Hari"] = day["workingday"].map({
        0: "Hari Nonkerja",
        1: "Hari Kerja"
    })

    hour["Jenis Hari"] = hour["workingday"].map({
        0: "Hari Nonkerja",
        1: "Hari Kerja"
    })

    return day, hour


try:
    day_df, hour_df = load_data()
except FileNotFoundError as error:
    st.error(
        "File dataset tidak ditemukan. Pastikan day.csv dan hour.csv "
        "berada di folder yang sama dengan dashboard.py."
    )
    st.stop()


# ==========================================
# 3. JUDUL DAN DESKRIPSI
# ==========================================
st.title("🚲 Bike Sharing Dashboard")
st.markdown(
    """
    Dashboard interaktif untuk mengeksplorasi penyewaan sepeda
    berdasarkan waktu, jenis hari, musim, kondisi cuaca,
    dan jenis pengguna selama 2011–2012.
    """
)

st.divider()


# ==========================================
# 4. FILTER INTERAKTIF
# ==========================================
st.sidebar.header("Filter Data")

available_years = sorted(day_df["Tahun"].dropna().unique())
selected_years = st.sidebar.multiselect(
    "Pilih tahun",
    options=available_years,
    default=available_years
)

available_seasons = list(SEASON_LABELS.values())
selected_seasons = st.sidebar.multiselect(
    "Pilih musim",
    options=available_seasons,
    default=available_seasons
)

available_weather = sorted(
    day_df["Kondisi Cuaca"].dropna().unique().tolist()
)
selected_weather = st.sidebar.multiselect(
    "Pilih kondisi cuaca",
    options=available_weather,
    default=available_weather
)

if not selected_years or not selected_seasons or not selected_weather:
    st.warning("Pilih minimal satu tahun, musim, dan kondisi cuaca.")
    st.stop()


# Terapkan filter ke data harian dan per jam
day_filtered = day_df[
    day_df["Tahun"].isin(selected_years)
    & day_df["Musim"].isin(selected_seasons)
    & day_df["Kondisi Cuaca"].isin(selected_weather)
].copy()

hour_filtered = hour_df[
    hour_df["Tahun"].isin(selected_years)
    & hour_df["Musim"].isin(selected_seasons)
    & hour_df["Kondisi Cuaca"].isin(selected_weather)
].copy()

if day_filtered.empty or hour_filtered.empty:
    st.warning("Tidak ada data yang sesuai dengan kombinasi filter ini.")
    st.stop()


# ==========================================
# 5. RINGKASAN METRIK
# ==========================================
st.subheader("Ringkasan Penyewaan")

total_rentals = int(day_filtered["cnt"].sum())
average_daily = day_filtered["cnt"].mean()
total_casual = int(day_filtered["casual"].sum())
total_registered = int(day_filtered["registered"].sum())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Penyewaan", f"{total_rentals:,}")
col2.metric("Rata-rata per Hari", f"{average_daily:,.0f}")
col3.metric("Pengguna Kasual", f"{total_casual:,}")
col4.metric("Pengguna Terdaftar", f"{total_registered:,}")

st.caption(
    f"Periode data terpilih: "
    f"{day_filtered['dteday'].min():%d %b %Y} – "
    f"{day_filtered['dteday'].max():%d %b %Y}"
)

st.divider()


# ==========================================
# 6. POLA PENYEWAAN PER JAM
# ==========================================
st.subheader("1. Pola Penyewaan Berdasarkan Jam")

hourly_summary = (
    hour_filtered.groupby(["hr", "Jenis Hari"])["cnt"]
    .mean()
    .reset_index()
)

fig1, ax1 = plt.subplots(figsize=(11, 5))

sns.lineplot(
    data=hourly_summary,
    x="hr",
    y="cnt",
    hue="Jenis Hari",
    marker="o",
    ax=ax1
)

ax1.set_title("Rata-rata Penyewaan per Jam dan Jenis Hari")
ax1.set_xlabel("Jam")
ax1.set_ylabel("Rata-rata Penyewaan")
ax1.set_xticks(range(24))
ax1.grid(alpha=0.3)
fig1.tight_layout()

st.pyplot(fig1)
plt.close(fig1)


# ==========================================
# 7. PENYEWAAN BERDASARKAN MUSIM DAN CUACA
# ==========================================
st.subheader("2. Penyewaan Berdasarkan Musim dan Cuaca")

col1, col2 = st.columns(2)

season_summary = (
    day_filtered.groupby("Musim", observed=False)["cnt"]
    .mean()
    .reindex(available_seasons)
    .dropna()
)

with col1:
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    season_summary.plot(kind="bar", ax=ax2)
    ax2.set_title("Rata-rata Penyewaan per Musim")
    ax2.set_xlabel("Musim")
    ax2.set_ylabel("Rata-rata Penyewaan per Hari")
    ax2.tick_params(axis="x", rotation=25)
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

weather_summary = (
    day_filtered.groupby("Kondisi Cuaca")["cnt"]
    .mean()
    .sort_values(ascending=False)
)

with col2:
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    weather_summary.plot(kind="bar", ax=ax3)
    ax3.set_title("Rata-rata Penyewaan per Kondisi Cuaca")
    ax3.set_xlabel("Kondisi Cuaca")
    ax3.set_ylabel("Rata-rata Penyewaan per Hari")
    ax3.tick_params(axis="x", rotation=25)
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)


# ==========================================
# 8. PERBANDINGAN JENIS PENGGUNA
# ==========================================
st.subheader("3. Pengguna Kasual vs Terdaftar")

user_summary = (
    hour_filtered.groupby("Jenis Hari")[["casual", "registered"]]
    .mean()
    .reindex(["Hari Nonkerja", "Hari Kerja"])
)

user_plot = user_summary.reset_index().melt(
    id_vars="Jenis Hari",
    var_name="Jenis Pengguna",
    value_name="Rata-rata Penyewaan per Jam"
)

fig4, ax4 = plt.subplots(figsize=(9, 5))

sns.barplot(
    data=user_plot,
    x="Jenis Hari",
    y="Rata-rata Penyewaan per Jam",
    hue="Jenis Pengguna",
    ax=ax4
)

ax4.set_title("Rata-rata Penyewaan Menurut Jenis Pengguna")
ax4.set_xlabel("Jenis Hari")
ax4.set_ylabel("Rata-rata Penyewaan per Jam")
fig4.tight_layout()

st.pyplot(fig4)
plt.close(fig4)


# ==========================================
# 9. TABEL DATA
# ==========================================
with st.expander("Lihat ringkasan data yang difilter"):
    st.write("Ringkasan penyewaan harian")
    st.dataframe(
        day_filtered[
            ["dteday", "Musim", "Kondisi Cuaca", "casual",
             "registered", "cnt"]
        ].reset_index(drop=True),
        use_container_width=True
    )

    st.write("Rata-rata penyewaan per jam")
    st.dataframe(
        hourly_summary,
        use_container_width=True
    )

st.caption("Bike Sharing Data Analysis | Dataset periode 2011–2012")