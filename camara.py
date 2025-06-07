
try:
    from detectorMano import CVMano

    objeto=CVMano()

    objeto.inicio()
except Exception as e:
    print(e)