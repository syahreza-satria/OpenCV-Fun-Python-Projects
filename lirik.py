import time
import sys

def lyrics_played():
    # Format: (lirik, jeda_per_huruf, jeda_setelah_baris)
    lyric = [
        ("Kita hampir mati dan kau selamatkan aku", 0.08, 1.5),
        ("Dan ku menyelamatkanmu dan sekarang aku tahu", 0.08, 1.2),
        ("CERITA KITA TAK JAUH BERBEDA", 0.11, 1.4),
        ("Got beat down by the world, sometimes I wanna fold", 0.08, 1.0),
        ("Namun suratmu kan kuceritakan ke anak-anakku nanti", 0.07, 1.2),
        ("Bahwa aku pernah dicintai with everything u are", 0.08, 1.0),
        ("Fully as I am with everything u are", 0.08, 2.0),
    ]

    for baris, jeda_per_huruf, jeda_setelah_baris in lyric:
        for karakter in baris:
            sys.stdout.write(karakter)
            sys.stdout.flush()
            time.sleep(jeda_per_huruf)
        print("")
        time.sleep(jeda_setelah_baris)

lyrics_played()