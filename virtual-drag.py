import cv2
from cvzone.HandTrackingModule import HandDetector

# 1. Setup Kamera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# 2. Setup Detektor
detector = HandDetector(detectionCon=0.8, maxHands=1)

# 3. Variabel Kotak
colorR = (255, 0, 255)

class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # Cek apakah jari ada di dalam area kotak
        # cursor[0] adalah X, cursor[1] adalah Y
        if cx - w // 2 < cursor[0] < cx + w // 2 and \
           cy - h // 2 < cursor[1] < cy + h // 2:
            # REVISI: Ambil hanya index 0 dan 1 agar tidak error 'too many values'
            self.posCenter = [cursor[0], cursor[1]]

rectList = []
for x in range(1):
    rectList.append(DragRect([150, 150]))

print("Tekan 'q' untuk keluar.")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    # Deteksi Tangan
    hands, img = detector.findHands(img, flipType=False) 

    if hands:
        lmList = hands[0]['lmList']
        
        # Ambil koordinat jari telunjuk (8) dan tengah (12)
        x1, y1 = lmList[8][0], lmList[8][1] 
        x2, y2 = lmList[12][0], lmList[12][1]

        # Cari jarak
        length, info, img = detector.findDistance((x1, y1), (x2, y2), img)

        if length < 50:
            cursor = lmList[8] # Ini aslinya [x, y, z]
            for rect in rectList:
                rect.update(cursor) # Masuk ke fungsi update yang sudah diperbaiki
                
                # Gambar kotak hijau (sedang dipegang)
                cv2.rectangle(img, (rect.posCenter[0] - rect.size[0] // 2, rect.posCenter[1] - rect.size[1] // 2),
                              (rect.posCenter[0] + rect.size[0] // 2, rect.posCenter[1] + rect.size[1] // 2),
                              (0, 255, 0), cv2.FILLED)
        else:
             # Gambar kotak ungu (idle)
             for rect in rectList:
                cv2.rectangle(img, (rect.posCenter[0] - rect.size[0] // 2, rect.posCenter[1] - rect.size[1] // 2),
                              (rect.posCenter[0] + rect.size[0] // 2, rect.posCenter[1] + rect.size[1] // 2),
                              colorR, cv2.FILLED)
    
    # Jika tangan tidak terdeteksi, tetap gambar kotak agar tidak hilang
    if not hands:
        for rect in rectList:
            cv2.rectangle(img, (rect.posCenter[0] - rect.size[0] // 2, rect.posCenter[1] - rect.size[1] // 2),
                              (rect.posCenter[0] + rect.size[0] // 2, rect.posCenter[1] + rect.size[1] // 2),
                              colorR, cv2.FILLED)

    cv2.imshow("Drag and Drop Virtual", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()