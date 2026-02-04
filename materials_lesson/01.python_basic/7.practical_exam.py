#case profil pengguna
print("Case Profil Pengguna")
print("="*50)
pengguna = {
    "nama":"apman",
    "email":"apman@dev.com",
    "umur": 36,
    "kota": "Jakarta",
    "is_aktif": True
}

#akses data
print(f"Nama : {pengguna['nama']}")
print(f"Email : {pengguna['email']}")
print(f"Umur : {pengguna['umur']}")
print(f"Kota : {pengguna['kota']}")
print(f"Status : {'Aktif' if pengguna['is_aktif'] else 'Tidak Aktif'}")

print("="*50)
print("Kalkulator BMI")
print("="*50)

#data beberapa orang
data_orang = [
    {"nama": "Andi", "berat": 70, "tinggi":170},
    {"nama": "Budi", "berat": 90, "tinggi":160},
    {"nama": "Citra", "berat": 40, "tinggi":165}
]

def hitung_bmi(berat, tinggi):
    tinggi_m= tinggi / 100  
    bmi = berat / (tinggi_m ** 2)
    return round(bmi, 2)

for orang in data_orang:
    print("Hasil pengecekan BMI : ")
    bmi = hitung_bmi(orang["berat"], orang["tinggi"])
    kategori = ""
    if bmi < 18.5:
        kategori = "Berat Badan Kurang"
    elif 18.5 <= bmi < 25:
        kategori = "Berat Badan Normal"
    elif 25 <= bmi < 30:
        kategori = "Berat Badan Berlebih"
    else:
        kategori = "Obesitas"
    
    print(f"{orang['nama']} - BMI: {bmi} - Kategori: {kategori}")
 
#absensi sederhana
print("="*50)
print("ABSENSI SEDERHANA")
print("="*50)

absensi = {
    "Senin": {"hadir": 25, "sakit": 2, "izin": 1, "alpha": 0},
    "Selasa": {"hadir": 24, "sakit": 1, "izin": 2, "alpha": 1},
    "Rabu": {"hadir": 26, "sakit": 1, "izin": 1, "alpha": 0},
    "Kamis": {"hadir": 23, "sakit": 3, "izin": 1, "alpha": 1},
    "Jumat": {"hadir": 22, "sakit": 2, "izin": 2, "alpha": 2}, 
}

def hitung_total_hadir(data):
    total = 0
    for hari, absen in data.items():
        total += absen["hadir"]
    return total

def hitung_kehadiran_persen(data, total_karyawan):
    total_hadir = hitung_total_hadir(data)
    total_hari = len(data)
    return (total_hadir / (total_karyawan * total_hari)) * 100

def tampilkan_rekap(data):
    print("\n" + "="*60)
    print("REKAP ABSEN MINGGUAN")
    print("="*60)
    print(f"{'HARI':<10} {'HADIR':<8} {'SAKIT':<8} {'IZIN':<8} {'ALPHA':<8}")
    print("-"*60)
    
    for hari, absen in data.items():
        print(f"{hari:<10} {absen['hadir']:<8} {absen['sakit']:<8} {absen['izin']:<8} {absen['alpha']:<8}")
    
    print("-"*60)
    
    total_hadir = hitung_total_hadir(data)
    total_sakit = sum(absen['sakit'] for absen in data.values())
    total_izin = sum(absen['izin'] for absen in data.values())
    total_alpha = sum(absen['alpha'] for absen in data.values())
    
    print(f"{'TOTAL':<10} {total_hadir:<8} {total_sakit:<8} {total_izin:<8} {total_alpha:<8}")
    print("="*60)
def cek_hari_terbaik(data):
    hari_terbaik = None
    hadir_tertinggi = 0
    
    for hari, absen in data.items():
        if absen['hadir'] > hadir_tertinggi:
            hadir_tertinggi = absen['hadir']
            hari_terbaik = hari
    
    return hari_terbaik, hadir_tertinggi
def cek_hari_buruk(data):
    hari_terburuk = None
    alpha_terbanyak = 0
    
    for hari, absen in data.items():
        if absen['alpha'] > alpha_terbanyak:
            alpha_terbanyak = absen['alpha']
            hari_terburuk = hari
    
    return hari_terburuk, alpha_terbanyak
# Jalankan program
total_karyawan = 28
tampilkan_rekap(absensi)
hari_terbaik, tertinggi = cek_hari_terbaik(absensi)
hari_terburuk, alpha_terbanyak = cek_hari_buruk(absensi)
persen_kehadiran = hitung_kehadiran_persen(absensi, total_karyawan)
print(f"\n📊 STATISTIK:")
print(f"- Kehadiran tertinggi: {hari_terbaik} ({tertinggi} orang)")
print(f"- Alpha tertinggi: {hari_terburuk} ({alpha_terbanyak} orang)")
print(f"- Persentase Kehadiran: {persen_kehadiran:.1f}%")



