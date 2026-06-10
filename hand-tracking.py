import cv2
from cvzone.HandTrackingModule import HandDetector
import pyttsx3
import threading

# Fungsi untuk bersuara tanpa memblokir thread utama (camera feed)
def speak_async(text):
    def speech_worker():
        try:
            # Inisialisasi engine di dalam thread untuk menghindari konflik COM Windows
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error running TTS: {e}")

    thread = threading.Thread(target=speech_worker, daemon=True)
    thread.start()

# 1. Setup Kamera
# Angka 0 biasanya kamera laptop bawaan. 
# Jika pakai webcam eksternal usb, coba ganti jadi 1.
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Lebar kamera
cap.set(4, 720)  # Tinggi kamera

# 2. Setup Detektor Tangan
# detectionCon: seberapa yakin AI bahwa itu tangan (0.8 = 80%)
detector = HandDetector(detectionCon=0.8, maxHands=2)

last_finger_count = -1 # Variabel agar suara tidak berulang-ulang

print("Tekan tombol 'q' di keyboard untuk keluar.")

while True:
    # Baca gambar dari kamera
    success, img = cap.read()
    if not success:
        print("Gagal membaca kamera.")
        break
        
    # Balik gambar secara horizontal (efek cermin) agar lebih intuitif
    img = cv2.flip(img, 1)
    
    # Cari tangan di dalam gambar
    # draw=True artinya gambar garis tulang tangan di layar
    # flipType=False karena kita sudah membalik gambarnya secara manual
    hands, img = detector.findHands(img, draw=True, flipType=False) 

    if hands:
        total_fingers = 0
        for hand in hands:
            # Cek jari mana saja yang naik untuk tangan ini
            fingers = detector.fingersUp(hand)
            total_fingers += fingers.count(1)
        
        # Tampilkan angka di layar
        cv2.putText(img, f'Jari: {total_fingers}', (50, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # Logika Suara: Hanya bicara jika jumlah jari berubah
        if total_fingers != last_finger_count:
            if total_fingers == 0:
                text = "Nol"
            elif total_fingers == 5:
                text = "Hai Kamu"
            elif total_fingers == 10:
                text = "Hai Semua"
            else:
                text = str(total_fingers)
            
            print(f"Mengucapkan: {text}")
            speak_async(text)
            last_finger_count = total_fingers
    else:
        # Reset tracker jika tidak ada tangan terdeteksi sama sekali
        last_finger_count = -1

    # Tampilkan gambar hasil olahan
    cv2.imshow("Kamera Pintar", img)

    # Cara menutup program: Tekan 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()