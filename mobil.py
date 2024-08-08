import streamlit as st
import pymysql
import pandas as pd
from formmobil import show_formmobil_page

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='rental_mobil'
)

def fetch_mobil_data(conn):
    try:
        query = "SELECT * FROM mobil"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f'Error fetching mobil data: {e}')
        return pd.DataFrame()

def show_mobil_page():
    st.title("Daftar Ketersediaan Mobil")

    # Membuat koneksi ke database MySQL
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='rental_mobil'
    )

    # Memanggil fungsi fetch_pemesanan_data untuk mendapatkan data pemesanan
    df_mobil = fetch_mobil_data(conn)
    df_mobil.columns = ['No','Merk','Tahun','Harga/hari','Tersedia']

    # Menutup koneksi database
    conn.close()

    # Menampilkan tabel data pemesanan menggunakan Streamlit
    if not df_mobil.empty:
        st.table(df_mobil)
    else:
        st.info("Belum ada data mobil.")

    # Tambahan konten atau fungsionalitas...

#Memanggil fungsi show_pemesanan_page untuk menampilkan halaman pemesanan
if __name__ == "__main__":
    show_mobil_page()
