"""
Compila il sito LifeCare Italia Medical Flights.

Produce due file dallo stesso sorgente `template.html`:

  site.html   frammento senza <head> per l'Artifact, con TUTTI gli asset
              incorporati come data URI: un file solo, nessuna dipendenza
  index.html  documento completo per il sito pubblicato, che carica frame e
              immagini come FILE SEPARATI da frames/ e cards/

La differenza conta: incorporare 124 frame in base64 porta index.html a 7 MB,
che il visitatore deve scaricare per intero prima di vedere qualsiasi cosa e
che il browser non può mettere in cache immagine per immagine. Con i file
separati la pagina pesa una quarantina di KB e le immagini arrivano dopo.

Uso:  python3 build.py
"""

import base64, glob, os, json

DESCRIZIONE = ("Trasporto sanitario su voli di linea con barella aeronautica ed equipe medica "
               "a bordo. Rimpatri e trasferimenti a medio e lungo raggio, dal reparto di partenza "
               "a quello di destinazione.")


def b64(percorso, mime=None):
    if mime is None:
        mime = "image/jpeg" if percorso.endswith((".jpg", ".jpeg")) else "image/webp"
    return "data:%s;base64,%s" % (mime, base64.b64encode(open(percorso, "rb").read()).decode())


# ---- composizione ----
frames = sorted(glob.glob("frames/f_*.webp"))
assert len(frames) == 124, "attesi 124 frame, trovati %d" % len(frames)

BLOCCO = 8


def componi(uris, card1, card2, card3, band):
    """Riempie il template con le sorgenti date: data URI oppure percorsi."""
    blocchi = [uris[i:i + BLOCCO] for i in range(0, len(uris), BLOCCO)]
    script_frame = "\n".join(
        "<script>LC.push(%s);</script>" % ",".join(json.dumps(u) for u in b)
        for b in blocchi
    )
    html = open("template.html", encoding="utf-8").read()
    html = html.replace("__TOTAL__", str(len(uris)))
    html = html.replace("__CARD1__", card1)
    html = html.replace("__CARD2__", card2)
    html = html.replace("__CARD3__", card3)
    html = html.replace("__BAND__", band)
    html = html.replace("__FRAME_CHUNKS__", script_frame)
    assert "__" not in html.split("<script>")[0], "e' rimasto un segnaposto non sostituito"
    return html


# versione autonoma: tutto incorporato
html = componi([b64(f) for f in frames], b64("cards/c1.webp"), b64("cards/c2.webp"),
               b64("cards/c3.webp"), b64("cards/band.webp"))

# versione collegata: i file restano file
html_collegato = componi(frames, "cards/c1.webp", "cards/c2.webp",
                         "cards/c3.webp", "cards/band.webp")

# ---- versione Artifact ----
open("site.html", "w", encoding="utf-8").write(html)

# ---- versione autonoma per GitHub Pages ----
taglio = html_collegato.index("</style>") + len("</style>")
testa, corpo = html_collegato[:taglio], html_collegato[taglio:]

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Crect width='64' height='64' rx='14' fill='%232E6BE0'/%3E"
    "%3Cpath d='M28 12h8v16h16v8H36v16h-8V36H12v-8h16z' fill='white'/%3E%3C/svg%3E"
)

documento = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta name="theme-color" content="#050A14">
<link rel="icon" href="{fav}">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="LifeCare Italia Medical Flights">
<meta property="og:title" content="Ci prendiamo cura dei tuoi cari fino a casa">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" as="image" href="frames/f_001.webp">
{testa}
</head>
<body>
{corpo}
</body>
</html>
""".format(desc=DESCRIZIONE, fav=FAVICON, testa=testa, corpo=corpo)

open("index.html", "w", encoding="utf-8").write(documento)

print("frame: %d" % len(frames))
for f in ("site.html", "index.html"):
    print("%-11s %.2f MB" % (f, os.path.getsize(f) / 1024 / 1024))
