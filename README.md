# Časovi pevanja sa Sanjom — novi sajt

Statičan sajt (HTML + CSS + JS), bez servera i baze, na tri jezika:
srpski u korenu, engleski u `en/`, nemački u `de/`.

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
- Meni, podnožje i sadržaj stranica: `build.py` (svaki tekst je `t("srpski", "English", "Deutsch")`), pa pokrenuti `python build.py .`
- Pevački saveti: `sadrzaj/saveti.json` (srpski), `saveti.en.json`, `saveti.de.json`
- Izbor jezika (nota) i mobilni meni: `build.py` (header), `style.css`, `site.js`
- Klavir i vežbe: `site.js`
