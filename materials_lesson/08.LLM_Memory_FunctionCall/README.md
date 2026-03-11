# LLM Memory & Function Calling

Modul ini mempelajari implementasi memory management pada LLM dan teknik function calling untuk mengintegrasikan LLM dengan external tools.

## File Overview

### 1. main.py
Implementasi **short memory** dengan kombinasi dua teknik:
- **Summarizing**: Merangkum 10 konteks percakapan terakhir menggunakan LLM
- **Sliding Window**: Mempertahankan 3 konteks percakapan terakhir sebagai konteks detail

Ketika percakapan melebihi 10 pesan, pesan-pesan lama di-rangkum dan hanya 3 pesan terakhir + ringkasan dikirim ke LLM. Ini mengoptimalkan penggunaan context window sambil tetap mempertahankan informasi penting.

### 2. function_call.py
Demonstrasi dasar **function calling** dengan LLM:
- Mendefinisikan custom function `get_weather` untuk mendapatkan informasi cuaca
- Mendaftarkan function sebagai tool ke OpenRouter API
- LLM secara otomatis memilih untuk memanggil function berdasarkan query user
- Mengirim hasil function call kembali ke LLM untuk generating final response

### 3. fc_tavily.py
Implementasi **function calling** dengan external API:
- Mengintegrasikan Tavily Search API untuk pencarian internet
- Mendefinisikan function `search` dengan parameter query
- LLM memanggil function search, lalu mengembalikan hasil pencarian sebagai response

## Prerequisites

- Python 3.13
- OpenRouter API Key
- Tavily API Key (untuk fc_tavily.py)

## Installation

```bash
uv sync
```

## Konfigurasi Environment

Buat file `.env` dengan format:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Cara Menjalankan

```bash
# Running main.py (Memory Management)
python main.py

# Running function_call.py
python function_call.py

# Running fc_tavily.py
python fc_tavily.py
```

## Konsep Utama

### Function Calling
Function calling memungkinkan LLM untuk memanggil external functions/APIs untuk mendapatkan informasi real-time atau melakukan tindakan tertentu. Alur:
1. User mengirim pesan
2. LLM mendeteksi perlu memanggil function
3. Function dipanggil dengan parameter yang sesuai
4. Hasil dikembalikan ke LLM
5. LLM menghasilkan response final

### Memory Management
Untuk menangani percakapan panjang tanpa melebihi context window:
- **Summarizing**: Kompres informasi penting dari percakapan lama
- **Sliding Window**: Selalu pertahankan konteks terbaru
- Kombinasi keduanya memberikan keseimbangan antara konteks dan efisiensi
