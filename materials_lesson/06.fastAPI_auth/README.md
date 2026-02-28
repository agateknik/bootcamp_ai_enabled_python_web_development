### Praktek membuat otentikasi dan otorisasi di fastAPI

- Sistem app sederhana task-management
- Menggunakan bcrypt untuk hash.
- Menggunakan python-jose[cryptography] untuk jwt.
- Implementasi role "admin" dan "user".
- Logic:
    -   User hanya bisa akses api/tasks [get, create, update, delete] untuk  tasknya masing-masing.
    -   Endpoint api/users hanya bisa diakses user yang memiliki role "admin".

