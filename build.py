"""Generiše statične stranice sajta iz zajedničkih delova (meni, podnožje) na tri jezika.

Srpski je u korenu sajta, engleski u folderu en/, nemački u folderu de/.
Svaki tekst je napisan kao t("srpski", "English", "Deutsch"), pa se sva tri jezika menjaju na istom mestu.
Članci (Pevački saveti) su u sadrzaj/saveti.json, saveti.en.json i saveti.de.json.
"""
import os, html, sys, json, math
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else BASE
ARTIFACT = "--artifact" in sys.argv
E = html.escape

TEACHER = "MA Sanja Trifunović Gerginov"
VIDEO = "https://www.youtube.com/watch?v=kQUhk-6FKRM"

# ---------- jezici ----------
LANGS = ["sr", "en", "de"]
LANG_DIR = {"sr": "", "en": "en/", "de": "de/"}
LANG_HTML = {"sr": "sr-Latn", "en": "en", "de": "de"}
LANG_NAME = {"sr": "Srpski", "en": "English", "de": "Deutsch"}
L = "sr"   # jezik koji se trenutno generiše
R = ""     # putanja do korena sajta ("" za srpski, "../" za en/ i de/)

def t(sr, en, de):
    return {"sr": sr, "en": en, "de": de}[L]

# zastavice (unutar ovala se seku po sredini)
FLAG = {
    "sr": '<svg viewBox="0 0 3 2" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="3" height="2" fill="#fff"/><rect width="3" height="1.334" fill="#0C4076"/><rect width="3" height=".667" fill="#C6363C"/></svg>',
    "en": '<svg viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="60" height="30" fill="#012169"/><path d="M0 0L60 30M60 0L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0L60 30M60 0L0 30" stroke="#C8102E" stroke-width="2"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></svg>',
    "de": '<svg viewBox="0 0 5 3" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="5" height="3" fill="#FFCE00"/><rect width="5" height="2" fill="#DD0000"/><rect width="5" height="1" fill="#000"/></svg>',
}

# nota (osmina) za izbor jezika; u glavi note je globus
NOTE = ('<svg class="ln-svg" viewBox="0 0 44 60" aria-hidden="true">'
        '<path class="ln-stem" d="M29.2 4h3.1v41h-3.1z"/>'
        '<path class="ln-flag" d="M30.8 4c.6 6.4 4.6 9 7.6 12.6 3.6 4.3 4.4 9.6 1.4 15.6 1.1-5.2-.2-9.4-3.6-12.2-1.7-1.4-3.6-2.3-5.4-2.6z"/>'
        '<g class="ln-head"><ellipse cx="18" cy="46" rx="14.2" ry="10.4" transform="rotate(-22 18 46)"/>'
        '<g class="ln-globe" transform="rotate(-8 18 46)"><circle cx="18" cy="46" r="6.3"/><ellipse cx="18" cy="46" rx="2.7" ry="6.3"/>'
        '<path d="M11.7 46h12.6M12.6 42.9h10.8M12.6 49.1h10.8"/></g></g></svg>')

def lang_href(cur, target):
    return R + LANG_DIR[target] + cur

def oval(lang):
    return f'<span class="oval">{FLAG[lang]}</span>'

def lang_note(cur):
    opts = "".join(
        f'<a class="ln-opt" role="menuitem" style="--i:{i}" href="{lang_href(cur, x)}" hreflang="{LANG_HTML[x]}" lang="{LANG_HTML[x]}"'
        f'{" aria-current=" + chr(34) + "true" + chr(34) if x == L else ""}>{oval(x)}<span class="ln-name">{LANG_NAME[x]}</span></a>'
        for i, x in enumerate(LANGS))
    label = t("Jezik: srpski. Promeni jezik", "Language: English. Change language", "Sprache: Deutsch. Sprache wechseln")
    return f'''<div class="lang-note">
    <button class="ln-btn" type="button" aria-expanded="false" aria-controls="ln-pop" aria-label="{label}" title="{t("Jezik", "Language", "Sprache")}">{NOTE}</button>
    <div class="ln-pop" id="ln-pop" role="menu"><span class="ln-staff" aria-hidden="true"></span>{opts}</div>
  </div>'''

def m_langs(cur):
    items = "".join(
        f'<a class="ml-opt" href="{lang_href(cur, x)}" hreflang="{LANG_HTML[x]}" lang="{LANG_HTML[x]}"'
        f'{" aria-current=" + chr(34) + "true" + chr(34) if x == L else ""}>{oval(x)}<span>{LANG_NAME[x]}</span></a>'
        for x in LANGS)
    return f'<div class="m-langs" role="group" aria-label="{t("Jezik", "Language", "Sprache")}">{items}</div>'

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Figtree:wght@400;500;600&family=JetBrains+Mono:wght@400;600&family=Manrope:wght@500;600;700&display=swap">')

def SITE():
    return t("Časovi pevanja sa Sanjom", "Singing Lessons with Sanja", "Gesangsunterricht mit Sanja")

def LOGO():
    return (f'<span class="logo-keys" aria-hidden="true"><i></i><i></i><i></i></span>'
            f'<span>{t("Časovi pevanja", "Singing lessons", "Gesangsstunden")}<small>{t("sa Sanjom · online", "with Sanja · online", "mit Sanja · online")}</small></span>')

def head(title, desc, fname):
    t_ = SITE() if title is None else f"{title} · {SITE()}"
    alts = "".join(f'<link rel="alternate" hreflang="{LANG_HTML[x]}" href="{lang_href(fname, x)}">' for x in LANGS)
    return (f'<title>{E(t_)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{E(desc)}">\n{alts}\n{FONTS}\n<link rel="stylesheet" href="{R}style.css">\n')

CUR = ' aria-current="page"'
def NAV():
    return [("index.html", t("Početna", "Home", "Start")), ("o-sanji.html", t("O Sanji", "About Sanja", "Über Sanja")),
            ("kursevi.html", t("Kursevi i cene", "Courses & prices", "Kurse & Preise")),
            ("vezbaonica.html", t("Vežbaonica", "Practice room", "Übungsraum")),
            ("saveti.html", t("Pevački saveti", "Singing tips", "Gesangstipps")), ("utisci.html", t("Utisci", "Reviews", "Stimmen"))]

def header(cur):
    new = f'<span class="new">{t("novo", "new", "neu")}</span>'
    links = "".join(
        f'<a href="{h}" style="--i:{i}"{CUR if h == cur else ""}>{E(l)}{new if h == "vezbaonica.html" else ""}</a>'
        for i, (h, l) in enumerate(NAV()))
    return f'''<header class="nav"><div class="wrap">
  <a class="logo" href="index.html">{LOGO()}</a>
  <div class="nav-menu" id="nav-menu"><div class="nav-menu-in">
    <nav class="nav-links" aria-label="{t("Glavna navigacija", "Main navigation", "Hauptnavigation")}">{links}</nav>
    {m_langs(cur)}
  </div></div>
  <div class="nav-end">
  {lang_note(cur)}
  <a class="btn btn-rose cta-top" href="prijava.html">{t("Prijavi se", "Sign up", "Anmelden")}</a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-menu" aria-label="{t("Otvori meni", "Open menu", "Menü öffnen")}" data-open="{t("Otvori meni", "Open menu", "Menü öffnen")}" data-close="{t("Zatvori meni", "Close menu", "Menü schließen")}"><span class="burger" aria-hidden="true"><i></i><i></i><i></i></span></button>
  </div>
</div></header>'''

def FOOTER():
    return f'''<footer><div class="wrap">
  <div class="cols">
    <div style="display:grid;gap:14px;align-content:start">
      <span class="logo">{LOGO()}</span>
      <p style="opacity:.75;max-width:40ch;font-size:.94rem">{t("Online časovi pevanja za decu i odrasle, na srpskom, engleskom i nemačkom jeziku.", "Online singing lessons for children and adults, in Serbian, English and German.", "Online-Gesangsunterricht für Kinder und Erwachsene, auf Serbisch, Englisch und Deutsch.")}</p>
    </div>
    <div><h4>{t("Sajt", "Site", "Seiten")}</h4><ul>
      <li><a href="o-sanji.html">{t("O Sanji", "About Sanja", "Über Sanja")}</a></li><li><a href="kursevi.html">{t("Kursevi i cene", "Courses & prices", "Kurse & Preise")}</a></li>
      <li><a href="prijava.html">{t("Prijava", "Sign up", "Anmeldung")}</a></li><li><a href="vezbaonica.html">{t("Vežbaonica", "Practice room", "Übungsraum")}</a></li>
      <li><a href="saveti.html">{t("Pevački saveti", "Singing tips", "Gesangstipps")}</a></li><li><a href="utisci.html">{t("Utisci", "Reviews", "Stimmen")}</a></li></ul></div>
    <div><h4>{t("Kontakt i mreže", "Contact & social", "Kontakt & Social Media")}</h4><ul>
      <li>Email: <span class="ph-inline">[dodati]</span></li>
      <li>Instagram: <span class="ph-inline">[dodati]</span></li>
      <li>TikTok: <span class="ph-inline">[dodati]</span></li>
      <li><a href="{VIDEO}" target="_blank" rel="noopener">YouTube ↗</a></li></ul></div>
  </div>
  <div class="bottom">
    <div class="legal"><span>© <span data-year>2026</span> {SITE()}. {t("Sva prava zadržana.", "All rights reserved.", "Alle Rechte vorbehalten.")}</span>
      <span><a href="privatnost.html">{t("Politika privatnosti", "Privacy policy", "Datenschutz")}</a> · <a href="uslovi.html">{t("Uslovi korišćenja", "Terms of use", "Nutzungsbedingungen")}</a></span></div>
    <p class="credit"><span>{t("Dizajn i izrada sajta", "Website design &amp; development", "Webdesign &amp; Umsetzung")}</span><img src="{R}img/designare-dark.png" width="600" height="166" alt="deSignare" loading="lazy"></p>
  </div>
</div></footer>
<script src="{R}site.js"></script>'''


