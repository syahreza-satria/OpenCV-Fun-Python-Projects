import cv2
from cvzone.HandTrackingModule import HandDetector
import pyttsx3

# 1. Setup Suara (Text to Speech)
engine = pyttsx3.init()
# Mengatur kecepatan bicara (opsional)
engine.setProperty('rate', 150) 

# 2. Setup Kamera
# Angka 0 biasanya kamera laptop bawaan. 
# Jika pakai webcam eksternal usb, coba ganti jadi 1.
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Lebar kamera
cap.set(4, 720)  # Tinggi kamera

# 3. Setup Detektor Tangan
# detectionCon: seberapa yakin AI bahwa itu tangan (0.8 = 80%)
detector = HandDetector(detectionCon=0.8, maxHands=1)

last_finger_count = -1 # Variabel agar suara tidak berulang-ulang

print("Tekan tombol 'q' di keyboard untuk keluar.")

while True:
    # Baca gambar dari kamera
    success, img = cap.read()
    
    # Cari tangan di dalam gambar
    # draw=True artinya gambar garis tulang tangan di layar
    hands, img = detector.findHands(img, draw=True) 

    if hands:
        # Jika tangan terdeteksi, ambil informasi tangan pertama
        hand1 = hands[0] 
        lmList = hand1["lmList"]  # List koordinat 21 titik tangan
        
        # Cek jari mana saja yang naik (returns list [1,0,1,1,1] dll)
        fingers = detector.fingersUp(hand1)
        
        # Hitung total jari yang naik
        total_fingers = fingers.count(1)
        
        # Tampilkan angka di layar
        cv2.putText(img, f'Jari: {total_fingers}', (50, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # Logika Suara: Hanya bicara jika jumlah jari berubah
        if total_fingers != last_finger_count:
            if total_fingers == 0:
                text = "Nol"
            elif total_fingers == 5:
                text = "Hai Kamu"
            else:
                text = str(total_fingers)
            
            print(f"Mengucapkan: {text}")
            engine.say(text)
            engine.runAndWait()
            last_finger_count = total_fingers

    # Tampilkan gambar hasil olahan
    cv2.imshow("Kamera Pintar", img)

    # Cara menutup program: Tekan 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()