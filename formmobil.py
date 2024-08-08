import streamlit as st
import pymysql

def create_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='rental_mobil'
    )
    return conn

def insert_data(conn, merk, tahun, harga_per_hari, tersedia):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO mobil (merk, tahun, harga_per_hari, tersedia) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (merk, tahun, harga_per_hari, tersedia))
        conn.commit()
        cursor.close()
    except pymysql.Error as e:
        st.error(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

def show_formmobil_page():
    try:
        st.title('Input Data Mobil')
        conn = create_connection()

        if conn:
            merk = st.text_input('Merk:')
            tahun = st.text_input('Tahun:')
            harga_per_hari = st.text_input('Harga per Hari:')
            tersedia = st.text_input('Kesediaan:')

            if st.button('Input Data'):
                if merk and tahun and harga_per_hari is not None:
                    insert_data(conn, merk, tahun, harga_per_hari, tersedia)
                    st.success('Data Berhasil Diinput!')
                else:
                    st.warning('Moohon Isi Dengan Benar...')

            conn.close()
    except Exception as e:
        st.error(f"Data telah terinput")

if __name__ == "__main__":
    show_formmobil_page()
