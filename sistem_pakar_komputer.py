import tkinter as tk
from tkinter import ttk, font
import threading
import time
import random

# ============================================================
#  KNOWLEDGE BASE — aturan disimpan dalam Dictionary
# ============================================================
KNOWLEDGE_BASE = {
    "RAM Rusak": {
        "gejala": {
            "komputer_restart_tiba_tiba",
            "blue_screen_bsod",
            "beep_panjang_saat_booting",
            "aplikasi_sering_crash",
            "performa_lambat_tiba_tiba",
        },
        "solusi": [
            "🔧 Lepas & pasang ulang RAM, bersihkan pin dengan penghapus pensil.",
            "🔄 Coba satu keping RAM saja untuk isolasi kerusakan.",
            "🧪 Jalankan Windows Memory Diagnostic (mdsched.exe) untuk cek error.",
            "💡 Jika masih error, pertimbangkan penggantian modul RAM baru.",
        ],
        "deskripsi": "Modul RAM mengalami kerusakan fisik atau error sehingga data tidak terbaca dengan benar.",
        "icon": "💾",
        "severity": "TINGGI",
    },
    "Overheat Prosesor": {
        "gejala": {
            "komputer_mati_mendadak",
            "kipas_berputar_kencang",
            "komputer_lambat_saat_beban_berat",
            "badan_laptop_sangat_panas",
            "blue_screen_bsod",
        },
        "solusi": [
            "🌬️ Bersihkan debu pada heatsink & kipas dengan blower/kuas.",
            "🧴 Ganti thermal paste prosesor yang sudah kering.",
            "📐 Pastikan ventilasi laptop/PC tidak terhalang.",
            "💻 Gunakan cooling pad untuk laptop.",
            "⚙️ Aktifkan power saving mode atau turunkan clock speed di BIOS.",
        ],
        "deskripsi": "Suhu prosesor melampaui batas aman akibat pendinginan yang tidak optimal.",
        "icon": "🔥",
        "severity": "KRITIS",
    },
    "Harddisk Corrupt / Rusak": {
        "gejala": {
            "komputer_sangat_lambat",
            "file_tidak_bisa_dibuka",
            "suara_klik_dari_harddisk",
            "windows_gagal_booting",
            "bad_sector_muncul",
            "performa_lambat_tiba_tiba",
        },
        "solusi": [
            "💾 Segera backup data penting ke drive lain!",
            "🔍 Jalankan CHKDSK /f /r melalui Command Prompt (Admin).",
            "🛠️ Gunakan CrystalDiskInfo untuk cek kesehatan HDD/SSD.",
            "🔄 Jika SSD, lakukan Secure Erase & install ulang OS.",
            "🆕 Pertimbangkan penggantian ke SSD baru untuk performa lebih baik.",
        ],
        "deskripsi": "Harddisk mengalami bad sector, kerusakan mekanis, atau sistem file yang korup.",
        "icon": "🗄️",
        "severity": "KRITIS",
    },
    "VGA / GPU Bermasalah": {
        "gejala": {
            "artefak_visual_di_layar",
            "layar_tiba_tiba_hitam",
            "resolusi_tidak_bisa_diubah",
            "game_crash_sering",
            "driver_vga_error",
            "blue_screen_bsod",
        },
        "solusi": [
            "🔄 Update atau reinstall driver GPU dari website resmi NVIDIA/AMD/Intel.",
            "🧹 Bersihkan slot PCIe dan pin konektor VGA card.",
            "🌡️ Cek suhu GPU menggunakan MSI Afterburner atau GPU-Z.",
            "⚡ Pastikan koneksi kabel power 6/8-pin ke GPU terpasang kuat.",
            "🛠️ Jika integrated GPU, coba disable & enable ulang di Device Manager.",
        ],
        "deskripsi": "Kartu grafis mengalami masalah hardware, driver, atau thermal yang menyebabkan output visual terganggu.",
        "icon": "🖥️",
        "severity": "TINGGI",
    },
    "Power Supply (PSU) Lemah": {
        "gejala": {
            "komputer_tidak_mau_menyala",
            "komputer_mati_mendadak",
            "kipas_berputar_sebentar_lalu_mati",
            "tegangan_tidak_stabil",
            "usb_device_sering_disconnect",
        },
        "solusi": [
            "🔌 Cek kabel power dan pastikan semua konektor terpasang dengan benar.",
            "⚡ Ukur output voltase PSU dengan multimeter (ideal: 12V, 5V, 3.3V).",
            "🧹 Bersihkan debu di dalam PSU (jangan buka unit).",
            "🔁 Test dengan PSU lain yang diketahui berfungsi normal.",
            "🆕 Ganti PSU dengan watt yang cukup (minimal 80 Plus Bronze).",
        ],
        "deskripsi": "Catu daya tidak mampu menyuplai tegangan yang stabil dan cukup untuk komponen PC.",
        "icon": "⚡",
        "severity": "TINGGI",
    },
    "Motherboard Bermasalah": {
        "gejala": {
            "beep_panjang_saat_booting",
            "komputer_tidak_mau_menyala",
            "usb_device_sering_disconnect",
            "komputer_restart_tiba_tiba",
            "komponen_tidak_terdeteksi",
        },
        "solusi": [
            "🔋 Reset CMOS dengan mencabut baterai CMOS 5-10 menit.",
            "🔍 Periksa kapasitor pada motherboard (jika menggembung, perlu diganti).",
            "📋 Cek POST code/beep code sesuai merk motherboard.",
            "🛠️ Update BIOS ke versi terbaru jika ada.",
            "🏭 Bawa ke teknisi untuk pengecekan komponen tingkat lanjut.",
        ],
        "deskripsi": "Papan utama (motherboard) mengalami kerusakan komponen atau jalur sirkuit yang terganggu.",
        "icon": "🔲",
        "severity": "KRITIS",
    },
    "Infeksi Virus / Malware": {
        "gejala": {
            "komputer_sangat_lambat",
            "aplikasi_sering_crash",
            "iklan_muncul_tiba_tiba",
            "file_tidak_bisa_dibuka",
            "cpu_usage_tinggi_tanpa_sebab",
        },
        "solusi": [
            "🛡️ Jalankan full scan dengan Windows Defender atau antivirus terpercaya.",
            "🔍 Gunakan Malwarebytes untuk deep scan malware.",
            "🌐 Periksa browser extensions yang mencurigakan.",
            "🔒 Update Windows dan semua software ke versi terbaru.",
            "💿 Jika parah, pertimbangkan reinstall OS dari clean install.",
        ],
        "deskripsi": "Sistem terinfeksi program berbahaya yang mengganggu performa dan keamanan komputer.",
        "icon": "🦠",
        "severity": "SEDANG",
    },
}

