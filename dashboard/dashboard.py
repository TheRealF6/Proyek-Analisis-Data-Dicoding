import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
sns.set(style='dark')

# Fungsi untuk memuat data bike sharing
def load_data():
    data = pd.read_csv('main_data.csv')
    data['dteday_x'] = pd.to_datetime(data['dteday_x'])
    return data

# Memuat data
data = load_data()

# Menentukan rentang tanggal minimum dan maksimum
min_date = data['dteday_x'].min().date()
max_date = data['dteday_x'].max().date()

# Sidebar untuk memilih rentang tanggal
with st.sidebar:
    st.title('Pilih Rentang Tanggal')
    start_date, end_date = st.date_input(
        'Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_data = data[(data['dteday_x'].dt.date >= start_date) & (data['dteday_x'].dt.date <= end_date)]

st.title('Dashboard Data Bike Sharing')

# Visualisasi tren penggunaan Bike Sharing
st.subheader('Tren Penggunaan Bike Sharing')
fig, ax = plt.subplots()
sns.lineplot(x='dteday_x', y='cnt_x', data=filtered_data, ax=ax)
plt.xticks(rotation=45)
plt.tight_layout()

# Menghitung total pengguna
total_users = filtered_data['cnt_x'].sum()

# Menemukan tanggal dengan jumlah user terbanyak
peak_date = filtered_data[filtered_data['cnt_x'] == filtered_data['cnt_x'].max()]['dteday_x'].dt.date.iloc[0]
peak_users = filtered_data['cnt_x'].max()

# Menampilkan informasi dengan markdown
st.markdown("""
    **Statistik Penyewaan Sepeda Berbagi:**
    - **Total Pengguna:** `{:,}`
    - **Tanggal Puncak Penyewaan:** `{}`
    - **Jumlah Pengguna pada Tanggal Puncak:** `{:,}`
    """.format(total_users, peak_date.strftime('%Y-%m-%d'), peak_users))

st.pyplot(fig)

# Visualisasi perbandingan antara akhir pekan dan hari kerja
st.subheader('Perbandingan Penggunaan Bike Sharing Antara Hari Kerja dan Akhir Pekan')
fig, ax = plt.subplots()
sns.boxplot(x='workingday_x', y='cnt_x', data=filtered_data, ax=ax)
plt.tight_layout()

# Menghitung statistik untuk akhir pekan dan hari kerja
weekend_data = filtered_data[filtered_data['workingday_x'] == 0]['cnt_x']
weekday_data = filtered_data[filtered_data['workingday_x'] == 1]['cnt_x']

# Menampilkan informasi dengan markdown
st.markdown("""
    ### Statistik Penggunaan Bike Sharing
    **Akhir Pekan:**
    - **Minimum Pengguna:** `{:,.0f}`
    - **Rata-Rata Pengguna:** `{:,.0f}`
    - **Maksimum Pengguna:** `{:,.0f}`
    
    **Hari Kerja:**
    - **Minimum Pengguna:** `{:,.0f}`
    - **Rata-Rata Pengguna:** `{:,.0f}`
    - **Maksimum Pengguna:** `{:,.0f}`
    """.format(weekend_data.min(), weekend_data.mean(), weekend_data.max(),
               weekday_data.min(), weekday_data.mean(), weekday_data.max()))

st.pyplot(fig)

st.caption('Muhammad Fakhri Fadhlurrahman (therealf6)')
