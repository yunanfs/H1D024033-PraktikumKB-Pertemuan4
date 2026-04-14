# Working Memory untuk menyimpan gejala yang dialami pasien [cite: 220]
gejala_pasien = []

def tanya_gejala(kode_gejala, teks_pertanyaan):
    """
    Menampilkan pertanyaan kepada user (Simulasi predikat pertanyaan/1 di Prolog)
    [cite: 224, 250, 251]
    """
    jawaban = input(f"{teks_pertanyaan} (y/t): ").lower()

    # Jika jawaban 'y', masukkan ke dalam list gejala (Simulasi assertz) [cite: 252, 253, 254]
    if jawaban == 'y':
        gejala_pasien.append(kode_gejala)

def jalankan_diagnosa():
    """
    Logika pencocokan gejala dengan jenis penyakit (Simulasi predikat penyakit/1)
    [cite: 271, 274, 279, 284, 290]
    """
    print("\n--- Hasil Analisis Sistem ---")
    terdeteksi = False

    # Check Malaria Tertiana [cite: 274, 275, 276, 277, 278]
    if "nyeri_otot" in gejala_pasien and "muntah" in gejala_pasien and "kejang" in gejala_pasien:
        print(">> Anda terdeteksi: Malaria Tertiana")
        terdeteksi = True

    # Check Malaria Quartana [cite: 279, 280, 281, 282, 283]
    if "nyeri_otot" in gejala_pasien and "menggigil" in gejala_pasien and "tidak_enak_badan" in gejala_pasien:
        print(">> Anda terdeteksi: Malaria Quartana")
        terdeteksi = True

    # Check Malaria Tropika [cite: 284, 285, 286, 287, 288, 289]
    if "keringat_dingin" in gejala_pasien and "sakit_kepala" in gejala_pasien and "mimisan" in gejala_pasien and "mual" in gejala_pasien:
        print(">> Anda terdeteksi: Malaria Tropika")
        terdeteksi = True

    # Jika tidak ada gejala yang cocok dengan aturan di atas [cite: 298, 300]
    if not terdeteksi:
        print(">> Tidak terdeteksi penyakit malaria berdasarkan gejala yang Anda masukkan.")

def main():
    """
    Main loop untuk menjalankan program sistem pakar [cite: 307]
    """
    print("=== SISTEM PAKAR DIAGNOSA MALARIA ===") # [cite: 309]
    print("Jawablah pertanyaan berikut dengan 'y' untuk Ya atau 't' untuk Tidak.\n")

    # Daftar pertanyaan yang diajukan (Simulasi predikat pertanyaan/1)
    # [cite: 225, 227, 229, 231, 233, 244]
    tanya_gejala("nyeri_otot", "Apakah Anda merasa nyeri otot?")
    tanya_gejala("muntah", "Apakah Anda muntah-muntah?")
    tanya_gejala("kejang", "Apakah Anda mengalami kejang-kejang?")
    tanya_gejala("menggigil", "Apakah Anda sering menggigil?")
    tanya_gejala("tidak_enak_badan", "Apakah Anda merasa tidak enak badan?")
    tanya_gejala("demam", "Apakah Anda mengalami demam?")

    # Jalankan diagnosa setelah semua pertanyaan dijawab [cite: 310]
    jalankan_diagnosa()

# Menjalankan program [cite: 317]
if __name__ == "__main__":
    main()