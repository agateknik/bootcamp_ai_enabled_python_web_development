#1 - practical discount calc
price = 1000
discount_percent = 20
is_member = True

##calculate
discount = price * (discount_percent/100)
final_price = price - discount

##memberbonus
if is_member:
    final_price *= 0.95 # kalau member diskon lagi 5%
    
print(f"Harga asli : {price}")
print(f"Harga potongan : {discount}")
print(f"Harga setelah diskon : {final_price}")

print("===========================================================")

#2 - grade calculation
assigment = 80
midterm = 75
final = 90

##calculate weights
grade = (assigment) *0.2 + (midterm*0.3) + (final*0.5)

#determine letter grade
if grade >= 90:
    letter_grade = "A"
elif grade>= 75:
    letter_grade ="B"
elif grade>=60:
    letter_grade="C"
else:
    letter_grade="D"

print(f"Grade anda: {grade:.1f} ({letter_grade})")

print("===========================================================")

#3 - validation check

email ="apman@dev.com"
password="Secret@123"
is_verified= True

##validation
has_at = "@" in email
has_dot = "." in email
password_long = len(password) >= 6
good_char = any(c.isupper() for c in password)

## all checking
all_valid = has_at and has_dot and password_long and good_char and is_verified
if all_valid:
    print("Login successful")
else:
    print("you failed to login")
    

# Ingat 3 Hal Ini:
    # Arithmetic buat math, comparison buat true/false, logical buat combine
    # Gunakan parentheses buat clarity dan override precedence
    # Membership operators buat check apakah item ada di collection

