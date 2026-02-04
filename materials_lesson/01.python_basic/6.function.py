# email validator
def is_valid_email(email):
    """Cek apakah email valid"""
    if "@" not in email:
        return False
    
    if "." not in email:
        return False
    
    return True

emails = [
    "user@example.com",
    "invalid.email",
    "test@domaincouk",
    "another@test.org"
]

for email in emails:
    if is_valid_email(email):
        print(f"{email} is valid")
    else:
        print(f"{email} is invalid")
        
#fungsi cek diskon
print("+"*50)
print("Fugnsi Cek diskon")
print("-"*50)

def hitung_diskon(harga, diskon):
    harga_potongan = harga * (diskon / 100)
    harga_final = harga - harga_potongan
    return harga_final

daftar_belanja = [
    {"nama": "Buku", "harga": 10000, "diskon": 10},
    {"nama": "Pensil", "harga": 2000, "diskon": 5},
    {"nama": "Penghapus", "harga": 1000, "diskon": 5},
]

for belanja in daftar_belanja:
    total_harga = hitung_diskon(belanja["harga"], belanja["diskon"])
    print(f"Pembelian {belanja['nama']} seharga {belanja['harga']}/pcs mendapatkan diskon {belanja['diskon']}%, jadi total yang harus dibayar: {total_harga}")


# Ingat 3 Hal Ini:
    # def buat bikin function, return buat keluarkan hasil
    # Jangan lupa indentation (4 spaces) - ini penting di Python!
    # Parameter buat input, return buat output


