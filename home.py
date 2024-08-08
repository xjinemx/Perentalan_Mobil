import streamlit as st
import pandas as pd
import pymysql
from fpdf import FPDF
from datetime import datetime, timedelta
from pemesanan import show_pemesanan_page
from mobil import show_mobil_page
from formmobil import show_formmobil_page

# bg
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://img.freepik.com/premium-photo/car-is-driving-road-red-color-is-from-headlightsfuturistic-innovative-car-generative-ai_76964-12052.jpg");
background-size: cover;
}
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# bg

# Membuat koneksi ke database MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='rental_mobil'
)

# untuk masuk ke database
def insert_user(username, password, cursor):
    # Masukkan data user baru ke dalam tabel
    query = "INSERT INTO login (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    connection.commit()

def authenticate_user(username, password, cursor):
    # Verifikasi keberadaan pengguna dalam database
    query = "SELECT * FROM login WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    return cursor.fetchone() is not None

def fetch_data(conn):
    try:
        df = pd.read_sql_query("SELECT * FROM mobil", conn)
        return df
    except Exception as e:
        st.error(f'Error: {e}')
        return pd.DataFrame()

    
def generate_pdf_and_save_to_database(merk, jumlah_hari, total_biaya, nama_penyewa, no_telepon, nik_ktp, alamat_penyewa, jaminan, tanggal_mulai, tanggal_selesai, cursor):
    # Your existing code for generating PDF
    pdf_filename = generate_pdf(merk, jumlah_hari, total_biaya, nama_penyewa, no_telepon, nik_ktp, alamat_penyewa, jaminan, tanggal_mulai, tanggal_selesai)

    # Save data to the database
    query = "INSERT INTO pemesanan (id, merk, jumlah_hari, total_biaya, nama_penyewa, no_telepon, nik_ktp, alamat_penyewa, jaminan, tanggal_mulai, tanggal_selesai) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (merk, jumlah_hari, total_biaya, nama_penyewa, no_telepon, nik_ktp, alamat_penyewa, jaminan, tanggal_mulai, tanggal_selesai))
    connection.commit()

    return pdf_filename

def generate_pdf(merk, jumlah_hari, total_biaya, nama_penyewa, no_telepon, nik_ktp, alamat_penyewa, jaminan, tanggal_mulai, tanggal_selesai):
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Judul

   # Informasi
    pdf.cell(200, 10, txt="==============================  RENTAL MOBIL ================================", ln=True, align='C')
    pdf.cell(200, 10, txt="=========================  SISTEM PENYEWAAN MOBIL ============================", ln=True, align='C')
    pdf.cell(200, 10, txt="========================= STRUK BUKTI PENYEWA UNTUK MENGAMBIL =========================", ln=True, align='C')

    # Menambahkan beberapa line break untuk memberikan spasi
    pdf.ln(20)

    pdf.cell(200, 10, txt=f'Merk Mobil: {merk}', ln=True)
    pdf.cell(200, 10, txt=f'Jumlah Hari: {jumlah_hari}', ln=True)
    pdf.cell(200, 10, txt=f'Total Biaya: Rp.{total_biaya}', ln=True)
    pdf.cell(200, 10, txt=f'Nama Penyewa: {nama_penyewa}', ln=True)
    pdf.cell(200, 10, txt=f'No Telepon: {no_telepon}', ln=True)
    pdf.cell(200, 10, txt=f'NIK KTP: {nik_ktp}', ln=True)
    pdf.cell(200, 10, txt=f'Alamat: {alamat_penyewa}', ln=True)
    pdf.cell(200, 10, txt=f'Jaminan Yang Diajukan: {jaminan}', ln=True)
    pdf.cell(200, 10, txt=f'Tanggal Mulai: {tanggal_mulai}', ln=True)
    pdf.cell(200, 10, txt=f'Tanggal Selesai: {tanggal_selesai}', ln=True)

    # Menambahkan kalimat terima kasih
    pdf.ln(20)  # Menambahkan spasi sebelum kalimat terima kasih
    pdf.cell(200, 10, txt="TERIMA KASIH SUDAH MENYEWA MOBIL KAMI. HATI HATI BERKENDARA!", ln=True, align='C')

    # Menambahkan line break sebelum kolom tanda tangan
    pdf.ln(10)

    # Menambahkan garis untuk pemakai semua
    pdf.ln(15)  # Menambahkan spasi sebelum garis
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Garis bawah pemakai di kiri bawah

    # Menambahkan garis untuk pemakai di kiri bawah
    # Add text for "Pemakai mobil"
    pdf.cell(180, 10, txt="Jakarta, ..............2023", ln=False, align='R')
    pdf.ln(5)
    pdf.cell(200, 10, txt="Pemakai mobil,", ln=True)
    pdf.ln(20)  # Add space

    # Add a line below "Pemakai" section
    pdf.line(10, pdf.get_y(), 50, pdf.get_y())

    # Add text for "PT. Rental Mobil"
    pdf.cell(180, 10, txt="PT. Rental Mobil", ln=True, align='R')

    # Set cursor position to the top right
    pdf.set_xy(140, pdf.get_y())  

    # Menambahkan garis di bawah nama PT. RENTAL MOBIL
    pdf.line(200, pdf.get_y(), 10, pdf.get_y())  # Line below "PT. RENTAL MOBIL"

    # Menyimpan ke file
    unique_filename = f"Struk_Pemesanan_{merk}_{nama_penyewa}.pdf"
    # Rest of your code to generate the PDF and output it
    pdf.output(unique_filename)
    return unique_filename


