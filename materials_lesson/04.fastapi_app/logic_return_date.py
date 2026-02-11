"""
Perbedaan logic untuk cek availability buku
"""

# ============================================================
# OPSI 1: TANPA is None (BUG - SALAH)
# ============================================================


def is_available_buggy(self):
    return not any([record.return_date for record in self.borrowing_records])


"""
BUG: any([record.return_date])
    - any() cek "truthy" values
    - return_date = None     → False (falsy)
    - return_date = date obj → True  (truthy)

Masalah: Logic kebalikan!
    - Buku SUDAH dikembalikan (return_date = date) → True  ❌
    - Buku MASIH dipinjam (return_date = None)    → False ✅
    
Ini memeriksa "apakah ada return_date?" bukan "apakah ada yang belum dikembalikan?"

Contoh:
    records = [None, date(2024,1,15)]
    [record.return_date for record in records]  # [None, date]
    any([None, date])                           # True (karena date truthy)
    not any(...)                                # False ❌ SALAH! Buku masih dipinjam tapi return False
"""


# ============================================================
# OPSI 2: DENGAN is None (BENAR)
# ============================================================


def is_available_correct(self):
    return not any(record.return_date is None for record in self.borrowing_records)


"""
BENAR: any(record.return_date is None)
    - return_date = None     → True  (buku masih dipinjam)
    - return_date = date obj → False (buku sudah kembali)

Logic yang benar:
    "Return True (available) kalau TIDAK ADA record yang return_date-nya None"
    
Contoh:
    records = [None, date(2024,1,15)]
    [r.return_date is None for r in records]    # [True, False]
    any([True, False])                          # True (ada yang masih dipinjam)
    not any(...)                                # False ✅ BENAR! Buku masih dipinjam

    records = [date(2024,1,1), date(2024,1,15)]
    [r.return_date is None for r in records]    # [False, False]
    any([False, False])                         # False (semua sudah kembali)
    not any(...)                                # True ✅ BENAR! Buku available
"""


# ============================================================
# PERBANDINGAN LANGSUNG
# ============================================================

"""
Skenario: Buku sedang dipinjam (ada 1 record dengan return_date=None)

records = [
    BorrowingRecord(return_date=None),           # Masih dipinjam
    BorrowingRecord(return_date=date(2024,1,1))  # Sudah dikembalikan
]

BUGGY VERSION:
    [record.return_date for record in records]  # [None, date]
    any([None, date])                           # True  (date is truthy)
    not any(...)                                # False ❌ Tapi buku masih dipinjam!

CORRECT VERSION:
    [record.return_date is None for record in records]  # [True, False]
    any([True, False])                                  # True (ada yang is None)
    not any(...)                                        # False ✅ BENAR!
"""


# ============================================================
# KESIMPULAN
# ============================================================

"""
WAJIB pakai `is None` karena:

1. any([record.return_date])     → Cek "apakah ada return_date?" 
                                     (tidak peduli apakah buku available)
                                     
2. any(record.return_date is None) → Cek "apakah ada yang belum dikembalikan?"
                                     (ini yang kita mau)

Penjelasan:
    - `return_date = None` artinya buku masih dipinjam (aktif)
    - Kita mau cek "apakah ada record yang masih aktif?"
    - Jadi pakai `is None`, bukan cek truthy value
"""
