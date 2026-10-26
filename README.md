# Časovi pevanja sa Sanjom — novi sajt

Statičan sajt (HTML + CSS + JS), bez servera i baze.

## Stranice
- `index.html` Početna
- `o-sanji.html` O Sanji
- `kursevi.html` Kursevi i cene
- `prijava.html` Prijava (forma — treba je povezati sa servisom za slanje, npr. Formspree)
- `vezbaonica.html` Vežbaonica (interaktivna klavijatura)
- `saveti.html` Pevački saveti (blog) i `clanak.html` (šablon članka)
- `utisci.html` Utisci učenika
- `privatnost.html`, `uslovi.html` Pravne stranice

## Izmene
- Boje i fontovi: vrh fajla `style.css` (blok `:root`)
- Meni, podnožje i sadržaj stranica: `build.py`, pa pokrenuti `python build.py .`
- Klavir i vežbe: `site.js`
