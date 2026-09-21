# LifeCare Italia Medical Flights — sito

Sito one-page per il servizio di trasporto sanitario su voli di linea: rimpatri
dopo infortunio e trasferimenti a medio e lungo raggio, con barella aeronautica
ed équipe medica a bordo.

L'apertura è un'animazione controllata dallo scroll: 124 fotogrammi disegnati su
un canvas a pieno schermo che raccontano il passaggio dal volo di linea alla
cabina attrezzata, con i testi che entrano ed escono in sincrono.

## Struttura

| File | A cosa serve |
|---|---|
| `index.html` | **Il sito.** Documento autonomo, generato. È quello che GitHub Pages serve |
| `template.html` | Il sorgente da modificare: markup, CSS e JavaScript |
| `build.py` | Incorpora gli asset nel template e genera `index.html` |
| `frames/` | I 124 fotogrammi dell'animazione (WebP 1152×648) |
| `cards/` | Immagini delle sezioni servizi e della banda a pieno schermo |
| `assets/og.jpg` | Anteprima mostrata quando il link viene condiviso sui social |

## Modificare il sito

Si modifica **sempre `template.html`**, mai `index.html`: quest'ultimo viene
sovrascritto a ogni compilazione.

```bash
python3 build.py
```

Il comando produce due file diversi dallo stesso template:

- `index.html` — documento completo per GitHub Pages, **40 KB**, carica frame e
  immagini come file da `frames/` e `cards/`;
- `site.html` — variante senza `<head>` per l'Artifact su claude.ai, **6,7 MB**,
  con tutti gli asset incorporati come data URI. Non è versionata.

Serve Python 3 con la libreria standard: nessuna dipendenza da installare.

## Come è fatta l'animazione

I 124 fotogrammi finiscono in `window.LC` tramite blocchi `<script>` consecutivi,
ma **cosa contengono quei blocchi dipende dalla versione**:

- in `index.html` sono **percorsi** a `frames/*.webp`, quindi il browser scarica le
  immagini come file separati, in parallelo e mettendole in cache;
- in `site.html` sono **data URI**, perché l'Artifact non può caricare file esterni.

Il canvas viene ridisegnato con `requestAnimationFrame` a ogni variazione dello
scroll, in modalità *cover* (l'immagine riempie sempre lo schermo). Se il
fotogramma richiesto non è ancora decodificato viene disegnato il più vicino
disponibile, così non compaiono mai buchi neri durante lo scorrimento.

**Non c'è nessuna schermata di caricamento.** C'era, e aspettava 30 fotogrammi prima
di scoprire la pagina: con i file separati non serviva più — il primo fotogramma è in
`<link rel="preload">` nell'head e il canvas viene disegnato appena è decodificato.

## Pubblicazione su GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → branch `main`, cartella `/ (root)`.

Il file `.nojekyll` disattiva l'elaborazione Jekyll, che qui non serve.

Per un dominio personalizzato: sempre in Settings → Pages, campo *Custom domain*,
poi si punta il DNS del dominio ai server di GitHub Pages.

## Da completare

- [ ] **Partita IVA** — per un'impresa italiana l'indicazione sul sito è un
      obbligo di legge (art. 35 DPR 633/72). Attualmente assente
- [ ] Collegare il modulo a un servizio form: vedi "Ricevere le richieste"
      qui sotto. Finché non è collegato, apre il client di posta dell'utente
- [ ] Testimonianze reali e autorizzate, se si vuole reintrodurre la sezione
- [ ] Uniformare il marchio: i mezzi e le divise riportano "Life Care Italia",
      il logo del sito "LifeCare Italia"

## Ricevere le richieste del modulo

Il modulo preventivo funziona già: apre il programma di posta dell'utente con
partenza, destinazione, data e telefono precompilati verso `centrale@lifecare-roma.it`.

Per riceverle invece direttamente, senza che l'utente esca dal sito, basta creare
un form su un servizio come [Formspree](https://formspree.io) e incollarne l'URL
in `template.html`, nella riga:

```js
var ENDPOINT='';
```

Da quel momento l'invio avviene in background e la posta resta come rete di
sicurezza se la chiamata fallisce. Dopo la modifica va rilanciato `build.py`.

## Contatti pubblicati sul sito

- Telefono: 06 9838 0428
- Email: centrale@lifecare-roma.it
