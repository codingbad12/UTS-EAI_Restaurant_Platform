# 🍽️ Restaurant Microservices Platform – IAE_V2

## 1. Deskripsi Umum
Project ini merupakan platform sistem restoran berbasis **arsitektur microservices** menggunakan **FastAPI**. Sistem ini dibagi menjadi tiga layanan utama yang masing-masing bertanggung jawab atas domain spesifik: manajemen menu, data pelanggan, dan pemesanan. Dengan pendekatan ini, setiap service dapat dikembangkan, diuji, dan dijalankan secara independen, meningkatkan skalabilitas dan fleksibilitas sistem.

## 2. Layanan yang Digunakan

- **menu_service** (port `8000`): Mengelola kategori dan daftar menu makanan/minuman.
- **customer_service** (port `8001`): Mengelola data pelanggan.
- **order_service** (port `8002`): Mengelola proses pemesanan dan riwayat order pelanggan.

Setiap service berjalan secara independen pada port yang berbeda dan saling berkomunikasi melalui HTTP REST API.

## 3. Alur Komunikasi Antar Layanan

### a) Endpoint `POST` (Penambahan/Pembuatan Data)

| Endpoint | Deskripsi Proses |
|----------|------------------|
| `POST /categories` (8000) | Menambahkan kategori menu baru. |
| `POST /menu-items` (8000) | Menambahkan menu makanan/minuman baru berdasarkan kategori. |
| `POST /customers` (8001) | Mendaftarkan pelanggan baru ke sistem. |
| `POST /orders` (8002) | Membuat pemesanan baru berdasarkan ID pelanggan dan daftar item menu. |

### b) Endpoint `GET` (Pengambilan Data)

| Endpoint | Deskripsi Proses |
|----------|------------------|
| `GET /orders` (8002) | Mengambil semua data pesanan yang telah dilakukan oleh pelanggan. |

## 4. Format Pertukaran Data (JSON)

Semua komunikasi antar layanan menggunakan format data **JSON**. Berikut adalah contoh JSON lengkap yang digunakan dalam proses `POST`:

### 📁 Tambah Kategori (menu_service)
**POST `http://localhost:8000/categories`**
```json
{
  "id": 1,
  "name": "Makanan Utama"
}
```

### 🍜 Tambah Menu Item (menu_service)
**POST `http://localhost:8000/menu-items`**
```json
{
  "id": 10,
  "name": "Nasi Goreng",
  "description": "Nasi goreng spesial",
  "price": 25000,
  "category": "Makanan Utama",
  "available": true
}
```

### 👤 Tambah Pelanggan (customer_service)
**POST `http://localhost:8001/customers`**
```json
{
  "id": 1,
  "name": "Budi",
  "email": "budi@mail.com",
  "phone": "08123456789"
}
```

### 🧾 Buat Order (order_service)
**POST `http://localhost:8002/orders`**
```json
{
  "id": 1,
  "customer_id": 1,
  "items": [
    {
      "menu_item_id": 10,
      "quantity": 2
    }
  ]
}
```

### 📄 Ambil Semua Order
**GET `http://localhost:8002/orders`**

Respons JSON (contoh):
```json
[
  {
    "id": 1,
    "customer_id": 1,
    "items": [
      {
        "menu_item_id": 10,
        "quantity": 2
      }
    ]
  }
]
```

## 5. Ringkasan Peran Tiap Service

- **menu_service**
  - Menyediakan fitur tambah kategori dan tambah item menu.
  - Menyimpan informasi nama, deskripsi, harga, dan status ketersediaan menu.

- **customer_service**
  - Menyimpan dan mengelola data pelanggan seperti nama, email, dan nomor HP.
  - Digunakan sebagai referensi saat melakukan pemesanan.

- **order_service**
  - Memproses dan mencatat order dari pelanggan.
  - Menghubungkan data pelanggan (dari `customer_service`) dan data menu (dari `menu_service`) untuk mencatat transaksi pemesanan.

## 6. Teknologi yang Digunakan

| Teknologi     | Keterangan                                         |
|---------------|----------------------------------------------------|
| **FastAPI**   | Framework utama untuk membangun layanan web service. |
| **Uvicorn**   | ASGI server untuk menjalankan aplikasi FastAPI.   |
| **Python 3.x**| Bahasa pemrograman utama.                         |
| **Postman**   | Digunakan untuk testing endpoint secara manual.   |
| **JSON**      | Format pertukaran data antar service.             |
