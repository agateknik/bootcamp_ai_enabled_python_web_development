#tipe data di python

#string untuk berisi teks
first_name = "Devscale"
last_name = "Indonesia"

#operation pada string 
fullname = first_name + " " + last_name + " adalah lembaga kursus progaming yang keren" # ini teknik concatenation
print(fullname)
print(f"{first_name} {last_name} adalah lembaga kursus programing yang keren") #sekarang pakai teknik ini untuk lebih mudah f"string

#integer
student_amount = 2000

#float
py_version = 3.14

print(f"Lebih dari {student_amount} siswa {first_name} menggunakan bahasa pemograman python versi {py_version}")
a = 0.1
b = 0.2
print(a+b) #hasilnya bukan 0.3
print(round(a+b, 2)) #ini hasilnya 0.3, use method round

#booelan
is_student = True
is_teacher = False

#list 
fruits = ["mango", "apple", "banana"]
number = [2, 4, 6, 8]
mixed = ["apple", 1, "durian", 3] 

print(fruits)
print(number[3])

#dictionary -> key-value pairs , like object di JS
user = {
    "name":"apman", 
    "age": 36,
    "hobby": "coding"
}
print(user)


#tupple yaitu list yang ida bisa diubah (imutable)
coordinates = (10.11, 20.22)
print(coordinates)

#conversion -> merubah tipe data ke tipe data lain
age_str = "25" #awalnya berupa str
print(int(age_str)) #langsung saat print dirubah ke int 


#checking -> untuk cek tipe dari variable yang hasilnya akan selalu boolean
name_office = "devscale ID"
print(type(name_office)) #jawaban str
print(isinstance(name_office, int)) #jawaban false, karena ver name_office bukan int

# Ingat 3 Hal Ini:
    # String untuk text, int untuk numbers, boolean untuk true/false
    # List buat collection, dict buat key-value, tuple buat immutable
    # Gunakan type conversion kalau butuh pindah tipe