def page(fname, title, desc, body, root=False):
    h = head(title, desc, fname)
    doc_start = f'<!doctype html>\n<html lang="{LANG_HTML[L]}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    if root and ARTIFACT and L == "sr":  # početna u Artifact pregledu: Artifact sam dodaje doctype/head/body
        out = h + header(fname) + "\n<main>\n" + body + "\n</main>\n" + FOOTER()
    else:
        out = (doc_start + h + "</head>\n<body>\n" + header(fname) + "\n<main>\n" + body + "\n</main>\n" + FOOTER() + "\n</body>\n</html>\n")
    d = os.path.join(OUT, LANG_DIR[L])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, fname), "w", encoding="utf-8").write(out)

def page_hero(eyebrow, h1, lead):
    return f'''<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p></div></section>'''

def CTA():
    return f'''<section class="dark"><div class="wrap cta-band">
  <h2>{t("Svoju blistavu budućnost stvaraš ti.", "You create your own bright future.", "Deine glänzende Zukunft gestaltest du selbst.")}</h2>
  <div class="btn-row"><a class="btn btn-rose" href="prijava.html">{t("Prijavi se i zakaži čas", "Sign up and book a lesson", "Anmelden und Stunde buchen")}</a><a class="btn btn-ghost" href="kursevi.html">{t("Pogledaj kurseve", "See the courses", "Kurse ansehen")}</a></div>
</div></section>'''

# ---------- podaci sa postojećeg sajta ----------
def TESTIMONIALS():
    return [
        ("Miletić Vladan", t("Beograd, Srbija", "Belgrade, Serbia", "Belgrad, Serbien"),
         t("Ako misliš da za pevanje nisi Bogom dan, sa Sanjom ćeš od pevanja kupiti stan!",
           "Think you weren't born to sing? With Sanja, singing will buy you a flat – and everything!",
           "Glaubst du, dir fehlt fürs Singen das Talent? Mit Sanja kaufst du dir vom Singen ein Appartement!")),
        ("Ignjat Marković", t("Beč, Austrija", "Vienna, Austria", "Wien, Österreich"),
         t("Na Grandovoj audiciji su mi rekli da nisam za muziku, danas se samo time bavim i od toga živim.",
           "At the Grand Production audition they told me I wasn't cut out for music. Today it's all I do, and I make a living from it.",
           "Beim Casting von Grand Production hieß es, ich sei nicht für die Musik gemacht. Heute mache ich nichts anderes und lebe davon.")),
        ("Goran Stojković", t("Nürnberg, Nemačka", "Nuremberg, Germany", "Nürnberg, Deutschland"),
         t("Već na prvom probnom času znao sam da ću dalje raditi sa Sanjom, jer je pre svega izuzetno kompetentna…",
           "After the very first trial lesson I knew I'd keep working with Sanja, because above all she is exceptionally competent…",
           "Schon nach der ersten Probestunde wusste ich, dass ich mit Sanja weitermache, denn sie ist vor allem außergewöhnlich kompetent…")),
        ("Pavle Marković", t("Gradiška, BiH", "Gradiška, Bosnia and Herzegovina", "Gradiška, Bosnien und Herzegowina"),
         t("Sanja mi je mnogo pomogla sa visokim tonovima. Baš mi se svidelo što ima nekoliko glavnih pravila koje sam sledio…",
           "Sanja helped me a lot with high notes. I really liked that she has a few main rules that I followed…",
           "Sanja hat mir sehr bei den hohen Tönen geholfen. Mir hat gefallen, dass sie ein paar Hauptregeln hat, denen ich gefolgt bin…")),
        ("Marko Savković", t("Lucern, Švajcarska", "Lucerne, Switzerland", "Luzern, Schweiz"),
         t("Ja sam počeo od nule, prvo smo radili na mom sluhu godinu dana… Nakon otprilike godinu i po dana sam našao svoj prvi bend.",
           "I started from zero – first we worked on my ear for a year… After about a year and a half I found my first band.",
           "Ich habe bei null angefangen, zuerst haben wir ein Jahr lang an meinem Gehör gearbeitet… Nach etwa anderthalb Jahren habe ich meine erste Band gefunden.")),
        ("Milena Radovanović", t("Smederevo, Srbija", "Smederevo, Serbia", "Smederevo, Serbien"),
         t("Sanjini časovi su, pre svega, jedna motivacijska bomba. Ona vas ohrabruje da se držite sebe i svog puta…",
           "Sanja's lessons are, above all, a motivation bomb. She encourages you to stay true to yourself and your own path…",
           "Sanjas Stunden sind vor allem eine Motivationsbombe. Sie ermutigt dich, dir selbst und deinem Weg treu zu bleiben…")),
        ("Aleksandar Gajić", t("Cirih, Švajcarska", "Zurich, Switzerland", "Zürich, Schweiz"),
         t("Nažalost, nisam uspeo da se upišem na intenzivni kurs jer je brzinom svetlosti popunjen…",
           "Unfortunately I didn't manage to sign up for the intensive course, because it filled up at the speed of light…",
           "Leider habe ich keinen Platz im Intensivkurs bekommen, weil er in Lichtgeschwindigkeit ausgebucht war…")),
        ("Mario", t("Grac, Austrija", "Graz, Austria", "Graz, Österreich"),
         t("Sanja je pevački guru! Jedna od retkih profesora za koju ne postoje prepreke da nekog nauči.",
           "Sanja is a singing guru! One of the rare teachers for whom there's no obstacle to teaching someone.",
           "Sanja ist ein Gesangs-Guru! Eine der wenigen Lehrerinnen, für die es kein Hindernis gibt, jemandem etwas beizubringen.")),
        ("Marina Maksimović", t("Aleksinac, Srbija", "Aleksinac, Serbia", "Aleksinac, Serbien"),
         t("Pevanje je moj posao. Sada pevam zahtevne pesme, ne postoji više pesma koja mi predstavlja problem!",
           "Singing is my job. Now I sing demanding songs – there's no song that's a problem for me anymore!",
           "Singen ist mein Beruf. Jetzt singe ich anspruchsvolle Lieder – es gibt kein Lied mehr, das mir Probleme macht!")),
        ("Helena Simić", t("Beč, Austrija", "Vienna, Austria", "Wien, Österreich"),
         t("Puno stvari sam naučila o pravilima pevanja. Zadovoljstvo je raditi sa Sanjom, jer radi nesebično, punim srcem.",
           "I've learned a lot about the rules of singing. It's a pleasure to work with Sanja, because she gives selflessly, with all her heart.",
           "Ich habe viel über die Regeln des Singens gelernt. Es ist eine Freude, mit Sanja zu arbeiten, denn sie gibt selbstlos und mit ganzem Herzen.")),
        ("Nenad Milivojević", t("Lucern, Švajcarska", "Lucerne, Switzerland", "Luzern, Schweiz"),
         t("Ubedljivo najbolji časovi pevanja! Sanja veoma dobro objašnjava, ima pravi odgovor na svako pitanje.",
           "By far the best singing lessons! Sanja explains things really well and has the right answer to every question.",
           "Mit Abstand der beste Gesangsunterricht! Sanja erklärt sehr gut und hat auf jede Frage die richtige Antwort.")),
    ]

def tq(x):
    n, c, q = x
    o, cl = t("„", "“", "„"), t("“", "”", "“")
    return f'<figure class="q" style="margin:0"><p>{o}{E(q)}{cl}</p><figcaption class="who"><b>{E(n)}</b>{E(c)}</figcaption></figure>'

