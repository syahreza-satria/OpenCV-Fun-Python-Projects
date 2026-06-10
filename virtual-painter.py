import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# 1. Setup Kamera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

# 2. Variabel Gambar
drawColor = (0, 0, 255) # Warna Merah (Format BGR: Blue, Green, Red)
brushThickness = 15     # Ketebalan kuas
xp, yp = 0, 0           # Koordinat titik sebelumnya (x previous, y previous)

# Membuat Kanvas Hitam kosong (seukuran kamera) untuk tempat menggambar
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

print("Instruksi:")
print("- 1 Jari (Telunjuk): Menggambar")
print("- 2 Jari (Telunjuk + Tengah): Pindah Posisi (Tidak Menggambar)")
print("- Tekan 'c' di keyboard: Hapus semua (Clear)")
print("- Tekan 'q' di keyboard: Keluar")

while True:
    # 1. Import Gambar
    success, img = cap.read()
    img = cv2.flip(img, 1) # Flip agar seperti cermin

    # 2. Temukan Tangan
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        # Ambil koordinat jari telunjuk (titik 8)
        lmList = hands[0]['lmList']
        # Ingat perbaikan sebelumnya: ambil index 0 dan 1 saja (x, y)
        x1, y1 = lmList[8][0], lmList[8][1]  # Ujung Telunjuk
        x2, y2 = lmList[12][0], lmList[12][1] # Ujung Jari Tengah

        # 3. Cek Jari mana yang naik
        fingers = detector.fingersUp(hands[0])
        
        # --- MODE PILIH (Selection Mode) ---
        # Jika dua jari naik (Telunjuk & Tengah), kita TIDAK menggambar
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0 # Reset titik history agar tidak ada garis nyasar
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
            print("Mode: Pindah")

        # --- MODE GAMBAR (Drawing Mode) ---
        # Jika hanya telunjuk yang naik, kita menggambar
        elif fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Mode: Menggambar")

            # Jika ini titik pertama kali terdeteksi, set xp=x1 agar tidak ada garis lurus dari pojok 0,0
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # Gambar garis dari titik lama (xp,yp) ke titik baru (x1,y1)
            # Kita gambar di KANVAS, bukan langsung di kamera agar permanen
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            
            # Update titik lama menjadi titik sekarang untuk frame berikutnya
            xp, yp = x1, y1
        else:
            # Jika jari lainnya, reset history
            xp, yp = 0, 0

    # 4. Menggabungkan Gambar Asli dengan Kanvas
    # Ubah gambar kanvas menjadi abu-abu
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    
    # Buat kebalikannya (Inverse), area hitam jadi putih, area gambar jadi hitam
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    
    # Ubah format imgInv agar bisa dioperasikan dengan warna
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    
    # Ambil bagian asli dari kamera, TAPI hapus bagian yang sudah dicoret (jadi hitam)
    img = cv2.bitwise_and(img, imgInv)
    
    # Tambahkan warna coretan dari kanvas ke gambar asli yang sudah bolong tadi
    img = cv2.bitwise_or(img, imgCanvas)

    # Tampilkan
    cv2.imshow("AI Painter", img)
    # cv2.imshow("Canvas", imgCanvas) # Uncomment ini jika ingin melihat kanvas hitamnya saja

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('c'): # Tombol C untuk menghapus
        imgCanvas = np.zeros((720, 1280, 3), np.uint8)

cap.release()
cv2.destroyAllWindows()