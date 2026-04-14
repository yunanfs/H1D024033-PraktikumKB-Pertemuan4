import tkinter as tk
from tkinter import messagebox, font

# ============================================================
# KNOWLEDGE BASE 
# ============================================================
KNOWLEDGE_BASE = {
    "RAM Rusak": {
        "gejala": {"komputer_restart_tiba_tiba", "blue_screen_bsod", "beep_panjang_saat_booting", "aplikasi_sering_crash"},
        "solusi": ["🔧 Bersihkan pin RAM dengan penghapus pensil.", "🔄 Coba pasang satu keping RAM saja."],
        "icon": "💾", "color": "#00d4ff"
    },
    "Overheat Prosesor": {
        "gejala": {"komputer_mati_mendadak", "kipas_berputar_kencang", "badan_laptop_sangat_panas", "blue_screen_bsod"},
        "solusi": ["🌬️ Bersihkan debu pada heatsink & kipas.", "🧴 Ganti thermal paste prosesor."],
        "icon": "🔥", "color": "#ef4444"
    },
    "Harddisk Rusak": {
        "gejala": {"komputer_sangat_lambat", "suara_klik_dari_harddisk", "windows_gagal_booting", "file_tidak_bisa_dibuka"},
        "solusi": ["💾 Segera backup data penting!", "🔍 Cek kesehatan dengan CrystalDiskInfo."],
        "icon": "🗄️", "color": "#f59e0b"
    },
    "VGA Bermasalah": {
        "gejala": {"artefak_visual_di_layar", "layar_tiba_tiba_hitam", "game_crash_sering", "driver_vga_error"},
        "solusi": ["🔄 Reinstall driver GPU resmi.", "🌡️ Cek suhu GPU saat load berat."],
        "icon": "🖥️", "color": "#10b981"
    },
    "PSU Lemah": {
        "gejala": {"komputer_tidak_mau_menyala", "komputer_mati_mendadak", "kipas_berputar_sebentar_lalu_mati"},
        "solusi": ["🔌 Cek kabel power & konektor.", "🆕 Ganti PSU dengan unit berkualitas."],
        "icon": "⚡", "color": "#7c3aed"
    }
}

GEJALA_LABELS = {
    "komputer_restart_tiba_tiba": "Komputer restart tiba-tiba",
    "blue_screen_bsod": "Blue Screen (BSOD)",
    "beep_panjang_saat_booting": "Bunyi beep panjang saat booting",
    "aplikasi_sering_crash": "Aplikasi sering crash",
    "komputer_mati_mendadak": "Komputer mati mendadak",
    "kipas_berputar_kencang": "Kipas sangat kencang/berisik",
    "badan_laptop_sangat_panas": "Laptop terasa sangat panas",
    "komputer_sangat_lambat": "Sangat lambat/lemot",
    "suara_klik_dari_harddisk": "Suara klik dari dalam PC",
    "windows_gagal_booting": "Gagal masuk ke Windows",
    "file_tidak_bisa_dibuka": "File sering korup/rusak",
    "artefak_visual_di_layar": "Garis/titik aneh di layar",
    "layar_tiba_tiba_hitam": "Layar mati tiba-tiba",
    "game_crash_sering": "Game sering keluar sendiri",
    "driver_vga_error": "Error driver grafis",
    "komputer_tidak_mau_menyala": "PC tidak mau hidup",
    "kipas_berputar_sebentar_lalu_mati": "Hidup sebentar lalu mati",
}

class EkspertApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pakar Diagnosa Komputer")
        self.root.geometry("1100x750")
        self.root.configure(bg="#0d0f1a")
        
        # Pengaturan Font
        self.f_ui = ("Segoe UI", 12)
        self.f_bold = ("Segoe UI", 13, "bold")
        self.f_header = ("Segoe UI", 20, "bold")
        
        # State: Menyimpan status checkbox dan list widget
        self.gejala_vars = {k: tk.BooleanVar() for k in GEJALA_LABELS}
        self.checkbox_widgets = {} # Untuk keperluan pencarian/filtering

        self._build_ui()

    def _build_ui(self):
        # Header
        head = tk.Frame(self.root, bg="#131626", height=80)
        head.pack(fill="x")
        tk.Label(head, text="⚡ SISTEM DIAGNOSA KOMPUTER", fg="#00d4ff", bg="#131626", font=self.f_header).pack(pady=20)

        # Main Body
        body = tk.Frame(self.root, bg="#0d0f1a")
        body.pack(fill="both", expand=True, padx=20, pady=10)

        # --- PANEL KIRI: GEJALA ---
        left = tk.Frame(body, bg="#1a1d2e", padx=15, pady=15, highlightthickness=1, highlightbackground="#2a2f4e")
        left.pack(side="left", fill="both", expand=True)
        
        # Fitur Cari
        search_frame = tk.Frame(left, bg="#1a1d2e")
        search_frame.pack(fill="x", pady=(0, 10))
        tk.Label(search_frame, text="🔍 CARI GEJALA:", fg="#94a3b8", bg="#1a1d2e", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        self.entry_search = tk.Entry(search_frame, bg="#0d0f1a", fg="#e2e8f0", font=self.f_ui, insertbackground="#00d4ff", relief="flat")
        self.entry_search.pack(fill="x", pady=5, ipady=5)
        self.entry_search.bind("<KeyRelease>", self._filter_gejala)

        # Scrollable Area
        canvas_frame = tk.Frame(left, bg="#1a1d2e")
        canvas_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#1a1d2e", highlightthickness=0)
        sb = tk.Scrollbar(canvas_frame, command=self.canvas.yview)
        self.f_list = tk.Frame(self.canvas, bg="#1a1d2e")
        
        self.canvas.create_window((0,0), window=self.f_list, anchor="nw")
        self.canvas.configure(yscrollcommand=sb.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Render Checkboxes
        self._render_gejala()

        # Tombol Aksi Kiri
        btn_box = tk.Frame(left, bg="#1a1d2e")
        btn_box.pack(fill="x", pady=(15, 0))
        
        tk.Button(btn_box, text="⟳ RESET", font=self.f_bold, bg="#334155", fg="white", relief="flat", command=self.reset).pack(side="left", fill="x", expand=True, padx=(0,5))
        tk.Button(btn_box, text="🔍 DIAGNOSA", font=self.f_bold, bg="#00d4ff", fg="#0d0f1a", relief="flat", command=self.diagnosa).pack(side="left", fill="x", expand=True, padx=(5,0))

        # --- PANEL KANAN: HASIL ---
        right_frame = tk.Frame(body, bg="#131626", highlightthickness=1, highlightbackground="#2a2f4e")
        right_frame.pack(side="left", fill="both", expand=True, padx=(20, 0))
        
        tk.Label(right_frame, text="📊 HASIL ANALISIS", fg="#7c3aed", bg="#131626", font=self.f_bold, pady=10).pack(fill="x")
        
        self.output = tk.Text(right_frame, bg="#131626", fg="#e2e8f0", font=self.f_ui, relief="flat", padx=15, pady=10)
        self.output.pack(fill="both", expand=True)
        self.output.insert("1.0", "Pilih gejala di sebelah kiri untuk memulai...")
        self.output.config(state="disabled")

    def _render_gejala(self, filter_text=""):
        # Hapus widget lama
        for widget in self.f_list.winfo_children():
            widget.destroy()
        
        for k, label in GEJALA_LABELS.items():
            if filter_text.lower() in label.lower():
                cb = tk.Checkbutton(self.f_list, text=label, variable=self.gejala_vars[k], 
                                   bg="#1a1d2e", fg="#e2e8f0", selectcolor="#0d0f1a", 
                                   activebackground="#00d4ff", font=self.f_ui, anchor="w", pady=2)
                cb.pack(fill="x")

        # Update scrollregion
        self.f_list.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _filter_gejala(self, event):
        self._render_gejala(self.entry_search.get())

    def reset(self):
        # Reset variabel
        for v in self.gejala_vars.values():
            v.set(False)
        self.entry_search.delete(0, tk.END)
        self._render_gejala()
        
        # Reset Output
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", "Data direset. Pilih kembali gejala...")
        self.output.config(state="disabled")

    def diagnosa(self):
        terpilih = {k for k, v in self.gejala_vars.items() if v.get()}
        if not terpilih:
            messagebox.showwarning("Peringatan", "Pilih minimal satu gejala!")
            return

        hasil = []
        for nama, data in KNOWLEDGE_BASE.items():
            cocok = terpilih & data["gejala"]
            if cocok:
                score = (len(cocok) / len(data["gejala"])) * 100
                hasil.append((nama, int(score), data))

        hasil.sort(key=lambda x: x[1], reverse=True)
        self._tampilkan_hasil(hasil)

    def _tampilkan_hasil(self, hasil):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        
        if not hasil:
            self.output.insert(tk.END, "❌ HASIL TIDAK DITEMUKAN\n\nGejala tidak terdaftar dalam pola kerusakan database kami.")
        else:
            for nama, score, data in hasil:
                self.output.insert(tk.END, f"{data['icon']} {nama.upper()} ({score}%)\n", "header")
                self.output.insert(tk.END, "💡 SOLUSI:\n", "bold")
                for s in data["solusi"]:
                    self.output.insert(tk.END, f" • {s}\n")
                self.output.insert(tk.END, "\n" + "-"*35 + "\n\n")
        
        # Konfigurasi gaya teks
        self.output.tag_config("header", foreground="#00d4ff", font=("Segoe UI", 16, "bold"))
        self.output.tag_config("bold", font=self.f_bold, foreground="#94a3b8")
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = EkspertApp(root)
    root.mainloop()