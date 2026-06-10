import cv2
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# 1. Setup Kamera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# 2. Setup Detektor Tangan
detector = HandDetector(detectionCon=0.7, maxHands=1)

# 3. Setup Audio Windows (Boilerplate Code pycaw)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Mendapatkan range volume laptop (biasanya -65.25 sampai 0.0)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

vol = 0
volBar = 400
volPer = 0

print("Tekan 'q' untuk keluar.")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # Flip biar enak dilihat

    # Temukan tangan
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']

        # Ambil koordinat Jempol (4) dan Telunjuk (8)
        # Ingat trik ambil index 0 dan 1 saja agar aman dari error z-axis
        x1, y1 = lmList[4][0], lmList[4][1]
        x2, y2 = lmList[8][0], lmList[8][1]
        
        # Titik tengah antara jempol dan telunjuk (untuk visualisasi)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Gambar lingkaran di ujung jari
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        # Gambar garis penghubung
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        # Gambar titik tengah
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Hitung jarak (panjang garis)
        length, info, img = detector.findDistance((x1, y1), (x2, y2), img)
        # print(length) # Uncomment ini kalau mau liat angka jaraknya di terminal

        # --- LOGIKA VOLUME (MATEMATIKA) ---
        # Jarak jari biasanya antara 50 (rapat) sampai 300 (lebar banget)
        # Kita harus konversi range [50 - 300] menjadi range volume [minVol - maxVol]
        
        # Fungsi numpy.interp sangat berguna untuk konversi range ini!
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150]) # Untuk gambar bar di layar
        volPer = np.interp(length, [50, 300], [0, 100])   # Untuk angka persen

        # Set Volume Windows
        volume.SetMasterVolumeLevel(vol, None)

        # Visualisasi: Jika jari rapat banget (volume 0), titik tengah jadi hijau
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # --- GAMBAR UI VOLUME BAR ---
    # Kotak frame bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    # Isi bar yang bergerak naik turun
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    # Teks Persentase
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    # Tampilkan FPS (Frame per Second) biar terlihat pro
    cTime = time.time()
    # (Opsional tambahkan logika FPS di sini jika mau)

    cv2.imshow("Gesture Volume Control", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()