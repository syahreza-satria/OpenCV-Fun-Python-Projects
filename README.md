# OpenCV Fun Python Projects

Koleksi script Python interaktif berbasis Computer Vision (OpenCV, CVZone) dan automasi sederhana yang menarik untuk dicoba. Proyek ini mencakup deteksi gerakan tangan (hand gesture control), menggambar virtual, kontrol volume suara, drag-and-drop virtual, hingga animasi penulisan lirik otomatis di terminal.

---

## 📂 Daftar Script & Penjelasan Fungsi

### 1. 🖐️ [hand-tracking.py](hand-tracking.py)
Aplikasi pendeteksi jumlah jari tangan secara real-time menggunakan kamera/webcam. Aplikasi ini diintegrasikan dengan **Text-to-Speech (TTS)** untuk melafalkan jumlah jari secara langsung.
*   **Cara Kerja**: 
    *   Mendeteksi 1 tangan dan menghitung jumlah jari yang terangkat (0 hingga 5).
    *   Mengucapkan angka tersebut menggunakan suara laptop (`pyttsx3`).
    *   Memiliki interaksi khusus: jika terdeteksi 5 jari, suara akan mengucapkan *"Hai Kamu"*, dan jika 0 jari akan mengucapkan *"Nol"*.

### 2. 🎶 [lirik.py](lirik.py)
Program CLI sederhana untuk menampilkan lirik lagu secara dramatis dengan efek mesin ketik (typewriter) yang tersinkronisasi.
*   **Cara Kerja**:
    *   Menampilkan baris demi baris lagu tren dengan jeda waktu per karakter yang disesuaikan agar pas dengan alunan musik aslinya.

### 3. 🖱️ [virtual-drag.py](virtual-drag.py)
Game/alat interaktif untuk memindahkan objek digital di layar webcam menggunakan gerakan jari tangan (virtual drag-and-drop).
*   **Cara Kerja**:
    *   Mendeteksi koordinat ujung jari telunjuk dan jari tengah.
    *   Jika kedua jari didekatkan (seperti menjepit/pinch dengan jarak < 50px), kotak ungu akan berubah warna menjadi hijau dan dapat diseret ke mana saja mengikuti gerakan tangan.

### 4. 🎨 [virtual-painter.py](virtual-painter.py)
Kanvas menggambar virtual di udara menggunakan gerakan jari telunjuk.
*   **Cara Kerja**:
    *   **Mode Menggambar (1 Jari)**: Angkat jari telunjuk saja untuk mulai menggoreskan kuas merah di layar.
    *   **Mode Pindah/Seleksi (2 Jari)**: Angkat jari telunjuk dan tengah secara bersamaan untuk memindahkan kuas tanpa meninggalkan goresan di kanvas.
    *   **Kontrol Keyboard**: Tekan tombol `c` pada keyboard untuk membersihkan layar (clear), dan `q` untuk keluar.

### 5. 🔊 [volume-control.py](volume-control.py)
Mengatur tingkat volume suara sistem operasi Windows menggunakan gestur tangan di depan kamera secara real-time.
*   **Cara Kerja**:
    *   Mendeteksi jarak antara ujung ibu jari (jempol) dan ujung jari telunjuk.
    *   Jarak tersebut dipetakan (mapped) secara dinamis ke rentang volume master Windows (0% - 100%) menggunakan library `pycaw`.
    *   Dilengkapi visualisasi slider bar dan persentase volume secara real-time di layar.

---

## 🛠️ Prasyarat & Cara Instalasi

Pastikan komputer Anda telah terinstal **Python 3.x** dan memiliki webcam yang berfungsi.

### 1. Klon Repositori
Clone repositori ini dan masuk ke direktori proyek:
```bash
git clone https://github.com/syahreza-satria/OpenCV-Fun-Python-Projects.git
cd OpenCV-Fun-Python-Projects
```

### 2. Instal Dependencies/Library yang Diperlukan
Instal seluruh library Python yang dibutuhkan dengan menjalankan perintah berikut di terminal:
```bash
pip install opencv-python numpy cvzone pyttsx3 comtypes pycaw
```

*Keterangan Library Utama:*
*   `opencv-python`: Pengolahan citra dan akses kamera/webcam.
*   `cvzone`: Library pembungkus (wrapper) OpenCV yang mempermudah tracking tangan.
*   `pyttsx3`: Text-to-speech offline untuk konversi teks ke suara.
*   `pycaw`: Python Core Audio Windows Library untuk mengontrol volume Windows.

---

## 🚀 Cara Menjalankan Script

Pilih script yang ingin dijalankan dan eksekusi via terminal. Contoh:

*   **Menjalankan Virtual Painter:**
    ```bash
    python virtual-painter.py
    ```
*   **Menjalankan Gesture Volume Control:**
    ```bash
    python volume-control.py
    ```
*   **Menjalankan Efek Lirik:**
    ```bash
    python lirik.py
    ```

*Catatan: Untuk menutup setiap program visual, Anda dapat menekan tombol `q` pada keyboard saat jendela kamera aktif.*
