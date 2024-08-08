import mysql.connector
import tkinter 
from tkinter import ttk 
from tkinter import messagebox
from tkcalendar import Calendar 

def enter_data():
    accepted = accept_var.get()
    
    if accepted == "Pesanan mu Sudah Diajukan!":
        
        # Info Pelanggan
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        
        if firstname and lastname:
            email = email_label_entry.get()
            umur = umur_spinbox.get()
            telpon = telp_label_entry.get()
            
            # Info Pesanan
            verify_umur = uaccept_var.get()
            pm = mobil_combobox.get()
            jp = jp_spinbox.get()
            sd = tawal_cal.get_date()
            ed = takhir_cal.get_date()
            
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="rental_mobil"
                )
                
                my_cursor = mydb.cursor()
                
                sql = "INSERT INTO `pesanan_pelanggan`(`nama_depan`, `nama_belakang`, `email`, `umur`, `no_telpon`, `jenis_mobil`, `jumlah_penumpang`, `dari`, `sampai`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (firstname, lastname, email, umur, telpon, pm, jp, sd, ed)
                
                my_cursor.execute(sql, val)
                mydb.commit()
                mydb.close()
                
                print("Pesanan mu sudah masuk!")
            except mysql.connector.Error as error:
                print("Error inserting data into MySQL:", error)
                messagebox.showerror("Kebanjiran Pesanan!", "Maaf sudah Full Booked!")
                
            first_name_entry.delete(0, tkinter.END)
            last_name_entry.delete(0, tkinter.END)
            email_label_entry.delete(0, tkinter.END)
            umur_spinbox.delete(0, tkinter.END)
            telp_label_entry.delete(0, tkinter.END)
            mobil_combobox.set("")  # Set combobox to empty string
            jp_spinbox.delete(0, tkinter.END)

        else: 
           tkinter.messagebox.showwarning(title="Harapan Jaya", message="Kamu harus mengisi nama!") 
        
        print("Informasi Pelanggan")
        print("Nama: ", firstname, lastname)
        print("Email: ", email)
        print("Umur: ", umur)
        print("No. Telpon: ", telpon)
        print("-------------------------")
        print("Info Pemesanan")
        print("Konfirmasi Umur: ", verify_umur)
        print("Jenis Mobil yang dipesan: ", pm)
        print("Jumlah Penumpang: ", jp)
        print("Untuk Tanggal", sd, "Sampai", ed)
        print("-------------------------")
        print("PESANAN MU TELAH DI AJUKAN!")
        
    else:
        tkinter.messagebox.showwarning(title="Harapan Jaya", message="Kamu belum menceklis BOX Ajukan Pemesanan")
    
    

window = tkinter.Tk()
window.title("Pusat Rental Mobil Harapan Jaya")

frame = tkinter.Frame(window)
frame.pack()

# INFO PELANGGAN
pelanggan_frame = tkinter.LabelFrame(frame, text="Informasi Pelanggan")
pelanggan_frame.grid(row= 0, column=0, padx=20, pady=10)

first_name_label = tkinter.Label(pelanggan_frame, text="Nama Depan")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(pelanggan_frame, text="Nama Belakang")
last_name_label.grid(row= 0, column=1)

first_name_entry = tkinter.Entry(pelanggan_frame)
last_name_entry = tkinter.Entry(pelanggan_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

email_label = tkinter.Label(pelanggan_frame, text="Email")
email_label_entry = tkinter.Entry (pelanggan_frame)
email_label.grid(row=0, column=2)
email_label_entry.grid(row=1, column=2)

umur_label = tkinter.Label(pelanggan_frame, text="Umur")
umur_spinbox = tkinter.Spinbox(pelanggan_frame, from_=1, to=100)
umur_label.grid(row=2, column=0)
umur_spinbox.grid(row=3, column= 0)

telp_label = tkinter.Label(pelanggan_frame, text="No. Telpon")
telp_label_entry = tkinter.Entry(pelanggan_frame)
telp_label.grid(row=2, column=1)
telp_label_entry.grid(row=3, column=1)


for widget in pelanggan_frame.winfo_children(): 
    widget.grid_configure(padx=10, pady=5)

# PESANAN  
pesanan_frame = tkinter.LabelFrame(frame, text="Informasi Pemesanan")
pesanan_frame.grid(row=1, column=0, sticky="news", padx=30, pady=10)

# verify umur
vu_label = tkinter.Label(pesanan_frame, text="Apakah anda diatas 17 tahun?")
uaccept_var = tkinter.StringVar(value= "Saya masih dibawah umur")
vu_check = tkinter.Checkbutton(pesanan_frame, text="Ya", 
                               variable=uaccept_var, onvalue="Saya sudah atau diatas 17 tahun", offvalue="Saya masih dibawah umur")
vu_label.grid(row=0, column=0)
vu_check.grid(row=1, column=0)

# PESANAN JENIS MOBIL & JUMLAH PENUMPANG
mobil_label = tkinter.Label(pesanan_frame, text="Pesanan Mobil")
mobil_combobox = ttk.Combobox(pesanan_frame, values=["Sedan", "SUV", "MPV", "Crossover", "Hatchbak", "Sport Sedan", "Convertible", "Station Wagon", "Off-road", "Pickup Truck", "Double Cabin", "Elektrik", "Hybrid", "Lcgc"])
mobil_label.grid(row=0, column=1)
mobil_combobox.grid(row=1, column=1)

jp_label = tkinter.Label(pesanan_frame, text="Jumlah Penumpang")
jp_spinbox = tkinter.Spinbox(pesanan_frame, from_=1, to=20)
jp_label.grid(row=0, column=2)
jp_spinbox.grid(row=1, column=2)


for widget in pesanan_frame.winfo_children():
    widget.grid_configure(padx=35, pady=5)

# CONFIRM PEMESANAN
confirm_frame = tkinter.LabelFrame(frame, text="Ajukan Pemesanan")
confirm_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

tawal_label = tkinter.Label(confirm_frame, text="Pilih Tanggal Awal: ")
tawal_cal = Calendar(confirm_frame, date_pattern="dd-mm-y")
tawal_label.grid(row=0, column=0)
tawal_cal.grid(row=1, column=0)

takhir_label = tkinter.Label(confirm_frame, text="Pilih Tanggal Akhir: ")
takhir_cal = Calendar(confirm_frame, date_pattern='dd-mm-y')
takhir_label.grid(row=0, column=1)
takhir_cal.grid(row=1, column=1)

accept_var = tkinter.StringVar(value= "Silahkan Ceklis BOX Ajukan Pemesanan!")
confirm_check = tkinter.Checkbutton(confirm_frame, text="Konfirmasi Pemesanan (setelah diajukan, pemesanan tidak dapat diubah)",
                                    variable=accept_var, onvalue="Pesanan mu Sudah Diajukan!", offvalue="Pesanan mu Tidak Diajukan!")
confirm_check.grid(row=2, column=0)

for widget in confirm_frame.winfo_children():
    widget.grid_configure(padx=25, pady=5)


# BUTTON 
button = tkinter.Button(frame, text="Ajukan Pemesanan", command= enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()