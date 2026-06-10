import time
import sys

def lyrics_played():
    lyric = [
        ("Kita hampir mati dan kau selamatkan aku", 0.15),
        ("Dan ku menyelamatkanmu dan sekarang aku tahu\n", 0.10),
        ("CERITA KITA TAK JAUH BERBEDA", 0.25),
        ("Got beat down by the world sometimes I wanna fold", 0.10),
        ("Namun suratmu kan ku ceritakan ke anak-anakku nanti", 0.10),
        ("Bahwa aku pernah dicintai with everything u are", 0.10),
        ("Fully as I am with everything u are", 0.10),
    ]

    for baris, jeda_per_huruf in lyric:
        for karakter in baris:
            sys.stdout.write(karakter)
            sys.stdout.flush()
            time.sleep(jeda_per_huruf)
        print("")
        time.sleep(0.3)

lyrics_played()