# Conditional = "Jika... maka...". Cara bikin program buat ngambil keputusan berdasarkan kondisi.

#if statement

umur =17
if umur >= 17:
    print("Anda sudah dewasa")

is_logged_in = True
if is_logged_in:
    print("Anda sudah login, silahkan akses data")
    
saldo= 5000
must_payment = 3000
if saldo >= must_payment:
    print("saldo mencukupi")
    
#if..else...
password = "12345678"
password_in = "11111111"

if password == password_in:
    print ("Login berhasil")
else:
    print("Password salah")
    
stock = 0
if stock>0:
    print("Stok tersedia")
else:
    print("stok kosong")

# if..elif..else
# strukturnya jalankan yang pertama benar, atau yang besar dulu

umur = 60

if umur >= 50:
    print("Anda harus banyak berdoa")
elif umur >= 40:
    print ("Anda sudah masuk usia senja")
elif umur >=17:
    print("Anda sudah harus kerja")
else:
    print("Anda harus rajin sekolah")

#practical 

print("=========================================")

## even /odd checker
while True: 
    print("pengecek bilangan ganjil/genap")
    print("tekan 'q' untuk keluar")
    
    user_input =input("masukan angka: ")
    
    if user_input.lower() =="q":
        print("Keluar dari program. Terima Kasih")
        break
    try:
        number = int(user_input)
        if number % 2 == 0:   #jika dimodulus 2 hasilnya 0, maka bilangan genap
            print("bilangan genap") 
        else:
            print("bilangan ganjil")
    except ValueError:
        print("input harus angka, coba lagi")

##if combine kondisi
print("="*50)

while True:
    print("Validasi pengajuan pinjaman")
    print("tekan 'q' untuk keluar")
    print("-"*50)
    
    usia_input = input("Masukan usia Anda: ")
    if usia_input.lower() == "q":
        print("keluar dari program. Terima kasih")
        break
    
    income_input = input("Masukan pendapatan Anda per bulan: ")
    if income_input.lower() == "q":
        print("keluar dari program. Terima kasih")
        break
    
    #validasi harus berupa angka untuk usia dan income
    try:
        usia = int(usia_input)
        income = int(income_input)
    except ValueError:
        print("usia dan income harus berupa angka")
        continue
    
    #input member
    member_input = input("Apakah anda sudah menjadi anggota ? (y/n)").lower()
    if member_input == "y":
        is_member = True
    elif member_input == "n":
        is_member = False
    else:
        print("input member harus y atau n")
        continue
    
    #validasi pinjaman    
    if usia >= 17 and income >= 3000000:
        print("Anda dapat mengajukan pinjaman")
    elif is_member:
        print("Anda belum dapat mendapatkan pinjaman")
    else:
        print("Anda tidak memiliki keanggotaan")
    

# Ingat 3 Hal Ini:
    # if buat satu kondisi, elif buat multiple, else buat fallback
    # Jangan lupa indentation (4 spaces) - ini penting di Python!
    # Gunakan and/or buat combine kondisi