def authenticate_user(username, password, cursor):
    # Verifikasi keberadaan pengguna dalam database
    query = "SELECT * FROM login WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    row = cursor.fetchone()

    if row:
        columns = [column[0] for column in cursor.description]
        user_data = dict(zip(columns, row))
        return user_data
    else:
        return None  

def main():
    cursor = connection.cursor()

    st.title("Aplikasi Rental Mobil")

    # Tambahkan variabel status login dan role
    is_logged_in = st.session_state.get("is_logged_in", False)
    user_data = st.session_state.get("user_data", None)

# Form untuk login
    if not is_logged_in:
        def login_page():
            
            st.subheader("Login")
            username = st.text_input("Username:")
            password = st.text_input("Password:", type="password")
            if st.button("Login"):
                user_data = authenticate_user(username, password, cursor)
                if user_data:
                    st.session_state.is_logged_in = True  # Set status login menjadi True
                    st.session_state.user_data = user_data  # Save user data to session state
                    st.success("Login berhasil!")

                    # Redirect to pemesanan page if the user is an ad
                    if user_data['role'] == 'admin':
                        st.session_state.is_admin = True
                        st.stop()

    # Jika sudah login atau setelah login berhasil
    if is_logged_in:
        # Check the user role and show appropriate content
        if user_data['role'] == 'admin':
            st.sidebar.title("Halaman Admin")
            admin_selection = st.sidebar.radio("Choose an option", ["Pemesanan", "Formmobil & Mobil"])
            if admin_selection == "Pemesanan":
                show_pemesanan_page()
            elif admin_selection == "Formmobil & Mobil":
                show_formmobil_page()
                show_mobil_page()
        else:
            show_rental_form(cursor)

    # Button untuk registrasi
    if not is_logged_in:
        def register_page():
            st.subheader("Belum punya akun? Registrasi sekarang!")
            
            # Buat session state jika belum ada
            if "registration_data" not in st.session_state:
                st.session_state.registration_data = {"new_username": "", "new_password": ""}

            new_username = st.text_input("Username baru:", value=st.session_state.registration_data["new_username"])
            new_password = st.text_input("Password baru:", type="password", value=st.session_state.registration_data["new_password"])


            if st.button("Registrasi"):
                # Simpan data input ke dalam session state
                st.session_state.registration_data["new_username"] = new_username
                st.session_state.registration_data["new_password"] = new_password

                # Panggil fungsi insert_user
                insert_user(new_username, new_password, cursor)

                # Berikan pesan keberhasilan
                st.success(f"Akun {new_username} berhasil dibuat!")

        def main():
            st.sidebar.title("LOGIN / REGISTRASI")
            pages = {
                "Login": login_page,
                "Registrasi": register_page
            }
            
            selection = st.sidebar.radio("Pilih", list(pages.keys()))
            page = pages[selection]
            page()
            
        if __name__ == "__main__":
            main()
        
    cursor.close()
    connection.close()

    