# Mapping gejala ke label tampilan
GEJALA_LABELS = {
    "komputer_restart_tiba_tiba": "Komputer restart tiba-tiba",
    "blue_screen_bsod": "Blue Screen (BSOD)",
    "beep_panjang_saat_booting": "Bunyi beep panjang saat booting",
    "aplikasi_sering_crash": "Aplikasi sering crash/error",
    "performa_lambat_tiba_tiba": "Performa tiba-tiba menjadi lambat",
    "komputer_mati_mendadak": "Komputer mati mendadak",
    "kipas_berputar_kencang": "Kipas berputar sangat kencang",
    "komputer_lambat_saat_beban_berat": "Lambat saat proses berat (gaming/render)",
    "badan_laptop_sangat_panas": "Badan laptop/PC sangat panas",
    "komputer_sangat_lambat": "Komputer sangat lambat",
    "file_tidak_bisa_dibuka": "File tidak bisa dibuka",
    "suara_klik_dari_harddisk": "Terdengar suara klik dari harddisk",
    "windows_gagal_booting": "Windows gagal booting",
    "bad_sector_muncul": "Muncul error bad sector",
    "artefak_visual_di_layar": "Muncul artefak/glitch di layar",
    "layar_tiba_tiba_hitam": "Layar tiba-tiba menjadi hitam",
    "resolusi_tidak_bisa_diubah": "Resolusi layar tidak bisa diubah",
    "game_crash_sering": "Game sering crash",
    "driver_vga_error": "Error pada driver VGA/GPU",
    "komputer_tidak_mau_menyala": "Komputer tidak mau menyala sama sekali",
    "kipas_berputar_sebentar_lalu_mati": "Kipas berputar sebentar lalu mati",
    "tegangan_tidak_stabil": "Tegangan/daya tidak stabil",
    "usb_device_sering_disconnect": "USB device sering disconnect sendiri",
    "komponen_tidak_terdeteksi": "Komponen tidak terdeteksi di sistem",
    "iklan_muncul_tiba_tiba": "Iklan pop-up muncul tiba-tiba",
    "cpu_usage_tinggi_tanpa_sebab": "CPU usage tinggi tanpa alasan",
}

