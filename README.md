# Automated Regression Testing - Sistem Pengujian Tanah (Sondir)

Repositori ini berisi skrip otomatisasi pengujian (*Automated Regression Testing*) menggunakan **Python, Pytest, dan Selenium** untuk aplikasi Sistem Informasi Manajemen Pengujian Tanah berbasis Laravel (PPKPL-UAS).

Untuk memastikan pengujian berjalan lancar, Jalankan aplikasi utama (Laravel) beserta data seeder terlebih dahulu sebelum menjalankan skrip Selenium.

---

## Tahap 1: Persiapan Aplikasi Laravel (PPKPL-UAS)

Pastikan komputer sudah terinstall **PHP, Composer, Node.js, dan Database (MySQL/Laragon/XAMPP)**.

1. Buka terminal/CMD dan arahkan ke direktori root proyek Laravel:
   ```bash
   cd path/ke/PPKPL-UAS
   ```

2. Install dependencies PHP dan Node.js:
   ```bash
   composer install
   npm install
   ```

3. Siapkan file konfigurasi lingkungan (Environment):
   - Copy file `.env.example` menjadi `.env`.
   - Sesuaikan konfigurasi database (`DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`) sesuai dengan server lokal.

4. Generate kunci aplikasi:
   ```bash
   php artisan key:generate
   ```

5. Wajib: Jalankan migrasi dan injeksi data awal (Seeder). Hal ini penting agar skrip testing memiliki akun dan data antrean untuk diuji:
   ```bash
   php artisan migrate:fresh --seed
   ```

6. Jalankan compiler asset (Tailwind/Vite) di satu terminal:
   ```bash
   npm run dev
   ```

7. Jalankan server lokal Laravel di terminal baru:
   ```bash
   php artisan serve
   ```
   Pastikan aplikasi berjalan di `http://127.0.0.1:8000`.

## Tahap 2: Persiapan Lingkungan Selenium

Pastikan komputer sudah terinstall Python (versi 3.8+) dan browser Google Chrome.

1. Buka terminal baru dan arahkan ke folder testing ini:
   ```bash
   cd path/ke/PPKPL-UAS/selenium-regression-test
   ```

2. Disarankan membuat dan mengaktifkan Virtual Environment (agar library tidak bentrok dengan proyek Python lain):
   ```bash
   python -m venv venv
   ```

   Cara mengaktifkan di Windows:
   ```bash
   venv\Scripts\activate
   ```

   Cara mengaktifkan di Mac/Linux:
   ```bash
   source venv/bin/activate
   ```

3. Install semua *library* Python yang dibutuhkan dengan menjalankan file `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Tahap 3: Cara Menjalankan Pengujian (Testing)

Sebelum menjalankan pengujian, pastikan server Laravel (`php artisan serve`) sedang aktif berjalan dan tidak ada masalah pada koneksi database.

Pastikan terminalnya berada di dalam folder `selenium-regression-test` dan virtual environment (`venv`) sedang aktif.

1. Menjalankan Seluruh Skenario Test (RG-01 s/d RG-20)

   Jalankan perintah berikut untuk mengeksekusi semua test case secara berurutan:
   ```bash
   pytest test_regression.py -v
   ```

2. Menjalankan Skenario Tertentu Saja

   Jika hanya ingin mengetes satu fitur (misalnya hanya RG-09), gunakan argumen `-k` diikuti nama fungsi test-nya:
   ```bash
   pytest test_regression.py -k "test_rg_09" -v
   ```

   Contoh lain:
   ```bash
   pytest test_regression.py -k "test_rg_05 or test_rg_10" -v
   ```