def show_rental_form(cursor):
    st.title("Form Rental Mobil")

    # Menampilkan dataframe mobil
    st.subheader('Daftar Mobil Tersedia')
    df_mobil = fetch_data(connection)
    df_mobil.columns = ['No', 'Merk', 'Tahun', 'Harga per Hari', 'Tersedia']


    if not df_mobil.empty:
        st.table(df_mobil)

        # Memasukkan informasi pemesanan dari penggun
        st.subheader('Pesan Mobil')
        merk_options = df_mobil['Merk'].tolist()
        merk = st.selectbox('Pilih Merk Mobil', merk_options)
        
        # Form untuk mengisi informasi penyewa dan pemakaian
        st.subheader('Informasi Penyewa')
        nama_penyewa = st.text_input('Nama Penyewa')
        no_telepon = st.text_input('Nomor Telepon')
        nik_ktp = st.text_input('NIK KTP')
        alamat_penyewa = st.text_area('Alamat Penyewa')
        
        # Membuat jaminan
        options_jaminan = ['Kartu Tanda Penduduk', 'Kartu Keluarga', 'Surat Izin Mengemudi', 'Surat Tanah', 'Pasport']
        jaminan = st.selectbox('Pilih Jaminan:', options_jaminan)

        # Membuat tanggal
        st.subheader('Pemakaian Mobil')
        st.subheader('Rentang Tanggal Pemakaian')
       
        tanggal_mulai_default = datetime.now() + timedelta(days=1)
        tanggal_mulai = st.date_input('Tanggal Mulai', min_value=tanggal_mulai_default, value=tanggal_mulai_default)

        tanggal_selesai_default = tanggal_mulai_default + timedelta(days=1)
        tanggal_selesai = st.date_input('Tanggal Selesai', min_value=tanggal_selesai_default, value=tanggal_selesai_default)

        # Hitung jumlah hari pemakaian
        jumlah_hari_pemakaian = (tanggal_selesai - tanggal_mulai).days + 1

        # Menampilkan total biaya
        harga_per_hari = df_mobil[df_mobil['Merk'] == merk]['Harga per Hari'].values[0]
        total_biaya = harga_per_hari * jumlah_hari_pemakaian

        st.subheader('Total Biaya')
        st.write(f'Total Biaya untuk {jumlah_hari_pemakaian} hari {merk} adalah: Rp.{total_biaya}')

        # Tombol "Pesan" untuk menghasilkan struk PDF
        if st.button("Pesan"):
            pdf_filename = generate_pdf_and_save_to_database(merk, jumlah_hari_pemakaian, total_biaya, nama_penyewa, no_telepon, nik_ktp, alamat_penyewa, jaminan, tanggal_mulai, tanggal_selesai, cursor)
            
            # Tampilkan tautan unduh untuk file PDF
            with open(pdf_filename, "rb") as f:
                pdf_data = f.read()
                st.download_button("Download Struk PDF", pdf_data, file_name=f"Struk_Pemesanan_{merk}_{nama_penyewa}.pdf", key=merk)

            st.success('Struk Pemesanan berhasil dibuat.')

            # Menambahkan langkah-langkah tambahan setelah menampilkan pesan kesuksesan
            st.info("Anda akan dialihkan ke menu utama setelah ini.")
            
            # Menghentikan eksekusi lebih lanjut
            st.stop()

def show_registration_form(cursor):
    st.title("Form Registrasi")

    new_username = st.text_input("Username baru:")
    new_password = st.text_input("Password baru:", type="password")

    if st.button("Registrasi", key="register_button"):
        insert_user(new_username, new_password, cursor)
        st.success(f"Akun {new_username} berhasil dibuat!")


if __name__ == '__main__':
    main()