# kratki opisi saveta za kartice (redosled kao na listi)
def POSTS():
    return [
        ("koliko-casova", t("Koliko brzo će učenik napredovati na časovima pevanja zavisi, zapravo, od nekoliko faktora.",
                            "How quickly a student progresses in singing lessons actually depends on several factors.",
                            "Wie schnell man im Gesangsunterricht vorankommt, hängt eigentlich von mehreren Faktoren ab.")),
        ("svakodnevno-disanje", t("Sigurno ste čuli za izraz „disati punim plućima“. To znači živeti ispunjen život, punim kapacitetom.",
                                  "You've surely heard the expression “to breathe with full lungs”. It means living a fulfilled life, at full capacity.",
                                  "Sicher kennen Sie den Ausdruck „aus voller Lunge atmen“. Er bedeutet, ein erfülltes Leben mit voller Kraft zu leben.")),
        ("drzanje-tela", t("Držanje tela svakog pevača treba da bude prirodno da bi svi mišići u telu bili opušteni.",
                           "Every singer's posture should be natural so that all the muscles in the body are relaxed.",
                           "Die Körperhaltung jedes Sängers sollte natürlich sein, damit alle Muskeln entspannt sind.")),
        ("online-nastava", t("Online nastava je postala deo naše svakodnevnice i povezuje vas sa najkvalitetnijim profesorima širom sveta.",
                             "Online lessons have become part of everyday life and connect you with the best teachers around the world.",
                             "Online-Unterricht ist Teil unseres Alltags und verbindet Sie mit den besten Lehrkräften weltweit.")),
        ("jasan-govor", t("Ukoliko jasno i razgovetno govorite, ostavljate veoma lep utisak na sagovornika.",
                          "If you speak clearly and distinctly, you leave a very good impression on the person you're talking to.",
                          "Wer klar und deutlich spricht, hinterlässt beim Gegenüber einen sehr guten Eindruck.")),
        ("pevanje-je-zdravo", t("Pevanje podiže samopouzdanje, kada otkrijemo svoju strast i počnemo njome da se bavimo.",
                                "Singing boosts self-confidence when we discover our passion and start pursuing it.",
                                "Singen stärkt das Selbstvertrauen, wenn wir unsere Leidenschaft entdecken und ihr nachgehen.")),
        ("boja-glasa", t("Svima se nama desilo da svoj glas prilikom govora doživljavamo na jedan način…",
                         "It has happened to all of us: we perceive our own speaking voice one way…",
                         "Das kennen wir alle: Wir nehmen unsere eigene Sprechstimme auf eine bestimmte Weise wahr…")),
        ("pevacko-disanje", t("Nama je vazduh gorivo. Vazduh je sve. Vazduh je pevačka moć. Bez vazduha nema pevanja.",
                              "Air is our fuel. Air is everything. Air is a singer's power. Without air there is no singing.",
                              "Luft ist unser Treibstoff. Luft ist alles. Luft ist die Kraft des Sängers. Ohne Luft kein Gesang.")),
        ("trema", t("Javni nastup može biti jedno stresno iskustvo ukoliko u glavi imamo negativna očekivanja.",
                    "Performing in public can be stressful if we have negative expectations in our head.",
                    "Ein öffentlicher Auftritt kann stressig sein, wenn wir negative Erwartungen im Kopf haben.")),
    ]

def load_articles():
    name = "saveti.json" if L == "sr" else f"saveti.{L}.json"
    arts = json.load(open(os.path.join(BASE, "sadrzaj", name), encoding="utf-8"))
    for a in arts:
        if "words" not in a:
            a["words"] = sum(len(" ".join(x for x in b[1:] if isinstance(x, str)).split()) for b in a["blocks"])
    return arts

def href(slug): return f"savet-{slug}.html"

def render_blocks(blocks):
    out, k = [], 0
    while k < len(blocks):
        typ = blocks[k][0]
        if typ == "li":
            items = []
            while k < len(blocks) and blocks[k][0] == "li": items.append(f"<li>{E(blocks[k][1])}</li>"); k += 1
            out.append('<ul class="art-list">' + "".join(items) + "</ul>"); continue
        if typ == "step":
            items = []
            while k < len(blocks) and blocks[k][0] in ("step", "li"):
                if blocks[k][0] == "step":
                    items.append([E(blocks[k][1]), []])
                else:
                    items[-1][1].append(f"<li>{E(blocks[k][1])}</li>")
                k += 1
            out.append('<ol class="art-steps">' + "".join(f"<li><span>{s}</span>" + (f'<ul>{"".join(sub)}</ul>' if sub else "") + "</li>" for s, sub in items) + "</ol>"); continue
        bl = blocks[k]
        if typ == "lead": out.append(f'<p class="art-lead">{E(bl[1])}</p>')
        elif typ == "p" and len(bl[1]) < 30 and bl[1].endswith(":"): out.append(f"<h3>{E(bl[1][:-1])}</h3>")
        elif typ == "p": out.append(f"<p>{E(bl[1])}</p>")
        elif typ == "pb": out.append(f"<p><strong>{E(bl[1])}</strong> {E(bl[2])}</p>")
        elif typ == "h2": out.append(f"<h2>{E(bl[1])}</h2>")
        elif typ == "h3": out.append(f"<h3>{E(bl[1])}</h3>")
        elif typ == "formula": out.append(f'<p class="formula">{" <span>→</span> ".join(E(x) for x in bl[1].split(" - "))}</p>')
        elif typ == "quote": out.append(f"<blockquote>{E(bl[1])}</blockquote>")
        k += 1
    return "\n  ".join(out)

