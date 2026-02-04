#for lop
for i in range(1,6):
    print(i)
    
produk = ["sabun", "shampoo", "masker", "bedak"]
for p in produk:
    print(p)
    
print("+++++dengan index+++++")
for i, p in enumerate(produk):
    print(f"{i+1}. {p}")
    
#while lop
print("+++++while loop+++++")
i =0 
while i < 5:
    print(i)
    i += 1
print("++++case saldo habis++++")
saldo = 100
while saldo >0:
    print(f"Saldo : {saldo}, masih bisa belanja")
    saldo -= 20
print("Saldo habis, sudah tidak bisa belanja")

print("+++for lop untuk case dictionary/object++++")
user = {"nama":"apman",
        "age":36, 
        "email":"apman@dev.com"
        }

for key , value in user.items():
    print(f"{key}: {value}")
    
#practical
print("-------------------------------------")
print("----print pattern----")
for i in range(1,6):
    print("*" * i)

print("="*50)
while True:
    print("Cek kekuatan password")
    print("tekan 'q' untuk keluar")
    print("+" * 40)
    
    password = input("Masukan password: ")
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    
    if password.lower() == "q":
        print("Keluar dari program. Terima kasih")
        break
    
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif not char.isalnum():
            has_special = True
    
    strength_pass = sum([has_upper, has_lower, has_digit, has_special])
    if strength_pass == 4:
        print("======================")
        print("Password kuat")
        print("======================")
    elif strength_pass == 3:
        print("======================")
        print("Password sedang")
        print("======================")
    else:
        print("======================")
        print("Password lemah")
        print("======================")


# Ingat 3 Hal Ini:
    # for = iterate collection, while = repeat sampai kondisi false
    # Jangan lupa indentation (4 spaces) - ini penting di Python!
    # Gunakan break untuk exit, continue untuk skip