import streamlit as st
import pymysql
import pandas as pd


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='rental_mobil'
)

def fetch_pemesanan_data(conn):
    try:
        query = "SELECT * FROM pemesanan"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f'Error fetching pemesanan data: {e}')
        return pd.DataFrame()

def show_pemesanan_page():
    st.title("Daftar Pemesanan")

    # Membuat koneksi ke database MySQL
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='rental_mobil'
    )

    # Memanggil fungsi fetch_pemesanan_data untuk mendapatkan data pemesanan
    df_pemesanan = fetch_pemesanan_data(conn)
    df_pemesanan.columns = ['Nomor Pelanggan', 'Merk Mobil', 'Jumlah Hari', 'Total Biaya', 'Nama Pelanggan', 'No. Telpon', 'NIK KTP', 'Alamat', 'Jaminan', 'Dari', 'Sampai']

    # Menutup koneksi database
    conn.close()

    # Menampilkan tabel data pemesanan menggunakan Streamlit
    if not df_pemesanan.empty:
        st.table(df_pemesanan)
    else:
        st.info("Belum ada data pemesanan.")

    # Tambahan konten atau fungsionalitas...

#Memanggil fungsi show_pemesanan_page untuk menampilkan halaman pemesanan
show_pemesanan_page()