# ===================== STRANICE =====================
def build():
    ARTS = load_articles()
    ART = {a["slug"]: a for a in ARTS}
    TS = TESTIMONIALS()
    PS = POSTS()
    read = t("Pročitaj →", "Read →", "Lesen →")
    def pc(p):
        slug, excerpt = p
        a = ART[slug]
        return f'<a class="post-card" href="{href(slug)}" data-cat="{E(a["cat"])}"><span class="cat">{E(a["cat"])}</span><h3>{E(a["title"])}</h3><p>{E(excerpt)}</p><span class="more">{read}</span></a>'

    # ---------- POČETNA ----------
    h1a, h1b, h1c = t(("Otkrij svoj glas. ", "Peva se", " odavde."),
                      ("Discover your voice. ", "Sing", " from right here."),
                      ("Entdecke deine Stimme. ", "Gesungen", " wird genau hier."))
    home = f'''<section class="hero"><div class="wrap hero-grid">
  <div class="hero-copy">
    <span class="eyebrow">{t("Online časovi pevanja · deca i odrasli", "Online singing lessons · children and adults", "Online-Gesangsunterricht · Kinder und Erwachsene")}</span>
    <h1>{h1a}<span class="accent">{h1b}</span>{h1c}</h1>
    <p class="lead">{t("Individualni časovi pevanja preko video poziva, za početnike, napredne i pripremu za takmičenja. Zajedno otkrivamo i razvijamo originalni i jedinstveni stil tvog pevanja.",
                      "One-to-one singing lessons over video call, for beginners, advanced singers and competition prep. Together we discover and develop your own original, unique singing style.",
                      "Einzelunterricht im Gesang per Videoanruf – für Anfänger, Fortgeschrittene und zur Vorbereitung auf Wettbewerbe. Gemeinsam entdecken und entwickeln wir deinen eigenen, unverwechselbaren Gesangsstil.")}</p>
    <div class="btn-row"><a class="btn btn-rose" href="prijava.html">{t("Prijavi se", "Sign up", "Anmelden")}</a><a class="btn btn-ghost" href="vezbaonica.html">{t("Isprobaj Vežbaonicu →", "Try the Practice room →", "Übungsraum ausprobieren →")}</a></div>
    <div class="chips"><span class="chip">{t("narodna", "folk", "Volksmusik")}</span><span class="chip">pop</span><span class="chip">rock</span><span class="chip">{t("etno", "ethno", "Ethno")}</span><span class="chip">SR · EN · DE</span></div>
  </div>
  <div class="hero-photo"><img src="{R}img/klavir.jpg" alt="{t("Otvorene note na klaviru, iza njih mehanika klavira i osušeni božur", "Open sheet music on a piano, with the piano action and a dried peony behind it", "Aufgeschlagene Noten auf einem Klavier, dahinter die Klaviermechanik und eine getrocknete Pfingstrose")}">
    <div class="hero-badge"><span class="live-dot" aria-hidden="true"></span><span><strong>{TEACHER}</strong><br>{t("vokalni pedagog, Beč", "vocal coach, Vienna", "Gesangspädagogin, Wien")}</span></div></div>
</div></section>
<div class="facts"><div class="wrap">
  <div class="fact"><b>{t("15 godina", "15 years", "15 Jahre")}</b><span>{t("podučavanja vokalne tehnike", "teaching vocal technique", "Unterricht in Gesangstechnik")}</span></div>
  <div class="fact"><b>{t("od 2004.", "since 2004", "seit 2004")}</b><span>{t("profesionalno peva", "singing professionally", "professionelle Sängerin")}</span></div>
  <div class="fact"><b>{t("3 jezika", "3 languages", "3 Sprachen")}</b><span>{t("srpski, engleski, nemački", "Serbian, English, German", "Serbisch, Englisch, Deutsch")}</span></div>
  <div class="fact"><b>{t("svi kontinenti", "every continent", "alle Kontinente")}</b><span>{t("učenici širom sveta", "students worldwide", "Schüler weltweit")}</span></div>
</div></div>

<section><div class="wrap split">
  <div style="display:grid;gap:22px"><span class="eyebrow">{t("Upoznaj Sanju", "Meet Sanja", "Lerne Sanja kennen")}</span>
    <p class="big-quote">{t("Za učenje pevanja preduslov je da učenik ima želju za učenjem i napretkom.", "The one requirement for learning to sing is that the student wants to learn and grow.", "Die Voraussetzung fürs Singenlernen ist, dass man lernen und vorankommen will.")}</p></div>
  <div class="prose">
    <p><strong>{TEACHER}</strong> {t("je vrhunski muzički pedagog sa 15 godina iskustva u podučavanju vokalne tehnike. Završila je master studije na Fakultetu muzičke umetnosti u Beogradu i stručno usavršavanje u Austriji.",
                                    "is a first-class music educator with 15 years of experience teaching vocal technique. She holds a master's degree from the Faculty of Music in Belgrade and completed further professional training in Austria.",
                                    "ist eine herausragende Musikpädagogin mit 15 Jahren Erfahrung im Unterrichten von Gesangstechnik. Sie hat ihr Masterstudium an der Fakultät für Musik in Belgrad abgeschlossen und sich in Österreich fachlich weitergebildet.")}</p>
    <p>{t("Autor je nekoliko stručnih publikacija o vokalnoj tehnici, a njena najnovija publikacija o osnovama vokalne tehnike je u pripremi.",
          "She is the author of several professional publications on vocal technique, and her latest publication, on the fundamentals of vocal technique, is in preparation.",
          "Sie ist Autorin mehrerer Fachpublikationen zur Gesangstechnik; ihre neueste Publikation über die Grundlagen der Gesangstechnik ist in Vorbereitung.")}</p>
    <p><a class="textlink" href="o-sanji.html">{t("Pročitaj više o Sanji", "Read more about Sanja", "Mehr über Sanja")}</a></p>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{t("Želiš li da ti pevanje postane posao, zanimanje, životni poziv?", "Do you want singing to become your job, your profession, your calling?", "Soll Singen dein Beruf, dein Job, deine Berufung werden?")}</span><h2>{t("Tri kursa, jedan cilj: tvoj glas.", "Three courses, one goal: your voice.", "Drei Kurse, ein Ziel: deine Stimme.")}</h2></div>
  <div class="grid-3">
    <a class="card level" href="kursevi.html" style="text-decoration:none"><div class="lvl"><i class="on"></i><i></i><i></i></div><span class="tagline">{t("početni", "beginner", "Einstieg")}</span><h3>{t("Buđenje muzičkog sluha", "Awakening your musical ear", "Das musikalische Gehör wecken")}</h3><p>{t("Za one koji tek počinju. Fokus na tačnoj intonaciji.", "For those just starting out. The focus is on accurate pitch.", "Für alle, die gerade anfangen. Im Fokus steht die saubere Intonation.")}</p></a>
    <a class="card level" href="kursevi.html" style="text-decoration:none"><div class="lvl"><i class="on"></i><i class="on"></i><i></i></div><span class="tagline">{t("napredni", "advanced", "Fortgeschritten")}</span><h3>{t("Pravilna tehnika pevanja", "Correct singing technique", "Die richtige Gesangstechnik")}</h3><p>{t("Disanje, držanje, opseg i elementi tvog omiljenog žanra.", "Breathing, posture, range and the elements of your favourite genre.", "Atmung, Haltung, Stimmumfang und die Elemente deines Lieblingsgenres.")}</p></a>
    <a class="card level" href="kursevi.html" style="text-decoration:none"><div class="lvl"><i class="on"></i><i class="on"></i><i class="on"></i></div><span class="tagline">{t("profesionalni", "professional", "Profi")}</span><h3>{t("Pevačke tajne profesionalaca", "Secrets of professional singers", "Gesangsgeheimnisse der Profis")}</h3><p>{t("Za scenu, takmičenja i pevanje kao zanimanje.", "For the stage, competitions and singing as a career.", "Für die Bühne, Wettbewerbe und Singen als Beruf.")}</p></a>
  </div>
  <div class="sec-foot"><a class="textlink" href="kursevi.html">{t("Cene i zakazivanje", "Prices and booking", "Preise und Buchung")}</a></div>
</div></section>

<section class="dark"><div class="wrap" style="display:grid;gap:40px">
  <a class="video-card" href="{VIDEO}" target="_blank" rel="noopener">
    <div class="video-thumb"><span class="play" aria-hidden="true"></span></div>
    <div class="video-text"><span class="eyebrow">{t("Video uputstvo", "Video guide", "Video-Anleitung")}</span><h2 style="font-size:clamp(1.7rem,3vw,2.4rem)">{t("Otkrijte sa mnom sve pevačke tajne!", "Discover all the secrets of singing with me!", "Entdecken Sie mit mir alle Geheimnisse des Singens!")}</h2><p class="muted">{t("Pogledaj na YouTube-u ↗", "Watch on YouTube ↗", "Auf YouTube ansehen ↗")}</p></div>
  </a>
  <div class="split" style="align-items:center">
    <div style="display:grid;gap:14px"><span class="eyebrow">{t("Novo · Vežbaonica", "New · Practice room", "Neu · Übungsraum")}</span><h2>{t("Zagrej glas uz klavir, bilo kad.", "Warm up your voice with the piano, any time.", "Wärm deine Stimme am Klavier auf, wann immer du willst.")}</h2></div>
    <div style="display:grid;gap:18px"><p class="lead">{t("Interaktivna klavijatura sa vežbama za zagrevanje. Izabereš vežbu i početni ton, klavir svira, a ti pevaš. Svaki krug se podiže za pola stepena.",
                                                       "An interactive keyboard with warm-up exercises. Pick an exercise and a starting note – the piano plays and you sing. Each round goes up a semitone.",
                                                       "Eine interaktive Klaviatur mit Übungen zum Einsingen. Du wählst eine Übung und einen Anfangston, das Klavier spielt und du singst. Jede Runde geht einen Halbton höher.")}</p>
      <div class="btn-row"><a class="btn btn-rose" href="vezbaonica.html">{t("Otvori Vežbaonicu", "Open the Practice room", "Übungsraum öffnen")}</a></div></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{t("Utisci učenika", "What students say", "Stimmen der Schüler")}</span><h2>{t("Od Beograda do Lucerna.", "From Belgrade to Lucerne.", "Von Belgrad bis Luzern.")}</h2></div>
  <div class="quotes">{tq(TS[1])}{tq(TS[4])}{tq(TS[10])}</div>
  <div class="sec-foot"><a class="textlink" href="utisci.html">{t("Svi utisci (11)", "All reviews (11)", "Alle Stimmen (11)")}</a></div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{t("Pevački saveti", "Singing tips", "Gesangstipps")}</span><h2>{t("Čitaj između časova.", "Read between lessons.", "Lies zwischen den Stunden.")}</h2></div>
  <div class="posts">{pc(PS[0])}{pc(PS[1])}{pc(PS[2])}</div>
  <div class="sec-foot"><a class="textlink" href="saveti.html">{t("Svi saveti", "All tips", "Alle Tipps")}</a></div>
</div></section>
{CTA()}'''
    page("index.html", None, t("Online časovi pevanja za decu i odrasle sa MA Sanjom Trifunović Gerginov: početnici, napredni i priprema za takmičenja.",
                               "Online singing lessons for children and adults with MA Sanja Trifunović Gerginov: beginners, advanced singers and competition prep.",
                               "Online-Gesangsunterricht für Kinder und Erwachsene mit MA Sanja Trifunović Gerginov: Anfänger, Fortgeschrittene und Wettbewerbsvorbereitung."), home, root=True)

    # ---------- O SANJI ----------
    about = page_hero(t("O Sanji", "About Sanja", "Über Sanja"),
                      t("Glas, scena i 15 godina u učionici.", "Voice, stage and 15 years in the classroom.", "Stimme, Bühne und 15 Jahre im Unterricht."),
                      t("Vokalni pedagog, online profesorka pevanja i predavač vokalne tehnike. Živi i radi u Beču, a predaje učenicima na svim kontinentima.",
                        "Vocal coach, online singing teacher and lecturer in vocal technique. She lives and works in Vienna and teaches students on every continent.",
                        "Gesangspädagogin, Online-Gesangslehrerin und Dozentin für Gesangstechnik. Sie lebt und arbeitet in Wien und unterrichtet Schüler auf allen Kontinenten.")) + f'''
<section><div class="wrap split">
  <div style="display:grid;gap:14px">
    <figure class="about-photo"><img src="{R}img/sanja.jpg" alt="{t("Sanja Trifunović Gerginov pored klavijature, sa peharom", "Sanja Trifunović Gerginov next to a keyboard, holding a trophy", "Sanja Trifunović Gerginov neben einem Keyboard, mit einem Pokal")}" loading="lazy"></figure>
    <button class="gal-banner" type="button" data-gallery-open aria-haspopup="dialog">
      <span class="gb-text"><span class="gb-kicker">{t("Galerija", "Gallery", "Galerie")}</span><span class="gb-title">{t("Sanja iza klavijature", "Sanja at the keys", "Sanja an den Tasten")}</span><span class="gb-cta">{t("3 fotografije · pogledaj →", "3 photos · take a look →", "3 Fotos · ansehen →")}</span></span>
      <span class="gb-stack" aria-hidden="true">
        <img src="{R}img/galerija/3.jpg" alt="" style="object-position:50% 40%">
        <img src="{R}img/galerija/2.jpg" alt="" style="object-position:50% 30%">
        <img src="{R}img/galerija/1.jpg" alt="" style="object-position:72% 40%">
      </span>
      <span class="gb-shine" aria-hidden="true"></span>
    </button>
  </div>
  <div class="prose">
    <p><strong>{TEACHER}</strong> {t("profesionalno se bavi pevanjem od 2004. godine. Priznati je vokalni izvođač, sa nagradama u zemlji i inostranstvu.",
                                    "has been singing professionally since 2004. She is an acclaimed vocal performer with awards at home and abroad.",
                                    "singt seit 2004 professionell. Sie ist eine anerkannte Sängerin mit Auszeichnungen im In- und Ausland.")}</p>
    <p>{t("Završila je master akademske studije na Fakultetu muzičke umetnosti u Beogradu. Radila je kao profesor muzičke kulture u školama u Beogradu i Jagodini i bila dugogodišnji saradnik u nastavi na Fakultetu pedagoških nauka u Jagodini.",
          "She completed her master's degree at the Faculty of Music in Belgrade. She taught music at schools in Belgrade and Jagodina and was a long-standing teaching associate at the Faculty of Education in Jagodina.",
          "Sie hat ihr Masterstudium an der Fakultät für Musik in Belgrad abgeschlossen. Sie unterrichtete Musik an Schulen in Belgrad und Jagodina und war viele Jahre Lehrbeauftragte an der Pädagogischen Fakultät in Jagodina.")}</p>
    <p>{t("Danas živi i radi u Beču, gde predaje i drži predavanja iz vokalne tehnike i nastavlja stručno usavršavanje. Vodi međunarodnu online školu pevanja na srpskom, engleskom i nemačkom jeziku, a govori i italijanski.",
          "Today she lives and works in Vienna, where she teaches, lectures on vocal technique and continues her professional development. She runs an international online singing school in Serbian, English and German, and also speaks Italian.",
          "Heute lebt und arbeitet sie in Wien, wo sie unterrichtet, Vorträge über Gesangstechnik hält und sich fachlich weiterbildet. Sie leitet eine internationale Online-Gesangsschule auf Serbisch, Englisch und Deutsch und spricht außerdem Italienisch.")}</p>
    <ul class="creds">
      <li><span class="yr">{t("od 2004.", "since 2004", "seit 2004")}</span><span>{t("Profesionalni vokalni izvođač, nagrade u zemlji i inostranstvu", "Professional vocal performer, awards at home and abroad", "Professionelle Sängerin, Auszeichnungen im In- und Ausland")}</span></li>
      <li><span class="yr">{t("FMU Beograd", "FMU Belgrade", "FMU Belgrad")}</span><span>{t("Master akademske studije", "Master's degree", "Masterstudium")}</span></li>
      <li><span class="yr">{t("Beograd · Jagodina", "Belgrade · Jagodina", "Belgrad · Jagodina")}</span><span>{t("Profesor muzičke kulture; saradnik u nastavi na Fakultetu pedagoških nauka", "Music teacher; teaching associate at the Faculty of Education", "Musiklehrerin; Lehrbeauftragte an der Pädagogischen Fakultät")}</span></li>
      <li><span class="yr">{t("od 2014.", "since 2014", "seit 2014")}</span><span>{t("Suosnivač KUD-a „Jovanča Micić“, predavač vokalne tehnike", "Co-founder of the cultural society “Jovanča Micić”, vocal technique teacher", "Mitbegründerin des Kulturvereins „Jovanča Micić“, Dozentin für Gesangstechnik")}</span></li>
      <li><span class="yr">{t("Austrija", "Austria", "Österreich")}</span><span>{t("Stručno usavršavanje; predavanja iz vokalne tehnike u Beču", "Further professional training; lectures on vocal technique in Vienna", "Fachliche Weiterbildung; Vorträge über Gesangstechnik in Wien")}</span></li>
      <li><span class="yr">{t("u pripremi", "in preparation", "in Vorbereitung")}</span><span>{t("Nova publikacija o osnovama vokalne tehnike", "New publication on the fundamentals of vocal technique", "Neue Publikation über die Grundlagen der Gesangstechnik")}</span></li>
    </ul>
  </div>
</div></section>


<dialog class="lightbox" id="lightbox" aria-label="{t("Galerija fotografija", "Photo gallery", "Fotogalerie")}">
  <div class="lb-inner">
    <button class="lb-close" type="button" aria-label="{t("Zatvori galeriju", "Close gallery", "Galerie schließen")}">×</button>
    <figure class="lb-main"><img id="lb-img" src="{R}img/galerija/1.jpg" alt=""><figcaption id="lb-cap"></figcaption></figure>
    <button class="lb-arrow lb-prev" type="button" aria-label="{t("Prethodna fotografija", "Previous photo", "Vorheriges Foto")}">‹</button>
    <button class="lb-arrow lb-next" type="button" aria-label="{t("Sledeća fotografija", "Next photo", "Nächstes Foto")}">›</button>
    <div class="lb-thumbs">
      <button type="button" data-src="{R}img/galerija/1.jpg"><img src="{R}img/galerija/1.jpg" alt="{t("Sanja za klavijaturom sa čarobnim štapićem", "Sanja at the keyboard with a magic wand", "Sanja am Keyboard mit einem Zauberstab")}"></button>
      <button type="button" data-src="{R}img/galerija/2.jpg"><img src="{R}img/galerija/2.jpg" alt="{t("Sanja u belom sakou, nasmejana", "Sanja in a white blazer, smiling", "Sanja im weißen Blazer, lächelnd")}"></button>
      <button type="button" data-src="{R}img/galerija/3.jpg"><img src="{R}img/galerija/3.jpg" alt="{t("Sanja pored klavijature, sa peharom", "Sanja next to the keyboard, holding a trophy", "Sanja neben dem Keyboard, mit einem Pokal")}"></button>
    </div>
  </div>
</dialog>
<section class="dark"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{t("Metoda", "Method", "Methode")}</span><h2>24/7 Online Singing Support</h2>
    <p class="lead">{t("Napredak se ne dešava samo na času. Zato Sanja prati tvoje vežbanje i između časova.", "Progress doesn't only happen during the lesson. That's why Sanja follows your practice between lessons too.", "Fortschritt passiert nicht nur in der Stunde. Deshalb begleitet Sanja dein Üben auch zwischen den Stunden.")}</p></div>
  <div class="steps" style="--cols:4">
    <div class="step"><span class="n">01 · {t("posle časa", "after the lesson", "nach der Stunde")}</span><h3>{t("Pisane smernice", "Written guidance", "Schriftliche Anleitung")}</h3><p>{t("Dobijaš uputstva i vežbaš kod kuće.", "You get instructions and practise at home.", "Du bekommst Anweisungen und übst zu Hause.")}</p></div>
    <div class="step"><span class="n">02 · {t("vežbanje", "practice", "Üben")}</span><h3>{t("Tvoj snimak", "Your recording", "Deine Aufnahme")}</h3><p>{t("Snimiš najbolji audio sa vežbanja i pošalješ ga Sanji.", "You record your best take from practice and send it to Sanja.", "Du nimmst deine beste Übungsaufnahme auf und schickst sie Sanja.")}</p></div>
    <div class="step"><span class="n">03 · {t("isti dan", "same day", "am selben Tag")}</span><h3>{t("Nove smernice", "New guidance", "Neue Anleitung")}</h3><p>{t("Sanja pregleda snimke na kraju radnog dana i brzo šalje nove smernice.", "Sanja reviews recordings at the end of the working day and quickly sends new guidance.", "Sanja hört die Aufnahmen am Ende des Arbeitstages an und schickt schnell neue Anweisungen.")}</p></div>
    <div class="step"><span class="n">04 · {t("uvek", "always", "immer")}</span><h3>{t("Snimljeni časovi", "Recorded lessons", "Aufgezeichnete Stunden")}</h3><p>{t("Svi časovi se snimaju, pa možeš da ih pogledaš ponovo.", "All lessons are recorded, so you can watch them again.", "Alle Stunden werden aufgezeichnet, sodass du sie dir erneut ansehen kannst.")}</p></div>
  </div>
</div></section>

<section><div class="wrap split">
  <div style="display:grid;gap:22px"><span class="eyebrow">{t("Zašto online", "Why online", "Warum online")}</span>
    <p class="big-quote">{t("Časove održavam online jer imam učenike na svim kontinentima.", "I teach online because I have students on every continent.", "Ich unterrichte online, weil ich Schüler auf allen Kontinenten habe.")}</p></div>
  <div class="prose">
    <p>{t("Biraš žanr koji voliš: narodna muzika, pop, rock ili etno. Na časovima radimo na svim karakterističnim elementima tvog omiljenog žanra.",
          "You choose the genre you love: folk, pop, rock or ethno. In the lessons we work on all the characteristic elements of your favourite genre.",
          "Du wählst das Genre, das du liebst: Volksmusik, Pop, Rock oder Ethno. Im Unterricht arbeiten wir an allen typischen Elementen deines Lieblingsgenres.")}</p>
    <p>{t("Za napredak su potrebni motivacija i spremnost da vežbaš svakog dana. Mnogi bivši učenici danas pevaju samostalno, a Sanja ostaje u kontaktu sa njima i posle završenih časova.",
          "Progress takes motivation and a willingness to practise every day. Many former students now sing independently, and Sanja stays in touch with them after their lessons end.",
          "Für Fortschritt braucht es Motivation und die Bereitschaft, jeden Tag zu üben. Viele ehemalige Schüler singen heute selbstständig, und Sanja bleibt auch nach dem Unterricht mit ihnen in Kontakt.")}</p>
  </div>
</div></section>
{CTA()}'''
    page("o-sanji.html", t("O Sanji", "About Sanja", "Über Sanja"),
         t("Biografija MA Sanje Trifunović Gerginov, vokalnog pedagoga i online profesorke pevanja iz Beča.",
           "Biography of MA Sanja Trifunović Gerginov, vocal coach and online singing teacher based in Vienna.",
           "Biografie von MA Sanja Trifunović Gerginov, Gesangspädagogin und Online-Gesangslehrerin aus Wien."), about)

    # ---------- KURSEVI I CENE ----------
    FAQ = [
        (t("Koliko časova mi treba da naučim da pevam?", "How many lessons do I need to learn to sing?", "Wie viele Stunden brauche ich, um singen zu lernen?"),
         t("Zavisi od sluha i osećaja za ritam, od toga koliko vežbaš i koliko često imaš časove. Uz redovno vežbanje, posle dva i po do tri meseca obično si zadovoljan onim što čuješ.",
           "It depends on your ear and sense of rhythm, how much you practise and how often you have lessons. With regular practice, after two and a half to three months you're usually happy with what you hear.",
           "Das hängt von deinem Gehör und Rhythmusgefühl ab, davon, wie viel du übst und wie oft du Unterricht hast. Mit regelmäßigem Üben bist du nach zweieinhalb bis drei Monaten meist zufrieden mit dem, was du hörst.")),
        (t("Na kom jeziku se drže časovi?", "What language are the lessons in?", "In welcher Sprache findet der Unterricht statt?"),
         t("Na srpskom, engleskom ili nemačkom.", "Serbian, English or German.", "Auf Serbisch, Englisch oder Deutsch.")),
        (t("Da li su časovi i za decu?", "Are the lessons for children too?", "Ist der Unterricht auch für Kinder?"),
         t("Da, časovi su za decu i odrasle.", "Yes, lessons are for children and adults.", "Ja, der Unterricht ist für Kinder und Erwachsene.")),
        (t("Šta je 24/7 Online Singing Support?", "What is 24/7 Online Singing Support?", "Was ist 24/7 Online Singing Support?"),
         t("Između časova šalješ snimke vežbanja, a Sanja ti vraća nove smernice. Opciju biraš u prijavi.",
           "Between lessons you send recordings of your practice, and Sanja sends you new guidance. You choose this option when you sign up.",
           "Zwischen den Stunden schickst du Aufnahmen vom Üben und Sanja gibt dir neue Anweisungen. Die Option wählst du bei der Anmeldung.")),
        (t("Da li se časovi snimaju?", "Are the lessons recorded?", "Werden die Stunden aufgezeichnet?"),
         t("Da, svi časovi se snimaju, pa možeš da ih pogledaš ponovo.", "Yes, all lessons are recorded, so you can watch them again.", "Ja, alle Stunden werden aufgezeichnet, sodass du sie dir erneut ansehen kannst.")),
        (t("Kako otkazujem čas?", "How do I cancel a lesson?", "Wie sage ich eine Stunde ab?"),
         t("Čas se otkazuje najkasnije dan ranije.", "Lessons must be cancelled at least one day in advance.", "Eine Stunde muss spätestens einen Tag vorher abgesagt werden.")),
    ]
    signup_btn = t("Prijavi se", "Sign up", "Anmelden")
    courses = page_hero(t("Kursevi i cene", "Courses & prices", "Kurse & Preise"),
                        t("Individualni časovi, po tvojoj meri.", "One-to-one lessons, tailored to you.", "Einzelunterricht, auf dich zugeschnitten."),
                        t("Svi časovi su individualni, a termini se prilagođavaju tebi. U prijavi navedi naziv kursa koji te zanima.",
                          "All lessons are one-to-one, and times are arranged around you. In your sign-up, mention the course you're interested in.",
                          "Alle Stunden sind Einzelunterricht, und die Termine richten sich nach dir. Gib bei der Anmeldung den Kurs an, der dich interessiert.")) + f'''
<section><div class="wrap">
  <div class="grid-3">
    <div class="card level"><div class="lvl"><i class="on"></i><i></i><i></i></div><span class="tagline">{t("početni nivo", "beginner level", "Einstiegsniveau")}</span><h3>{t("Buđenje muzičkog sluha", "Awakening your musical ear", "Das musikalische Gehör wecken")}</h3><p>{t("Prvi koraci u pevanju. Radimo na sluhu i tačnoj intonaciji, da čuješ i ponoviš ton koji sviram.", "Your first steps in singing. We work on your ear and accurate pitch, so you can hear and repeat the note I play.", "Deine ersten Schritte im Gesang. Wir arbeiten an Gehör und sauberer Intonation, damit du den Ton, den ich spiele, hörst und nachsingst.")}</p></div>
    <div class="card level"><div class="lvl"><i class="on"></i><i class="on"></i><i></i></div><span class="tagline">{t("napredni nivo", "advanced level", "Fortgeschrittenes Niveau")}</span><h3>{t("Pravilna tehnika pevanja", "Correct singing technique", "Die richtige Gesangstechnik")}</h3><p>{t("Disanje, držanje tela, opseg i karakteristični elementi tvog omiljenog žanra.", "Breathing, posture, range and the characteristic elements of your favourite genre.", "Atmung, Körperhaltung, Stimmumfang und die typischen Elemente deines Lieblingsgenres.")}</p></div>
    <div class="card level"><div class="lvl"><i class="on"></i><i class="on"></i><i class="on"></i></div><span class="tagline">{t("profesionalni nivo", "professional level", "Profi-Niveau")}</span><h3>{t("Pevačke tajne profesionalaca", "Secrets of professional singers", "Gesangsgeheimnisse der Profis")}</h3><p>{t("Za one kojima je pevanje posao ili cilj: scena, takmičenja i sopstveni stil.", "For those for whom singing is a job or a goal: the stage, competitions and a style of your own.", "Für alle, für die Singen Beruf oder Ziel ist: Bühne, Wettbewerbe und ein eigener Stil.")}</p></div>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{t("Cene", "Prices", "Preise")}</span><h2>{t("Jasno i jednostavno.", "Clear and simple.", "Klar und einfach.")}</h2>
    <p class="lead">{t("Zbog velikog interesovanja termini se rezervišu na mesečnom nivou.", "Due to high demand, lesson times are booked on a monthly basis.", "Wegen der großen Nachfrage werden Termine monatlich reserviert.")}</p></div>
  <div class="prices">
    <div class="price"><h3>{t("Probni čas", "Trial lesson", "Probestunde")}</h3><div class="amount">30 € </div><ul><li>{t("Upoznavanje i procena glasa", "Getting to know you and assessing your voice", "Kennenlernen und Einschätzung deiner Stimme")}</li><li>{t("Dogovor oko kursa i termina", "Agreeing on the course and lesson times", "Absprache zu Kurs und Terminen")}</li></ul><a class="btn btn-ghost" href="prijava.html">{t("Zakaži probni čas", "Book a trial lesson", "Probestunde buchen")}</a></div>
    <div class="price featured"><span class="tag">{t("Paket", "Package", "Paket")}</span><h3>{t("8 časova × 60 minuta", "8 lessons × 60 minutes", "8 Stunden × 60 Minuten")}</h3><div class="amount">200 € <small>{t("za decu i odrasle", "for children and adults", "für Kinder und Erwachsene")}</small></div>
      <ul><li>{t("Koristiš za mesec dana (2 časa nedeljno) ili dva meseca (1 čas nedeljno)", "Use it over one month (2 lessons a week) or two months (1 lesson a week)", "Für einen Monat (2 Stunden pro Woche) oder zwei Monate (1 Stunde pro Woche)")}</li><li>{t("Svi časovi se snimaju", "All lessons are recorded", "Alle Stunden werden aufgezeichnet")}</li><li>{t("Opciono: 24/7 Online Singing Support", "Optional: 24/7 Online Singing Support", "Optional: 24/7 Online Singing Support")}</li></ul>
      <a class="btn" href="prijava.html">{signup_btn}</a></div>
  </div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{t("Zakazivanje", "Booking", "Buchung")}</span><h2>{t("Od prijave do prvog časa.", "From sign-up to your first lesson.", "Von der Anmeldung zur ersten Stunde.")}</h2></div>
  <div class="steps" style="--cols:4">
    <div class="step"><span class="n">01</span><h3>{t("Popuni prijavu", "Fill in the form", "Formular ausfüllen")}</h3><p>{t("Odgovori na nekoliko pitanja u formi za prijavu i pošalji.", "Answer a few questions in the sign-up form and send it.", "Beantworte ein paar Fragen im Anmeldeformular und schick es ab.")}</p></div>
    <div class="step"><span class="n">02</span><h3>{t("Stiže ti email", "You get an email", "Du bekommst eine E-Mail")}</h3><p>{t("Dobijaš sve potrebne informacije i slobodne termine.", "You receive all the information you need and the available times.", "Du erhältst alle nötigen Infos und die freien Termine.")}</p></div>
    <div class="step"><span class="n">03</span><h3>{t("Rezerviši termine", "Book your times", "Termine reservieren")}</h3><p>{t("Sa mentorkom dogovaraš fiksne termine za ceo paket.", "You agree fixed times for the whole package with your mentor.", "Mit deiner Mentorin vereinbarst du feste Termine für das ganze Paket.")}</p></div>
    <div class="step"><span class="n">04</span><h3>{t("Uplata", "Payment", "Zahlung")}</h3><p>{t("Podaci za uplatu stižu emailom. Dokaz o uplati šalješ najkasnije dan pre prvog časa.", "Payment details arrive by email. You send proof of payment no later than the day before your first lesson.", "Die Zahlungsdaten kommen per E-Mail. Den Zahlungsnachweis schickst du spätestens einen Tag vor der ersten Stunde.")}</p></div>
  </div>
  <p class="muted" style="margin-top:28px">{t("Ako dokaz o uplati ne stigne na vreme, rezervisani termin se otkazuje. Konsultacije sa mentorkom moguće su svakog dana.", "If proof of payment doesn't arrive in time, the reserved slot is cancelled. You can consult your mentor every day.", "Kommt der Zahlungsnachweis nicht rechtzeitig, wird der reservierte Termin storniert. Rücksprache mit der Mentorin ist jeden Tag möglich.")}</p>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{t("Česta pitanja", "FAQ", "Häufige Fragen")}</span><h2>{t("Pre nego što se prijaviš.", "Before you sign up.", "Bevor du dich anmeldest.")}</h2></div>
  <div class="faq">''' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ) + '''</div>
</div></section>''' + CTA()
    page("kursevi.html", t("Kursevi i cene", "Courses & prices", "Kurse & Preise"),
         t("Kursevi pevanja (početni, napredni, profesionalni), cene i postupak zakazivanja online časova.",
           "Singing courses (beginner, advanced, professional), prices and how to book online lessons.",
           "Gesangskurse (Einstieg, Fortgeschritten, Profi), Preise und Ablauf der Buchung von Online-Stunden."), courses)

    # ---------- PRIJAVA ----------
    def radios(name, opts):
        return '<div class="options">' + "".join(f'<label class="opt"><input type="radio" name="{name}" value="{E(o)}"{" checked" if i == 0 else ""}><span>{E(o)}</span></label>' for i, o in enumerate(opts)) + "</div>"
    yes, no = t("Da", "Yes", "Ja"), t("Ne", "No", "Nein")
    signup = page_hero(t("Prijava", "Sign up", "Anmeldung"),
                       t("Prijavi se i zakaži čas.", "Sign up and book a lesson.", "Melde dich an und buche eine Stunde."),
                       t("Popuni prijavu i pošalji. Na email ti stižu sve informacije i slobodni termini.",
                         "Fill in the form and send it. You'll get all the information and available times by email.",
                         "Füll das Formular aus und schick es ab. Alle Infos und freien Termine bekommst du per E-Mail.")) + f'''
<section><div class="wrap split">
  <div class="prose" style="align-content:start">
    <span class="eyebrow">{t("Šta se dešava posle", "What happens next", "Wie es weitergeht")}</span>
    <ul class="creds">
      <li><span class="yr">{t("korak 1", "step 1", "Schritt 1")}</span><span>{t("Šalješ prijavu", "You send the form", "Du schickst die Anmeldung")}</span></li>
      <li><span class="yr">{t("korak 2", "step 2", "Schritt 2")}</span><span>{t("Email sa informacijama i terminima", "Email with information and times", "E-Mail mit Infos und Terminen")}</span></li>
      <li><span class="yr">{t("korak 3", "step 3", "Schritt 3")}</span><span>{t("Dogovor fiksnih termina", "Agreeing fixed times", "Feste Termine vereinbaren")}</span></li>
      <li><span class="yr">{t("korak 4", "step 4", "Schritt 4")}</span><span>{t("Uplata i prvi čas", "Payment and first lesson", "Zahlung und erste Stunde")}</span></li>
    </ul>
    <p>{t("Probni čas košta 30 €, a paket od 8 časova 200 €.", "A trial lesson costs €30, and a package of 8 lessons €200.", "Eine Probestunde kostet 30 €, ein Paket mit 8 Stunden 200 €.")} <a class="textlink" href="kursevi.html">{t("Detalji", "Details", "Details")}</a></p>
  </div>
  <form class="signup" id="signup" novalidate>
    <div class="form-row">
      <div class="field"><label for="f-name">{t("Ime i prezime", "Full name", "Vor- und Nachname")}</label><input id="f-name" name="ime" autocomplete="name" required></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="form-row">
      <div class="field"><label for="f-birth">{t("Datum rođenja", "Date of birth", "Geburtsdatum")}</label><input id="f-birth" name="datum_rodjenja" type="date"></div>
      <div class="field"><label for="f-course">{t("Kurs", "Course", "Kurs")}</label><select id="f-course" name="kurs"><option>{t("Probni čas", "Trial lesson", "Probestunde")}</option><option>{t("Buđenje muzičkog sluha (početni)", "Awakening your musical ear (beginner)", "Das musikalische Gehör wecken (Einstieg)")}</option><option>{t("Pravilna tehnika pevanja (napredni)", "Correct singing technique (advanced)", "Die richtige Gesangstechnik (Fortgeschritten)")}</option><option>{t("Pevačke tajne profesionalaca", "Secrets of professional singers", "Gesangsgeheimnisse der Profis")}</option></select></div>
    </div>
    <fieldset class="field"><legend>{t("Prethodno muzičko iskustvo", "Previous musical experience", "Musikalische Vorerfahrung")}</legend>{radios("iskustvo", [no, yes])}</fieldset>
    <div class="field"><label for="f-genre">{t("Koji žanr te najviše zanima?", "Which genre interests you most?", "Welches Genre interessiert dich am meisten?")}</label><input id="f-genre" name="zanr" placeholder="{t("npr. pop, narodna, rock, etno", "e.g. pop, folk, rock, ethno", "z. B. Pop, Volksmusik, Rock, Ethno")}"></div>
    <fieldset class="field"><legend>24/7 Online Singing Support</legend>{radios("podrska", [yes, no])}</fieldset>
    <fieldset class="field"><legend>{t("Za časove sam saznao/la preko", "I heard about the lessons through", "Vom Unterricht erfahren habe ich über")}</legend>{radios("izvor", [t("Preporuke", "A recommendation", "Empfehlung"), t("Sajta", "The website", "Die Website"), t("Reklame", "An ad", "Werbung"), "Facebook" if L != "sr" else "Facebook-a", "Instagram" if L != "sr" else "Instagrama", "TikTok" if L != "sr" else "TikTok-a"])}</fieldset>
    <label class="consent"><input type="checkbox" id="f-consent"> <span>{t("Saglasan/na sam sa", "I agree to the", "Ich stimme der")} <a href="privatnost.html">{t("Politikom privatnosti", "Privacy policy", "Datenschutzerklärung")}</a> {t("i", "and", "und den")} <a href="uslovi.html">{t("Uslovima korišćenja", "Terms of use", "Nutzungsbedingungen")}</a> {t("i sa tim da se moji podaci čuvaju i koriste za internet marketing.", "and to my data being stored and used for online marketing.", "zu und bin damit einverstanden, dass meine Daten gespeichert und für Online-Marketing verwendet werden.")}</span></label>
    <button class="btn btn-primary" type="submit">{t("Pošalji prijavu", "Send", "Anmeldung senden")}</button>
    <p class="form-msg" id="form-msg" aria-live="polite"></p>
  </form>
</div></section>'''
    page("prijava.html", t("Prijava", "Sign up", "Anmeldung"),
         t("Prijava za online časove pevanja kod MA Sanje Trifunović Gerginov.", "Sign up for online singing lessons with MA Sanja Trifunović Gerginov.", "Anmeldung zum Online-Gesangsunterricht bei MA Sanja Trifunović Gerginov."), signup)

    # ---------- VEŽBAONICA ----------
    notes = [(48, t("C3 · niži muški", "C3 · lower male", "C3 · tiefe Männerstimme")), (53, "F3"), (55, "G3"), (57, "A3"),
             (60, t("C4 · srednji", "C4 · middle", "C4 · Mitte")), (62, "D4"), (65, t("F4 · viši ženski", "F4 · higher female", "F4 · hohe Frauenstimme")), (67, "G4")]
    opts = "".join(f'<option value="{m}"{" selected" if m == 60 else ""}>{n}</option>' for m, n in notes)
    practice = f'''<section class="dark" style="padding-top:clamp(40px,6vw,80px)"><div class="wrap piano-panel">
  <div class="sec-head" style="margin-bottom:6px"><span class="eyebrow">{t("Vežbaonica", "Practice room", "Übungsraum")}</span>
    <h1 style="font-size:clamp(2.4rem,6vw,4.4rem);font-weight:800;letter-spacing:-.04em">{t("Zagrej glas uz klavir.", "Warm up with the piano.", "Einsingen am Klavier.")}</h1>
    <p class="lead">{t("Izaberi vežbu i početni ton, pa pritisni Pokreni. Pevaj slogove dok klavir svira. Posle svakog kruga vežba se podiže za pola stepena. Dirke možeš i sam da sviraš.",
                      "Pick an exercise and a starting note, then press Start. Sing the syllables while the piano plays. After each round the exercise goes up a semitone. You can play the keys yourself, too.",
                      "Wähle eine Übung und einen Anfangston und drück auf Start. Sing die Silben, während das Klavier spielt. Nach jeder Runde geht die Übung einen Halbton höher. Du kannst die Tasten auch selbst spielen.")}</p></div>
  <div class="exercises">
    <button class="ex" type="button" data-ex="lestvica" aria-pressed="true"><b>{t("Lestvica do kvinte", "Scale up to the fifth", "Tonleiter bis zur Quinte")}</b><span>do · re · mi · fa · sol · fa · mi · re · do</span></button>
    <button class="ex" type="button" data-ex="trozvuk" aria-pressed="false"><b>{t("Razloženi akord", "Broken chord", "Gebrochener Akkord")}</b><span>ma · ma · ma · ma (do · mi · sol · do)</span></button>
    <button class="ex" type="button" data-ex="vokali" aria-pressed="false"><b>{t("Vokali na jednom tonu", "Vowels on one note", "Vokale auf einem Ton")}</b><span>mi · me · ma · mo · mu</span></button>
  </div>
  <div class="piano-scroll"><div class="piano" id="piano" aria-label="{t("Klavijatura od C3 do C6", "Keyboard from C3 to C6", "Klaviatur von C3 bis C6")}"></div></div>
  <div class="controls">
    <button class="btn btn-rose" id="play" type="button">▶ {t("Pokreni", "Start", "Start")}</button>
    <button class="btn btn-ghost" id="stop" type="button">■ {t("Stani", "Stop", "Stopp")}</button>
    <label class="ctrl" for="start">{t("Početni ton", "Starting note", "Anfangston")} <select id="start">{opts}</select></label>
    <label class="ctrl" for="tempo">{t("Tempo", "Tempo", "Tempo")} <input id="tempo" type="range" min="60" max="160" value="110"></label>
  </div>
  <p class="solf" id="solf" aria-live="polite"></p>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{t("Pre nego što počneš", "Before you start", "Bevor du anfängst")}</span><h2>{t("Tri pravila za zdravo zagrevanje.", "Three rules for a healthy warm-up.", "Drei Regeln für gesundes Einsingen.")}</h2></div>
  <div class="grid-3">
    <div class="card"><span class="tagline">{t("disanje", "breathing", "Atmung")}</span><h3>{t("Vazduh je gorivo", "Air is fuel", "Luft ist Treibstoff")}</h3><p>{t("Udahni mirno i duboko pre svake fraze. Bez vazduha nema pevanja.", "Breathe in calmly and deeply before each phrase. Without air there is no singing.", "Atme vor jeder Phrase ruhig und tief ein. Ohne Luft kein Gesang.")}</p><a class="textlink" href="savet-pevacko-disanje.html" style="justify-self:start">{t("Pravilno disanje", "Correct breathing", "Richtiges Atmen")}</a></div>
    <div class="card"><span class="tagline">{t("držanje", "posture", "Haltung")}</span><h3>{t("Opušteno telo", "A relaxed body", "Ein entspannter Körper")}</h3><p>{t("Stani prirodno, ramena dole, vrat slobodan. Napet mišić znači napet ton.", "Stand naturally, shoulders down, neck free. A tense muscle means a tense tone.", "Steh natürlich, Schultern unten, Nacken frei. Ein angespannter Muskel bedeutet einen angespannten Ton.")}</p><a class="textlink" href="savet-drzanje-tela.html" style="justify-self:start">{t("Držanje tela", "Posture", "Körperhaltung")}</a></div>
    <div class="card"><span class="tagline">{t("mera", "moderation", "Maß")}</span><h3>{t("Bez forsiranja", "No forcing", "Nichts erzwingen")}</h3><p>{t("Kad ton postane težak, stani i vrati se na početni ton. Visina dolazi sa vežbom.", "When a note gets hard, stop and go back to the starting note. Range comes with practice.", "Wenn ein Ton schwer wird, hör auf und geh zurück zum Anfangston. Die Höhe kommt mit der Übung.")}</p></div>
  </div>
  <p class="ph-note" style="margin-top:28px">ŠABLON: Sanja proverava vežbe i savete; po želji dodajemo nove vežbe (npr. sirena, staccato, intervali).</p>
</div></section>''' + CTA()
    page("vezbaonica.html", t("Vežbaonica", "Practice room", "Übungsraum"),
         t("Interaktivna klavijatura sa vežbama za zagrevanje glasa.", "An interactive keyboard with vocal warm-up exercises.", "Eine interaktive Klaviatur mit Übungen zum Einsingen."), practice)

    # ---------- PEVAČKI SAVETI ----------
    cats = []
    for a in ARTS:
        if a["cat"] not in cats: cats.append(a["cat"])
    order = {"sr": ["Disanje", "Tehnika", "Glas", "Nastup", "Učenje"], "en": ["Breathing", "Technique", "Voice", "Performance", "Learning"],
             "de": ["Atmung", "Technik", "Stimme", "Auftritt", "Lernen"]}[L]
    cats = [c for c in order if c in cats] + [c for c in cats if c not in order]
    blog = page_hero(t("Pevački saveti", "Singing tips", "Gesangstipps"),
                     t("Saveti za pevače, od daha do scene.", "Tips for singers, from breath to stage.", "Tipps für Sänger, vom Atem bis zur Bühne."),
                     t("Kratki tekstovi o disanju, tehnici, glasu i tremi, da vežbaš pametnije između časova.",
                       "Short articles on breathing, technique, voice and stage fright, so you practise smarter between lessons.",
                       "Kurze Texte über Atmung, Technik, Stimme und Lampenfieber, damit du zwischen den Stunden klüger übst.")) + f'''
<section><div class="wrap">
  <div class="filters" role="group" aria-label="{t("Kategorije", "Categories", "Kategorien")}"><button class="filter" type="button" data-cat="sve" aria-pressed="true">{t("Sve", "All", "Alle")}</button>''' + "".join(f'<button class="filter" type="button" data-cat="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in cats) + '''</div>
  <div class="posts">''' + "".join(pc(p) for p in PS) + '''</div>
</div></section>''' + CTA()
    page("saveti.html", t("Pevački saveti", "Singing tips", "Gesangstipps"),
         t("Saveti o disanju, tehnici pevanja, glasu i tremi od MA Sanje Trifunović Gerginov.",
           "Tips on breathing, singing technique, voice and stage fright from MA Sanja Trifunović Gerginov.",
           "Tipps zu Atmung, Gesangstechnik, Stimme und Lampenfieber von MA Sanja Trifunović Gerginov."), blog)

    # ---------- ČLANCI ----------
    excerpts = dict(PS)
    for n, a in enumerate(ARTS):
        mins = max(1, math.ceil(a["words"] / 200))
        prev, nxt = ARTS[n - 1], ARTS[(n + 1) % len(ARTS)]
        body = f"""<section><div class="wrap"><article class="article">
  <a class="textlink" href="saveti.html" style="justify-self:start">← {t('Pevački saveti', 'Singing tips', 'Gesangstipps')}</a>
  <span class="eyebrow">{E(a["cat"])} · {mins} {t('min čitanja', 'min read', 'Min. Lesezeit')}</span>
  <h1 class="art-title">{E(a["title"])}</h1>
  {render_blocks(a["blocks"])}
  <p class="signature"><span>{t('Vaša', 'Yours,', 'Ihre')}</span>Sanja Trifunović Gerginov</p>
  <div class="btn-row"><a class="btn btn-rose" href="prijava.html">{t('Prijavi se', 'Sign up', 'Anmelden')}</a><a class="btn btn-ghost" href="vezbaonica.html">{t('Vežbaj odmah', 'Practise now', 'Jetzt üben')}</a></div>
</article>
<nav class="art-nav" aria-label="{t('Drugi saveti', 'More tips', 'Weitere Tipps')}">
  <a href="{href(prev["slug"])}"><small>← {t('Prethodni', 'Previous', 'Vorheriger')}</small>{E(prev["title"])}</a>
  <a href="{href(nxt["slug"])}" class="next"><small>{t('Sledeći', 'Next', 'Nächster')} →</small>{E(nxt["title"])}</a>
</nav></div></section>"""
        page(href(a["slug"]), a["title"], excerpts.get(a["slug"], a["title"]), body)

    # stari šablon članka preusmerava na listu saveta (samo na srpskom)
    if L == "sr":
        open(os.path.join(OUT, "clanak.html"), "w", encoding="utf-8").write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=saveti.html"><link rel="canonical" href="saveti.html"><a href="saveti.html">Pevački saveti</a>\n')

    # ---------- UTISCI ----------
    reviews = page_hero(t("Utisci", "Reviews", "Stimmen"),
                        t("Učenici iz šest zemalja.", "Students from six countries.", "Schüler aus sechs Ländern."),
                        t("Srbija, Austrija, Nemačka, Švajcarska, Bosna i Hercegovina. Evo šta kažu oni koji već pevaju sa Sanjom.",
                          "Serbia, Austria, Germany, Switzerland, Bosnia and Herzegovina. Here's what those already singing with Sanja say.",
                          "Serbien, Österreich, Deutschland, Schweiz, Bosnien und Herzegowina. Das sagen alle, die schon mit Sanja singen.")) + '''
<section><div class="wrap">
  <div class="quotes masonry">''' + "".join(tq(x) for x in TS) + '''</div>
  <p class="ph-note" style="margin-top:12px">ŠABLON: utisci su skraćeni; pune tekstove prenosimo sa starog sajta. Uz dozvolu učenika mogu se dodati i fotografije ili kratki video snimci.</p>
</div></section>''' + CTA()
    page("utisci.html", t("Utisci", "Reviews", "Stimmen"),
         t("Utisci učenika online časova pevanja sa Sanjom.", "Reviews from students of online singing lessons with Sanja.", "Stimmen von Schülern des Online-Gesangsunterrichts mit Sanja."), reviews)

    # ---------- PRAVNE STRANICE ----------
    for fn, title in [("privatnost.html", t("Politika privatnosti", "Privacy policy", "Datenschutzerklärung")),
                      ("uslovi.html", t("Uslovi korišćenja", "Terms of use", "Nutzungsbedingungen"))]:
        body = page_hero(t("Pravne informacije", "Legal", "Rechtliches"), title, t("Poslednja izmena: [datum]", "Last updated: [date]", "Zuletzt aktualisiert: [Datum]")) + f'''
<section><div class="wrap"><div class="article"><p class="ph-note">ŠABLON: ovde ide tekst „{title}“ sa postojećeg sajta, preuzet u celosti.</p></div></div></section>'''
        page(fn, title, f"{title} — {SITE()}.", body)


for L in LANGS:
    R = "" if L == "sr" else "../"
    build()

print("ok")
