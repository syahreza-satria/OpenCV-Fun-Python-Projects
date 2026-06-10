import cv2
from cvzone.HandTrackingModule import HandDetector
import pyttsx3
import threading
import queue

# Queue untuk antrean teks yang akan diucapkan
speech_queue = queue.Queue()

def speech_worker():
    # Inisialisasi engine sekali di dalam thread ini
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
    except Exception as e:
        print(f"Error initializing TTS engine: {e}")
        return

    while True:
        text = speech_queue.get()
        if text is None:
            break
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error during speaking: {e}")
        speech_queue.task_done()

# Jalankan worker thread sejak awal secara background (daemon)
worker_thread = threading.Thread(target=speech_worker, daemon=True)
worker_thread.start()

def speak_async(text):
    # Kosongkan antrean lama agar suara tidak menumpuk terlalu banyak saat jari berubah cepat
    while not speech_queue.empty():
        try:
            speech_queue.get_nowait()
            speech_queue.task_done()
        except queue.Empty:
            break
            
    speech_queue.put(text)

# 1. Setup Kamera
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Lebar kamera
cap.set(4, 720)  # Tinggi kamera

# 2. Setup Detektor Tangan
detector = HandDetector(detectionCon=0.8, maxHands=2)

last_finger_count = -1

print("Tekan tombol 'q' di keyboard untuk keluar.")

while True:
    success, img = cap.read()
    if not success:
        print("Gagal membaca kamera.")
        break
        
    # Balik gambar secara horizontal (efek cermin)
    img = cv2.flip(img, 1)
    
    # flipType=False agar detector menunjukkan label tangan yang benar secara fisik (Kiri tetap Kiri, Kanan tetap Kanan)
    hands, img = detector.findHands(img, draw=True, flipType=False) 

    if hands:
        total_fingers = 0
        for hand in hands:
            # Karena gambar di-flip secara horizontal, arah koordinat X jempol terbalik.
            # Kita buat salinan data tangan dan balikkan tipe tangannya ("Left" <-> "Right") 
            # hanya untuk perhitungan fingersUp agar deteksi jempolnya akurat.
            temp_hand = hand.copy()
            temp_hand["type"] = "Left" if hand["type"] == "Right" else "Right"
            
            fingers = detector.fingersUp(temp_hand)
            total_fingers += fingers.count(1)
        
        cv2.putText(img, f'Jari: {total_fingers}', (50, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

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
        last_finger_count = -1

    cv2.imshow("Kamera Pintar", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Hentikan worker thread dengan mengirim None
speech_queue.put(None)
cap.release()
cv2.destroyAllWindows()