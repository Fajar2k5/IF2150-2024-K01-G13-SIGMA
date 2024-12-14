# IF2150-2024-K01-G13-SIGMA
Tugas 8 IF2150 Rekayasa Perangkat Lunak: Implementasi Perangkat Lunak

## Shield’s Inventory Goods Management Assistance (SIGMA)

### Deskripsi Aplikasi
Shield’s Inventory Goods Management Assistance (SIGMA) adalah sebuah perangkat lunak berbasis web yang dibangun untuk membantu manajemen warehouse secara efisien. Perangkat lunak ini  dirancang untuk  membantu pengguna menambahkan data barang dalam database warehouse, mengambil data barang dari database warehouse, mengubah data di database warehouse, dan menghapus data dari database warehouse melalui antarmuka yang mudah digunakan. Perangkat lunak ini juga memungkinkan pengguna untuk melacak dan mengelola barang yang dipindahkan antar warehouse. Selain itu, perangkat lunak ini juga dapat menambahkan dan menghapus warehouse.

### Cara Menjalankan Aplikasi
1. **Kloning Repository**
   ```bash
   git clone https://github.com/Fajar2k5/IF2150-2024-K01-G13-SIGMA.git
   cd IF2150-2024-K01-G13-SIGMA
   ```
2. **Buat Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\activate   # Windows
   ```

3. **Install Dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Menjalankan Aplikasi**
   ```bash
   python src/app/main.py
   ```

### Daftar Modul
1. **Manajemen Akun**
   - Registrasi 
   - Login
   - Edit akun

2. **Manajemen Warehouse**
   - Tambah, ubah, dan hapus data warehouse
   - Menampilkan daftar warehouse
   - Pindahkan barang antar warehouse

3. **Manajemen Item**
   - Tambah, ubah, dan hapus data item
   - Menampilkan daftar item

### Daftar Tabel Basis Data
1 Tabel `Warehouse`
| Kolom           | Tipe Data  | Deskripsi               |
|-----------------|------------|-------------------------|
| id              | INTEGER    | Primary Key             |
| name            | TEXT       | Nama warehouse          |
| description     | TEXT       | Deskripsi warehouse     |
| capacity        | REAL       | Kapasitas warehouse     |
| used_capacity   | REAL       | Kapasitas yang terpakai |

2 Tabel `items`
| Kolom           | Tipe Data  | Deskripsi               |
|-----------------|------------|-------------------------|
| id              | INTEGER    | Primary Key             |
| name            | TEXT       | Nama item               |
| description     | TEXT       | Deskripsi item          |
| volume          | INTEGER    | Volume item             |

3 Tabel `warehouseitem`
| Kolom           | Tipe Data  | Deskripsi                |
|-----------------|------------|--------------------------|
| id              | INTEGER    | Primary Key              |
| warehouse_id    | INTEGER    | Foreign Key ke Warehouse |
| item_id         | INTEGER    | Foreign Key ke Items     |
| quantity        | INTEGER    | Jumlah item              |

4 Tabel `accounts`
| Kolom           | Tipe Data  | Deskripsi               |
|-----------------|------------|-------------------------|
| id              | INTEGER    | Primary Key             |
| username        | TEXT       | Nama user               |
| email           | TEXT       | Email user              |
| password        | TEXT       | Password                |
