import tkinter as tk
from tkinter import messagebox

# KNOWLEDGE BASE: Menyimpan aturan kerusakan, gejala, dan solusi 
# Struktur: "Nama Kerusakan": {"gejala": [list_gejala], "solusi": "teks_solusi"}
knowledge_base = {
    "RAM Rusak/Kotor": {
        "gejala": ["beep_berulang", "layar_blank", "sering_bsod"],
        "solusi": "Lepas RAM, bersihkan pin emasnya menggunakan penghapus pensil, lalu pasang kembali dengan kuat."
    },
    "Power Supply (PSU) Lemah": {
        "gejala": ["sering_restart_sendiri", "pc_tidak_mau_hidup", "bau_hangat_psu"],
        "solusi": "Cek tegangan PSU dengan multitester atau coba ganti dengan PSU cadangan yang normal."
    },
    "Overheat (Prosesor)": {
        "gejala": ["mati_mendadak_saat_berat", "kipas_berisik", "suhu_tinggi"],
        "solusi": "Bersihkan debu pada heatsink dan ganti thermal paste pada prosesor."
    },
    "VGA Bermasalah": {
        "gejala": ["layar_artifak_garis", "driver_sering_crash", "layar_blank"],
        "solusi": "Update driver VGA. Jika masih bermasalah, cek suhu chip VGA atau coba re-seat kabel monitor."
    },
    "Hardisk Corrupt/Rusak": {
        "gejala": ["loading_sangat_lambat", "bunyi_tik_tik", "gagal_booting"],
        "solusi": "Lakukan pengecekan kesehatan disk menggunakan alat seperti CrystalDiskInfo. Segera backup data penting."
    }
}

# DAFTAR GEJALA UNTUK PERTANYAAN [cite: 159, 337]
daftar_pertanyaan = [
    ("beep_berulang", "Apakah terdengar bunyi 'beep' berulang kali?"),
    ("layar_blank", "Apakah layar monitor tetap hitam/blank saat dinyalakan?"),
    ("sering_bsod", "Apakah sistem sering mengalami Blue Screen of Death (BSOD)?"),
    ("sering_restart_sendiri", "Apakah komputer sering restart secara tiba-tiba?"),
    ("pc_tidak_mau_hidup", "Apakah PC sama sekali tidak memberikan tanda kehidupan?"),
    ("bau_hangat_psu", "Apakah tercium aroma komponen terbakar dari arah PSU?"),
    ("mati_mendadak_saat_berat", "Apakah laptop mati mendadak saat menjalankan aplikasi berat/game?"),
    ("kipas_berisik", "Apakah kipas pendingin berputar sangat kencang dan berisik?"),
    ("suhu_tinggi", "Apakah body laptop terasa sangat panas secara tidak wajar?"),
    ("layar_artifak_garis", "Apakah muncul garis-garis atau kotak berwarna (artifak) di layar?"),
    ("driver_sering_crash", "Apakah sering muncul notifikasi driver grafis berhenti bekerja?"),
    ("loading_sangat_lambat", "Apakah proses membuka folder atau file memakan waktu sangat lama?"),
    ("bunyi_tik_tik", "Apakah terdengar bunyi 'tik-tik' atau gesekan dari dalam laptop?"),
    ("gagal_booting", "Apakah muncul pesan 'No Bootable Device' saat menyalakan komputer?")
]

class SistemPakarKomputer:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagnosa Kerusakan Komputer")
        self.gejala_user = []
        self.index = 0

        # UI Elements [cite: 365, 368]
        self.label_tanya = tk.Label(root, text="Klik tombol di bawah untuk mulai diagnosa", 
                                    font=("Arial", 11), wraplength=350)
        self.label_tanya.pack(pady=30)

        self.btn_mulai = tk.Button(root, text="Mulai Diagnosa", command=self.mulai)
        self.btn_mulai.pack(pady=10)

        self.frame_opsi = tk.Frame(root)
        self.btn_ya = tk.Button(self.frame_opsi, text="YA", width=10, command=lambda: self.proses('y'))
        self.btn_tidak = tk.Button(self.frame_opsi, text="TIDAK", width=10, command=lambda: self.proses('t'))
        
        self.btn_ya.pack(side=tk.LEFT, padx=10)
        self.btn_tidak.pack(side=tk.LEFT, padx=10)

    def mulai(self):
        self.gejala_user = []
        self.index = 0
        self.btn_mulai.pack_forget()
        self.frame_opsi.pack(pady=10)
        self.tampilkan_soal()

    def tampilkan_soal(self):
        if self.index < len(daftar_pertanyaan):
            self.label_tanya.config(text=daftar_pertanyaan[self.index][1])
        else:
            self.hitung_hasil()

    def proses(self, jawab):
        if jawab == 'y':
            self.gejala_user.append(daftar_pertanyaan[self.index][0])
        
        self.index += 1
        self.tampilkan_soal()

    def hitung_hasil(self):
        """MESIN INFERENSI: Mencocokkan input dengan Knowledge Base [cite: 437, 465]"""
        hasil_diagnosa = []
        
        for kerusakan, info in knowledge_base.items():
            # Jika semua gejala dalam aturan ada pada input user (Logika AND) [cite: 440]
            if all(g in self.gejala_user for g in info["gejala"]):
                hasil_diagnosa.append((kerusakan, info["solusi"]))

        # Menampilkan Output [cite: 467, 470]
        if hasil_diagnosa:
            pesan = ""
            for h in hasil_diagnosa:
                pesan += f"KERUSAKAN: {h[0]}\nSOLUSI: {h[1]}\n\n"
            messagebox.showinfo("Hasil Analisis", pesan)
        else:
            messagebox.showwarning("Hasil Analisis", "Maaf, gejala tidak cocok dengan kerusakan yang terdaftar.")

        self.frame_opsi.pack_forget()
        self.btn_mulai.pack(pady=10)
        self.label_tanya.config(text="Diagnosa selesai. Ingin cek lagi?")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = SistemPakarKomputer(root)
    root.mainloop()