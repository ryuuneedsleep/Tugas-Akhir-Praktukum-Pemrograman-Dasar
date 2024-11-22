import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime


class PemesananTiket:
    def __init__(self, root):
        self.root = root
        self.root.title("Pemesanan Tiket Pesawat")
        self.root.geometry("600x650")
        self.root.configure(bg="#f0f8ff")
        self.root.resizable(False, False)

        #Dictionary Rute
        self.penerbangan = {
            "Semarang - Jakarta": 800000,
            "Semarang - Bali": 1700000,
            "Semarang - Palembang": 2200000
        }
        #Dictionary Kelas
        self.kelas = {
            "Ekonomi": 0,
            "Eksekutif": 450000,
            "First Class": 700000,
        }
        #Dictionary Tipe Tiket
        self.tipe_tiket = {
            "Dewasa": 0,
            "Anak-anak": 250000
        }
        #Dictionary Riwayat Pemesanan
        self.riwayat_pemesanan = []

        #GUI
        self.setup_gui()

    def setup_gui(self):
        #Gambar
        image = Image.open("pesawat.PNG")
        image = image.resize((300, 150))
        photo = ImageTk.PhotoImage(image)
        tk.Label(self.root, image=photo, bg="#f0f8ff").pack(pady=10)
        self.photo = photo

        #Form
        self.form_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.form_frame.pack(pady=10, padx=20, fill="both")

        #Nama
        self.add_label("Nama:", 0)
        self.entry_nama = tk.Entry(self.form_frame, width=40, font=("Segoe UI", 10))
        self.entry_nama.grid(row=0, column=1, padx=5, pady=5)

        #Rute
        self.add_label("Rute:", 1)
        self.dropdown_rute = tk.StringVar()
        self.dropdown_rute.set("Pilih Rute")
        tk.OptionMenu(self.form_frame, self.dropdown_rute, *self.penerbangan.keys()).grid(row=1, column=1, padx=5, pady=5)

        #Kelas
        self.add_label("Kelas:", 2)
        self.dropdown_kelas = tk.StringVar()
        self.dropdown_kelas.set("Pilih Kelas")
        tk.OptionMenu(self.form_frame, self.dropdown_kelas, *self.kelas.keys()).grid(row=2, column=1, padx=5, pady=5)

        #Tipe Tiket
        self.add_label("Tipe Tiket:", 3)
        self.tipe_tiket_var = tk.StringVar()
        tk.Radiobutton(self.form_frame, text="Dewasa", variable=self.tipe_tiket_var, value="Dewasa", bg="#f0f8ff").grid(row=3, column=1, padx=5, pady=5, sticky="w")
        tk.Radiobutton(self.form_frame, text="Anak-anak", variable=self.tipe_tiket_var, value="Anak-anak", bg="#f0f8ff").grid(row=4, column=1, padx=5, pady=5, sticky="w")

        #Tanggal
        self.add_label("Jadwal (tanggal-bulan-tahun):", 5)
        self.entry_tanggal = tk.Entry(self.form_frame, width=40, font=("Segoe UI", 10))
        self.entry_tanggal.grid(row=5, column=1, padx=5, pady=5)

        #Tombol Pesan
        self.create_button("Pesan Tiket", self.pesan_tiket, "#007acc", "#003366", 20)
        #Tombol Reset
        self.create_button("Reset", self.reset_form, "#5E1914", "#420D09", 20)

    def add_label(self, text, row):
        tk.Label(self.form_frame, text=text, font=("Segoe UI", 10), bg="#f0f8ff").grid(row=row, column=0, padx=5, pady=5, sticky="w")

    def create_button(self, text, command, color, hover_color, pady):
        button = tk.Button(self.root, text=text, font=("Segoe UI", 12, "bold"), bg=color, fg="white", command=command)
        button.pack(pady=pady)
        button.bind("<Enter>", lambda event : button.configure(bg=hover_color))
        button.bind("<Leave>", lambda event : button.configure(bg=color))

    def pesan_tiket(self):
        nama = self.entry_nama.get()
        rute = self.dropdown_rute.get()
        pilih_kelas = self.dropdown_kelas.get()
        pilih_tiket = self.tipe_tiket_var.get()
        tanggal = self.entry_tanggal.get()

        if not nama or rute == "Pilih Rute" or pilih_kelas == "Pilih Kelas" or not tanggal:
            messagebox.showerror("Error", "Tolong lengkapi semua pilihan Anda!")
            return

        if not nama.replace(" ", "").isalpha():
            messagebox.showerror("Error", "Nama hanya boleh terdiri dari huruf!")
            return

        try:
            datetime.strptime(tanggal, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Error", "Format tanggal salah! Gunakan format: tanggal-bulan-tahun (contoh: 26-12-2006)")
            return

        for pemesanan in self.riwayat_pemesanan:
            if pemesanan["nama"] == nama and pemesanan["rute"] == rute and pemesanan["tanggal"] == tanggal:
                messagebox.showerror("Error",f"Nama '{nama}' sudah memesan tiket untuk rute '{rute}' pada tanggal '{tanggal}'!")
                return

        harga_rute = self.penerbangan.get(rute, 0)
        harga_kelas = self.kelas.get(pilih_kelas, 0)
        harga_tiket = self.tipe_tiket.get(pilih_tiket, 0)
        harga_total = harga_rute + harga_kelas + harga_tiket

        self.riwayat_pemesanan.append({
            "nama": nama,
            "rute": rute,
            "kelas": pilih_kelas,
            "tanggal": tanggal,
            "tipe_tiket": pilih_tiket
        })

        info = (f"Tiket Pesawat\n"
                f"Nama: {nama}\n"
                f"Rute: {rute}\n"
                f"Kelas: {pilih_kelas}\n"
                f"Tipe Tiket: {pilih_tiket}\n"
                f"Tanggal: {tanggal}\n"
                f"Harga Total: Rp {harga_total:,}")

        messagebox.showinfo("Info Pemesanan", info)

    def reset_form(self):
        self.entry_nama.delete(0, tk.END)
        self.dropdown_rute.set("Pilih Rute")
        self.dropdown_kelas.set("Pilih Kelas")
        self.tipe_tiket_var.set("")
        self.entry_tanggal.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PemesananTiket(root)
    root.mainloop()