# ============================================================
#  MESIN INFERENSI
# ============================================================
def diagnosa(gejala_terpilih: set) -> list:
    """
    Mencocokkan gejala dengan knowledge base.
    Mengembalikan list hasil diagnosa terurut berdasarkan confidence score.
    """
    if not gejala_terpilih:
        return []

    hasil = []
    for penyakit, data in KNOWLEDGE_BASE.items():
        kecocokan = gejala_terpilih & data["gejala"]
        if kecocokan:
            score = len(kecocokan) / len(data["gejala"])
            hasil.append({
                "penyakit": penyakit,
                "score": score,
                "persen": int(score * 100),
                "kecocokan": len(kecocokan),
                "total_gejala": len(data["gejala"]),
                "solusi": data["solusi"],
                "deskripsi": data["deskripsi"],
                "icon": data["icon"],
                "severity": data["severity"],
            })

    hasil.sort(key=lambda x: x["score"], reverse=True)
    return hasil


# ============================================================
#  GUI APLIKASI
# ============================================================
class SistemPakarApp:
    # Palet warna — dark tech theme
    C = {
        "bg":        "#0d0f1a",
        "panel":     "#131626",
        "card":      "#1a1d2e",
        "border":    "#2a2f4e",
        "accent":    "#00d4ff",
        "accent2":   "#7c3aed",
        "accent3":   "#f59e0b",
        "red":       "#ef4444",
        "green":     "#10b981",
        "yellow":    "#f59e0b",
        "text":      "#e2e8f0",
        "text_dim":  "#64748b",
        "text_mid":  "#94a3b8",
        "hover":     "#1e2235",
        "selected":  "#0e2040",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("⚡ EKSPERT — Sistem Pakar Diagnosa Komputer")
        self.root.geometry("1100x750")
        self.root.configure(bg=self.C["bg"])
        self.root.resizable(True, True)
        self.root.minsize(900, 600)

        self.gejala_vars = {}   # checkbox var per gejala
        self.selected_gejala = set()

        self._setup_fonts()
        self._build_ui()
        self._animate_title()

    # ── fonts ──────────────────────────────────────────────
    def _setup_fonts(self):
        self.f_title  = font.Font(family="Courier New", size=18, weight="bold")
        self.f_header = font.Font(family="Courier New", size=11, weight="bold")
        self.f_body   = font.Font(family="Courier New", size=9)
        self.f_small  = font.Font(family="Courier New", size=8)
        self.f_big    = font.Font(family="Courier New", size=24, weight="bold")
        self.f_card   = font.Font(family="Courier New", size=10, weight="bold")

    # ── layout utama ───────────────────────────────────────
    def _build_ui(self):
        # ── TOP BAR ──
        top = tk.Frame(self.root, bg="#090b14", height=55)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)

        # dekorasi bar kiri
        tk.Frame(top, bg=self.C["accent"], width=4).pack(side="left", fill="y")
        tk.Frame(top, bg=self.C["accent2"], width=2).pack(side="left", fill="y")

        title_frame = tk.Frame(top, bg="#090b14")
        title_frame.pack(side="left", padx=18, pady=8)

        self.title_lbl = tk.Label(title_frame, text="⚡ EKSPERT",
                                  font=self.f_title, fg=self.C["accent"],
                                  bg="#090b14")
        self.title_lbl.pack(side="left")
        tk.Label(title_frame, text=" // Sistem Pakar Diagnosa Komputer",
                 font=self.f_header, fg=self.C["text_mid"],
                 bg="#090b14").pack(side="left")

        # status pills
        pill_frame = tk.Frame(top, bg="#090b14")
        pill_frame.pack(side="right", padx=16)
        self._pill(pill_frame, "● ONLINE", self.C["green"])
        self._pill(pill_frame, f"{len(KNOWLEDGE_BASE)} PENYAKIT", self.C["accent"])
        self._pill(pill_frame, f"{len(GEJALA_LABELS)} GEJALA", self.C["accent2"])

        # ── MAIN BODY ──
        body = tk.Frame(self.root, bg=self.C["bg"])
        body.pack(fill="both", expand=True, padx=14, pady=10)

        # Kiri: panel gejala
        left = tk.Frame(body, bg=self.C["panel"],
                        highlightbackground=self.C["border"],
                        highlightthickness=1)
        left.pack(side="left", fill="both", padx=(0, 7), pady=0)
        left.pack_propagate(False)
        left.configure(width=410)

        self._build_symptom_panel(left)

        # Kanan: panel hasil
        right = tk.Frame(body, bg=self.C["panel"],
                         highlightbackground=self.C["border"],
                         highlightthickness=1)
        right.pack(side="left", fill="both", expand=True)

        self._build_result_panel(right)

    def _pill(self, parent, text, color):
        f = tk.Frame(parent, bg=color, padx=8, pady=2)
        f.pack(side="left", padx=4, pady=14)
        tk.Label(f, text=text, font=self.f_small,
                 fg="#000", bg=color, fontmap=None).pack()

    # ── PANEL GEJALA ───────────────────────────────────────
    def _build_symptom_panel(self, parent):
        # Header
        hdr = tk.Frame(parent, bg="#0d0f1a", height=42)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Frame(hdr, bg=self.C["accent"], width=3).pack(side="left", fill="y")
        tk.Label(hdr, text="  📋 PILIH GEJALA", font=self.f_header,
                 fg=self.C["accent"], bg="#0d0f1a").pack(side="left", pady=10)

        self.count_lbl = tk.Label(hdr, text="[0 dipilih]", font=self.f_small,
                                  fg=self.C["text_dim"], bg="#0d0f1a")
        self.count_lbl.pack(side="right", padx=12)

        # Search
        sf = tk.Frame(parent, bg=self.C["panel"], pady=8, padx=10)
        sf.pack(fill="x")
        tk.Label(sf, text="CARI:", font=self.f_small,
                 fg=self.C["text_dim"], bg=self.C["panel"]).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter_gejala)
        search_entry = tk.Entry(sf, textvariable=self.search_var,
                                bg=self.C["card"], fg=self.C["text"],
                                insertbackground=self.C["accent"],
                                relief="flat", font=self.f_body,
                                highlightbackground=self.C["border"],
                                highlightthickness=1)
        search_entry.pack(side="left", fill="x", expand=True, padx=(8, 0), ipady=4)

        # Scrollable checkboxes
        scroll_frame = tk.Frame(parent, bg=self.C["panel"])
        scroll_frame.pack(fill="both", expand=True, padx=6, pady=4)

        canvas = tk.Canvas(scroll_frame, bg=self.C["panel"],
                           highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical",
                                 command=canvas.yview,
                                 bg=self.C["panel"])
        self.cb_frame = tk.Frame(canvas, bg=self.C["panel"])
        self.cb_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.cb_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(
            -1 if e.delta > 0 else 1, "units"))

        self.all_checkboxes = []
        self._render_checkboxes(list(GEJALA_LABELS.items()))

        # Tombol bawah
        btn_frame = tk.Frame(parent, bg=self.C["panel"], pady=10, padx=10)
        btn_frame.pack(fill="x")

        self._btn(btn_frame, "⟳  RESET", self._reset, self.C["text_dim"],
                  side="left")
        self._btn(btn_frame, "✓  PILIH SEMUA", self._select_all,
                  self.C["accent2"], side="left", padx=6)
        self._btn(btn_frame, "🔍  DIAGNOSA", self._run_diagnosa,
                  self.C["accent"], side="right", bold=True)

    def _render_checkboxes(self, items):
        for w in self.cb_frame.winfo_children():
            w.destroy()
        self.all_checkboxes.clear()

        for key, label in items:
            if key not in self.gejala_vars:
                self.gejala_vars[key] = tk.BooleanVar(value=key in self.selected_gejala)

            row = tk.Frame(self.cb_frame, bg=self.C["panel"], pady=1)
            row.pack(fill="x", padx=6)

            cb = tk.Checkbutton(
                row, text=f"  {label}",
                variable=self.gejala_vars[key],
                onvalue=True, offvalue=False,
                bg=self.C["panel"],
                fg=self.C["text"],
                selectcolor=self.C["selected"],
                activebackground=self.C["hover"],
                activeforeground=self.C["accent"],
                font=self.f_body,
                anchor="w",
                cursor="hand2",
                command=self._update_count,
            )
            cb.pack(fill="x")
            self.all_checkboxes.append((key, cb))

            # Hover effect
            row.bind("<Enter>", lambda e, r=row: r.configure(bg=self.C["hover"]))
            row.bind("<Leave>", lambda e, r=row: r.configure(bg=self.C["panel"]))

    def _filter_gejala(self, *_):
        q = self.search_var.get().lower()
        filtered = [(k, v) for k, v in GEJALA_LABELS.items()
                    if q in v.lower() or q in k.lower()]
        self._render_checkboxes(filtered)

    def _btn(self, parent, text, cmd, color, side="left",
             padx=0, bold=False):
        f_use = font.Font(family="Courier New", size=9,
                          weight="bold" if bold else "normal")
        b = tk.Button(parent, text=text, command=cmd,
                      bg=color if bold else self.C["card"],
                      fg=self.C["bg"] if bold else color,
                      activebackground=color,
                      activeforeground=self.C["bg"],
                      relief="flat", font=f_use,
                      cursor="hand2", padx=12, pady=6,
                      bd=0)
        b.pack(side=side, padx=padx)
        return b

    # ── PANEL HASIL ────────────────────────────────────────
    def _build_result_panel(self, parent):
        hdr = tk.Frame(parent, bg="#0d0f1a", height=42)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Frame(hdr, bg=self.C["accent2"], width=3).pack(side="left", fill="y")
        tk.Label(hdr, text="  📊 HASIL DIAGNOSA", font=self.f_header,
                 fg=self.C["accent2"], bg="#0d0f1a").pack(side="left", pady=10)

        self.result_scroll = tk.Frame(parent, bg=self.C["panel"])
        self.result_scroll.pack(fill="both", expand=True)

        # Canvas + scrollbar
        self.r_canvas = tk.Canvas(self.result_scroll, bg=self.C["panel"],
                                   highlightthickness=0)
        r_scroll = tk.Scrollbar(self.result_scroll, orient="vertical",
                                command=self.r_canvas.yview,
                                bg=self.C["panel"])
        self.r_inner = tk.Frame(self.r_canvas, bg=self.C["panel"])
        self.r_inner.bind("<Configure>",
            lambda e: self.r_canvas.configure(
                scrollregion=self.r_canvas.bbox("all")))
        self.r_canvas.create_window((0, 0), window=self.r_inner, anchor="nw")
        self.r_canvas.configure(yscrollcommand=r_scroll.set)
        self.r_canvas.pack(side="left", fill="both", expand=True)
        r_scroll.pack(side="right", fill="y")
        self.r_canvas.bind_all("<MouseWheel>", lambda e: self.r_canvas.yview_scroll(
            -1 if e.delta > 0 else 1, "units"))

        self._show_welcome()

    def _show_welcome(self):
        for w in self.r_inner.winfo_children():
            w.destroy()

        f = tk.Frame(self.r_inner, bg=self.C["panel"])
        f.pack(expand=True, fill="both", pady=80)

        tk.Label(f, text="⚡", font=font.Font(size=48),
                 bg=self.C["panel"], fg=self.C["accent"]).pack()
        tk.Label(f, text="SISTEM PAKAR SIAP", font=self.f_header,
                 bg=self.C["panel"], fg=self.C["accent"]).pack(pady=4)
        tk.Label(f,
                 text="Pilih gejala yang Anda alami di panel kiri,\nlalu tekan tombol DIAGNOSA.",
                 font=self.f_body, bg=self.C["panel"],
                 fg=self.C["text_dim"], justify="center").pack(pady=8)

        # Stats grid
        stats_f = tk.Frame(f, bg=self.C["panel"])
        stats_f.pack(pady=12)
        for label, val, color in [
            ("PENYAKIT DALAM DB", str(len(KNOWLEDGE_BASE)), self.C["accent"]),
            ("TOTAL GEJALA",      str(len(GEJALA_LABELS)),   self.C["accent2"]),
            ("METODE",            "FORWARD\nCHAINING",        self.C["accent3"]),
        ]:
            box = tk.Frame(stats_f, bg=self.C["card"],
                           highlightbackground=self.C["border"],
                           highlightthickness=1, padx=18, pady=10)
            box.pack(side="left", padx=8)
            tk.Label(box, text=val, font=self.f_big, fg=color,
                     bg=self.C["card"]).pack()
            tk.Label(box, text=label, font=self.f_small,
                     fg=self.C["text_dim"], bg=self.C["card"]).pack()

    # ── AKSI ───────────────────────────────────────────────
    def _update_count(self):
        n = sum(1 for k, v in self.gejala_vars.items() if v.get())
        self.count_lbl.configure(text=f"[{n} dipilih]",
                                  fg=self.C["accent"] if n > 0 else self.C["text_dim"])

    def _reset(self):
        for v in self.gejala_vars.values():
            v.set(False)
        self.search_var.set("")
        self._update_count()
        self._show_welcome()

    def _select_all(self):
        for v in self.gejala_vars.values():
            v.set(True)
        self._update_count()

    def _run_diagnosa(self):
        self.selected_gejala = {k for k, v in self.gejala_vars.items() if v.get()}
        if not self.selected_gejala:
            self._show_error("⚠️ Belum Ada Gejala Dipilih",
                             "Silakan pilih minimal satu gejala terlebih dahulu.")
            return

        # Animasi loading
        self._show_loading()
        threading.Thread(target=self._delayed_diagnosa, daemon=True).start()

    def _delayed_diagnosa(self):
        time.sleep(0.9)   # jeda animasi
        hasil = diagnosa(self.selected_gejala)
        self.root.after(0, lambda: self._show_results(hasil))

    def _show_loading(self):
        for w in self.r_inner.winfo_children():
            w.destroy()
        f = tk.Frame(self.r_inner, bg=self.C["panel"])
        f.pack(expand=True, fill="both", pady=120)
        self.loading_lbl = tk.Label(f, text="🔍 MENGANALISIS...",
                                     font=self.f_header, fg=self.C["accent"],
                                     bg=self.C["panel"])
        self.loading_lbl.pack()
        self._animate_loading(0)

    def _animate_loading(self, step):
        chars = ["▰▱▱▱▱▱▱▱", "▰▰▱▱▱▱▱▱", "▰▰▰▱▱▱▱▱",
                 "▰▰▰▰▱▱▱▱", "▰▰▰▰▰▱▱▱", "▰▰▰▰▰▰▱▱",
                 "▰▰▰▰▰▰▰▱", "▰▰▰▰▰▰▰▰"]
        try:
            self.loading_lbl.configure(text=f"🔍 MENGANALISIS...  {chars[step % 8]}")
            self.root.after(110, lambda: self._animate_loading(step + 1))
        except Exception:
            pass

    def _show_error(self, title, msg):
        for w in self.r_inner.winfo_children():
            w.destroy()
        f = tk.Frame(self.r_inner, bg=self.C["panel"])
        f.pack(expand=True, fill="both", pady=100)
        tk.Label(f, text="⚠️", font=font.Font(size=36),
                 bg=self.C["panel"], fg=self.C["yellow"]).pack()
        tk.Label(f, text=title, font=self.f_header,
                 fg=self.C["yellow"], bg=self.C["panel"]).pack(pady=4)
        tk.Label(f, text=msg, font=self.f_body,
                 fg=self.C["text_dim"], bg=self.C["panel"],
                 justify="center").pack()

    def _show_results(self, hasil):
        for w in self.r_inner.winfo_children():
            w.destroy()

        if not hasil:
            # Tidak ada diagnosa cocok
            f = tk.Frame(self.r_inner, bg=self.C["panel"])
            f.pack(expand=True, fill="both", pady=80)
            tk.Label(f, text="🤔", font=font.Font(size=42),
                     bg=self.C["panel"]).pack()
            tk.Label(f, text="TIDAK ADA KERUSAKAN TERIDENTIFIKASI",
                     font=self.f_header, fg=self.C["yellow"],
                     bg=self.C["panel"]).pack(pady=6)
            tk.Label(f,
                     text=(f"Gejala yang Anda pilih ({len(self.selected_gejala)} gejala) tidak\n"
                           "cocok dengan kerusakan manapun dalam database.\n\n"
                           "Saran: Coba pilih gejala yang lebih spesifik,\n"
                           "atau konsultasikan ke teknisi komputer."),
                     font=self.f_body, fg=self.C["text_mid"],
                     bg=self.C["panel"], justify="center").pack()
            return

        # Header ringkasan
        summary = tk.Frame(self.r_inner, bg=self.C["card"],
                            highlightbackground=self.C["border"],
                            highlightthickness=1)
        summary.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(summary,
                 text=f"  ✅  Ditemukan {len(hasil)} kemungkinan kerusakan dari "
                      f"{len(self.selected_gejala)} gejala yang dipilih",
                 font=self.f_body, fg=self.C["green"],
                 bg=self.C["card"], pady=6).pack(anchor="w")

        for i, h in enumerate(hasil):
            self._result_card(self.r_inner, h, i + 1)

        # Footer
        tk.Label(self.r_inner,
                 text="⚠️  Hasil ini bersifat estimasi. Selalu konsultasikan ke teknisi profesional.",
                 font=self.f_small, fg=self.C["text_dim"],
                 bg=self.C["panel"]).pack(pady=8)

    def _result_card(self, parent, h, rank):
        sev_color = {
            "KRITIS": self.C["red"],
            "TINGGI": self.C["yellow"],
            "SEDANG": self.C["accent"],
        }.get(h["severity"], self.C["text_dim"])

        card = tk.Frame(parent, bg=self.C["card"],
                        highlightbackground=sev_color if rank == 1 else self.C["border"],
                        highlightthickness=2 if rank == 1 else 1)
        card.pack(fill="x", padx=12, pady=5)

        # ── Card header ──
        ch = tk.Frame(card, bg="#0d0f1a")
        ch.pack(fill="x")

        rank_lbl = tk.Label(ch,
                             text=f"  #{rank}",
                             font=self.f_card,
                             fg=self.C["accent"] if rank == 1 else self.C["text_dim"],
                             bg="#0d0f1a", padx=6, pady=8)
        rank_lbl.pack(side="left")

        tk.Label(ch, text=f"{h['icon']}  {h['penyakit']}",
                 font=font.Font(family="Courier New", size=11, weight="bold"),
                 fg=self.C["text"], bg="#0d0f1a",
                 pady=8).pack(side="left", padx=4)

        # Severity badge
        sev_badge = tk.Label(ch, text=f" {h['severity']} ",
                              font=self.f_small, fg="#000",
                              bg=sev_color, padx=4, pady=2)
        sev_badge.pack(side="right", padx=10, pady=10)

        # ── Confidence bar ──
        bar_frame = tk.Frame(card, bg=self.C["card"], pady=4, padx=12)
        bar_frame.pack(fill="x")
        tk.Label(bar_frame,
                 text=f"CONFIDENCE: {h['persen']}%  ({h['kecocokan']}/{h['total_gejala']} gejala cocok)",
                 font=self.f_small, fg=self.C["text_mid"],
                 bg=self.C["card"]).pack(anchor="w")

        bar_bg = tk.Frame(bar_frame, bg=self.C["border"], height=6)
        bar_bg.pack(fill="x", pady=3)
        bar_bg.update_idletasks()
        bar_w = bar_bg.winfo_width() or 400
        fill_w = max(4, int(bar_w * h["score"]))
        tk.Frame(bar_bg, bg=sev_color, height=6, width=fill_w).place(x=0, y=0)

        # ── Deskripsi ──
        tk.Label(card, text=f"  ℹ️  {h['deskripsi']}",
                 font=self.f_body, fg=self.C["text_mid"],
                 bg=self.C["card"], wraplength=560, justify="left",
                 padx=6, pady=4).pack(anchor="w")

        # ── Solusi ──
        sol_hdr = tk.Frame(card, bg=self.C["panel"])
        sol_hdr.pack(fill="x", padx=8, pady=(4, 0))
        tk.Frame(sol_hdr, bg=self.C["accent2"], width=2).pack(side="left", fill="y")
        tk.Label(sol_hdr, text="  SOLUSI YANG DISARANKAN:",
                 font=font.Font(family="Courier New", size=9, weight="bold"),
                 fg=self.C["accent2"], bg=self.C["panel"],
                 pady=4).pack(side="left")

        for sol in h["solusi"]:
            sol_row = tk.Frame(card, bg=self.C["card"])
            sol_row.pack(fill="x", padx=8, pady=1)
            tk.Label(sol_row, text=sol,
                     font=self.f_body, fg=self.C["text"],
                     bg=self.C["card"], wraplength=540,
                     justify="left", padx=8, pady=3).pack(anchor="w")

        tk.Frame(card, bg=self.C["panel"], height=6).pack(fill="x")

    # ── ANIMASI JUDUL ──────────────────────────────────────
    def _animate_title(self):
        colors = [self.C["accent"], "#00aadd", "#0088bb",
                  "#00aadd", self.C["accent"]]
        idx = [0]

        def cycle():
            self.title_lbl.configure(fg=colors[idx[0] % len(colors)])
            idx[0] += 1
            self.root.after(600, cycle)

        cycle()


# ============================================================
#  ENTRY POINT
# ============================================================
def main():
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.25)
    except Exception:
        pass
    app = SistemPakarApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
