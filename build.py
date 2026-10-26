"""Generiše statične stranice sajta iz zajedničkih delova (meni, podnožje)."""
import os, html
import sys
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
ARTIFACT = "--artifact" in sys.argv
E = html.escape

SITE = "Časovi pevanja sa Sanjom"
TEACHER = "MA Sanja Trifunović Gerginov"
VIDEO = "https://www.youtube.com/watch?v=kQUhk-6FKRM"

NAV = [("index.html", "Početna"), ("o-sanji.html", "O Sanji"), ("kursevi.html", "Kursevi i cene"),
       ("vezbaonica.html", "Vežbaonica"), ("saveti.html", "Pevački saveti"), ("utisci.html", "Utisci")]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Figtree:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">')

LOGO = f'<span class="logo-keys" aria-hidden="true"><i></i><i></i><i></i></span><span>Časovi pevanja<small>sa Sanjom · online</small></span>'

def head(title, desc):
    t = SITE if title is None else f"{title} · {SITE}"
    return (f'<title>{E(t)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{E(desc)}">\n{FONTS}\n<link rel="stylesheet" href="style.css">\n')

CUR = ' aria-current="page"'
NEW = '<span class="new">novo</span>'
def header(cur):
    links = "".join(
        f'<a href="{h}"{CUR if h == cur else ""}>{E(l)}{NEW if h == "vezbaonica.html" else ""}</a>'
        for h, l in NAV)
    return f'''<header class="nav"><div class="wrap">
  <a class="logo" href="index.html">{LOGO}</a>
  <nav class="nav-links" aria-label="Glavna navigacija">{links}</nav>
  <a class="btn btn-rose cta-top" href="prijava.html">Prijavi se</a>
  <button class="menu-btn" type="button" aria-expanded="false">Meni</button>
</div></header>'''

FOOTER = f'''<footer><div class="wrap">
  <div class="cols">
    <div style="display:grid;gap:14px;align-content:start">
      <span class="logo">{LOGO}</span>
      <p style="opacity:.75;max-width:40ch;font-size:.94rem">Online časovi pevanja za decu i odrasle, na srpskom, engleskom i nemačkom jeziku.</p>
    </div>
    <div><h4>Sajt</h4><ul>
      <li><a href="o-sanji.html">O Sanji</a></li><li><a href="kursevi.html">Kursevi i cene</a></li>
      <li><a href="prijava.html">Prijava</a></li><li><a href="vezbaonica.html">Vežbaonica</a></li>
      <li><a href="saveti.html">Pevački saveti</a></li><li><a href="utisci.html">Utisci</a></li></ul></div>
    <div><h4>Kontakt i mreže</h4><ul>
      <li>Email: <span class="ph-inline">[dodati]</span></li>
      <li>Instagram: <span class="ph-inline">[dodati]</span></li>
      <li>TikTok: <span class="ph-inline">[dodati]</span></li>
      <li><a href="{VIDEO}" target="_blank" rel="noopener">YouTube ↗</a></li></ul></div>
  </div>
  <div class="bottom"><span>© <span data-year>2026</span> {SITE}. Sva prava zadržana.</span>
    <span><a href="privatnost.html">Politika privatnosti</a> · <a href="uslovi.html">Uslovi korišćenja</a></span></div>
</div></footer>
<script src="site.js"></script>'''

DOC_START = '<!doctype html>\n<html lang="sr-Latn">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'

def page(fname, title, desc, body, root=False):
    h = head(title, desc)
    if root and ARTIFACT:  # početna u Artifact pregledu: Artifact sam dodaje doctype/head/body
        out = h + header(fname) + "\n<main>\n" + body + "\n</main>\n" + FOOTER
    else:
        out = (DOC_START + h + "</head>\n<body>\n" + header(fname) + "\n<main>\n" + body + "\n</main>\n" + FOOTER + "\n</body>\n</html>\n")
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(out)

def page_hero(eyebrow, h1, lead):
    return f'''<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p></div></section>'''

CTA = '''<section class="dark"><div class="wrap cta-band">
  <h2>Svoju blistavu budućnost stvaraš ti.</h2>
  <div class="btn-row"><a class="btn btn-rose" href="prijava.html">Prijavi se i zakaži čas</a><a class="btn btn-ghost" href="kursevi.html">Pogledaj kurseve</a></div>
</div></section>'''

# ---------- podaci sa postojećeg sajta ----------
TESTIMONIALS = [
    ("Miletić Vladan", "Beograd, Srbija", "Ako misliš da za pevanje nisi Bogom dan, sa Sanjom ćeš od pevanja kupiti stan!"),
    ("Ignjat Marković", "Beč, Austrija", "Na Grandovoj audiciji su mi rekli da nisam za muziku, danas se samo time bavim i od toga živim."),
    ("Goran Stojković", "Nürnberg, Nemačka", "Već na prvom probnom času znao sam da ću dalje raditi sa Sanjom, jer je pre svega izuzetno kompetentna…"),
    ("Pavle Marković", "Gradiška, BiH", "Sanja mi je mnogo pomogla sa visokim tonovima. Baš mi se svidelo što ima nekoliko glavnih pravila koje sam sledio…"),
    ("Marko Savković", "Lucern, Švajcarska", "Ja sam počeo od nule, prvo smo radili na mom sluhu godinu dana… Nakon otprilike godinu i po dana sam našao svoj prvi bend."),
    ("Milena Radovanović", "Smederevo, Srbija", "Sanjini časovi su, pre svega, jedna motivacijska bomba. Ona vas ohrabruje da se držite sebe i svog puta…"),
    ("Aleksandar Gajić", "Cirih, Švajcarska", "Nažalost, nisam uspeo da se upišem na intenzivni kurs jer je brzinom svetlosti popunjen…"),
    ("Mario", "Grac, Austrija", "Sanja je pevački guru! Jedna od retkih profesora za koju ne postoje prepreke da nekog nauči."),
    ("Marina Maksimović", "Aleksinac, Srbija", "Pevanje je moj posao. Sada pevam zahtevne pesme, ne postoji više pesma koja mi predstavlja problem!"),
    ("Helena Simić", "Beč, Austrija", "Puno stvari sam naučila o pravilima pevanja. Zadovoljstvo je raditi sa Sanjom, jer radi nesebično, punim srcem."),
    ("Nenad Milivojević", "Lucern, Švajcarska", "Ubedljivo najbolji časovi pevanja! Sanja veoma dobro objašnjava, ima pravi odgovor na svako pitanje."),
]
def tq(t):
    n, c, q = t
    return f'<figure class="q" style="margin:0"><p>„{E(q)}“</p><figcaption class="who"><b>{E(n)}</b>{E(c)}</figcaption></figure>'

POSTS = [
    ("Učenje", "Koliko je časova potrebno da naučim da pevam?", "Koliko brzo će učenik napredovati na časovima pevanja zavisi, zapravo, od nekoliko faktora."),
    ("Disanje", "Svakodnevno pravilno disanje kao glavni preduslov za zdrav život i dobro pevanje", "Sigurno ste čuli za izraz „disati punim plućima“. To znači živeti ispunjen život, punim kapacitetom."),
    ("Tehnika", "Pravilno držanje tela prilikom pevanja", "Držanje tela svakog pevača treba da bude prirodno da bi svi mišići u telu bili opušteni."),
    ("Učenje", "Koje su prednosti online nastave?", "Online nastava je postala deo naše svakodnevnice i povezuje vas sa najkvalitetnijim profesorima širom sveta."),
    ("Glas", "Kako govoriti jasno, razgovetno i lepo?", "Ukoliko jasno i razgovetno govorite, ostavljate veoma lep utisak na sagovornika."),
    ("Glas", "Zbog čega je pevanje zdravo?", "Pevanje podiže samopouzdanje, kada otkrijemo svoju strast i počnemo njome da se bavimo."),
    ("Glas", "Šta ako ne volim boju svog glasa?", "Svima se nama desilo da svoj glas prilikom govora doživljavamo na jedan način…"),
    ("Disanje", "Pravilno disanje prilikom pevanja", "Nama je vazduh gorivo. Vazduh je sve. Vazduh je pevačka moć. Bez vazduha nema pevanja."),
    ("Nastup", "Kako pobediti strah od javnog nastupa?", "Javni nastup može biti jedno stresno iskustvo ukoliko u glavi imamo negativna očekivanja."),
]
def pc(p):
    c, t, x = p
    return f'<a class="post-card" href="clanak.html" data-cat="{c}"><span class="cat">{c}</span><h3>{E(t)}</h3><p>{E(x)}</p><span class="more">Pročitaj →</span></a>'

# ---------- POČETNA ----------
home = f'''<section class="hero"><div class="wrap hero-grid">
  <div class="hero-copy">
    <span class="eyebrow">Online časovi pevanja · deca i odrasli</span>
    <h1>Otkrij svoj glas. <span class="accent">Peva se</span> odavde.</h1>
    <p class="lead">Individualni časovi pevanja preko video poziva, za početnike, napredne i pripremu za takmičenja. Zajedno otkrivamo i razvijamo originalni i jedinstveni stil tvog pevanja.</p>
    <div class="btn-row"><a class="btn btn-rose" href="prijava.html">Prijavi se</a><a class="btn btn-ghost" href="vezbaonica.html">Isprobaj Vežbaonicu →</a></div>
    <div class="chips"><span class="chip">narodna</span><span class="chip">pop</span><span class="chip">rock</span><span class="chip">etno</span><span class="chip">SR · EN · DE</span></div>
  </div>
  <div class="hero-photo"><img src="img/klavir.jpg" alt="Otvorene note na klaviru, iza njih mehanika klavira i osušeni božur">
    <div class="hero-badge"><span class="live-dot" aria-hidden="true"></span><span><strong>{TEACHER}</strong><br>vokalni pedagog, Beč</span></div></div>
</div></section>
<div class="facts"><div class="wrap">
  <div class="fact"><b>15 godina</b><span>podučavanja vokalne tehnike</span></div>
  <div class="fact"><b>od 2004.</b><span>profesionalno peva</span></div>
  <div class="fact"><b>3 jezika</b><span>srpski, engleski, nemački</span></div>
  <div class="fact"><b>svi kontinenti</b><span>učenici širom sveta</span></div>
</div></div>

<section><div class="wrap split">
  <div style="display:grid;gap:22px"><span class="eyebrow">Upoznaj Sanju</span>
    <p class="big-quote">Za učenje pevanja preduslov je da učenik ima želju za učenjem i napretkom.</p></div>
  <div class="prose">
    <p><strong>{TEACHER}</strong> je vrhunski muzički pedagog sa 15 godina iskustva u podučavanju vokalne tehnike. Završila je master studije na Fakultetu muzičke umetnosti u Beogradu i stručno usavršavanje u Austriji.</p>
    <p>Autor je nekoliko stručnih publikacija o vokalnoj tehnici, a njena najnovija publikacija o osnovama vokalne tehnike je u pripremi.</p>
    <p><a class="textlink" href="o-sanji.html">Pročitaj više o Sanji</a></p>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Želiš li da ti pevanje postane posao, zanimanje, životni poziv?</span><h2>Tri kursa, jedan cilj: tvoj glas.</h2></div>
  <div class="grid-3">
    <a class="card level" href="kursevi.html" style="text-decoration:none"><div class="lvl"><i class="on"></i><i></i><i></i></div><span class="tagline">početni</span><h3>Buđenje muzičkog sluha</h3><p>Za one koji tek počinju. Fokus na tačnoj intonaciji.</p></a>
    <a class="card level" href="kursevi.html" style="text-decoration:none"><div class="lvl"><i class="on"></i><i class="on"></i><i></i></div><span class="tagline">napredni</span><h3>Pravilna tehnika pevanja</h3><p>Disanje, držanje, opseg i elementi tvog omiljenog žanra.</p></a>
    <a class="card level" href="kursevi.html" style="text-decoration:none"><div class="lvl"><i class="on"></i><i class="on"></i><i class="on"></i></div><span class="tagline">profesionalni</span><h3>Pevačke tajne profesionalaca</h3><p>Za scenu, takmičenja i pevanje kao zanimanje.</p></a>
  </div>
  <div class="sec-foot"><a class="textlink" href="kursevi.html">Cene i zakazivanje</a></div>
</div></section>

<section class="dark"><div class="wrap" style="display:grid;gap:40px">
  <a class="video-card" href="{VIDEO}" target="_blank" rel="noopener">
    <div class="video-thumb"><span class="play" aria-hidden="true"></span></div>
    <div class="video-text"><span class="eyebrow">Video uputstvo</span><h2 style="font-size:clamp(1.7rem,3vw,2.4rem)">Otkrijte sa mnom sve pevačke tajne!</h2><p class="muted">Pogledaj na YouTube-u ↗</p></div>
  </a>
  <div class="split" style="align-items:center">
    <div style="display:grid;gap:14px"><span class="eyebrow">Novo · Vežbaonica</span><h2>Zagrej glas uz klavir, bilo kad.</h2></div>
    <div style="display:grid;gap:18px"><p class="lead">Interaktivna klavijatura sa vežbama za zagrevanje. Izabereš vežbu i početni ton, klavir svira, a ti pevaš. Svaki krug se podiže za pola stepena.</p>
      <div class="btn-row"><a class="btn btn-rose" href="vezbaonica.html">Otvori Vežbaonicu</a></div></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Utisci učenika</span><h2>Od Beograda do Lucerna.</h2></div>
  <div class="quotes">{tq(TESTIMONIALS[1])}{tq(TESTIMONIALS[4])}{tq(TESTIMONIALS[10])}</div>
  <div class="sec-foot"><a class="textlink" href="utisci.html">Svi utisci (11)</a></div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Pevački saveti</span><h2>Čitaj između časova.</h2></div>
  <div class="posts">{pc(POSTS[0])}{pc(POSTS[1])}{pc(POSTS[2])}</div>
  <div class="sec-foot"><a class="textlink" href="saveti.html">Svi saveti</a></div>
</div></section>
{CTA}'''
page("index.html", None, "Online časovi pevanja za decu i odrasle sa MA Sanjom Trifunović Gerginov: početnici, napredni i priprema za takmičenja.", home, root=True)

# ---------- O SANJI ----------
about = page_hero("O Sanji", "Glas, scena i 15 godina u učionici.", "Vokalni pedagog, online profesorka pevanja i predavač vokalne tehnike. Živi i radi u Beču, a predaje učenicima na svim kontinentima.") + f'''
<section><div class="wrap split">
  <div style="display:grid;gap:14px">
    <figure class="about-photo"><img src="img/sanja.jpg" alt="Sanja Trifunović Gerginov pored klavijature, sa peharom" loading="lazy"></figure>
  </div>
  <div class="prose">
    <p><strong>{TEACHER}</strong> profesionalno se bavi pevanjem od 2004. godine. Priznati je vokalni izvođač, sa nagradama u zemlji i inostranstvu.</p>
    <p>Završila je master akademske studije na Fakultetu muzičke umetnosti u Beogradu. Radila je kao profesor muzičke kulture u školama u Beogradu i Jagodini i bila dugogodišnji saradnik u nastavi na Fakultetu pedagoških nauka u Jagodini.</p>
    <p>Danas živi i radi u Beču, gde predaje i drži predavanja iz vokalne tehnike i nastavlja stručno usavršavanje. Vodi međunarodnu online školu pevanja na srpskom, engleskom i nemačkom jeziku, a govori i italijanski.</p>
    <ul class="creds">
      <li><span class="yr">od 2004.</span><span>Profesionalni vokalni izvođač, nagrade u zemlji i inostranstvu</span></li>
      <li><span class="yr">FMU Beograd</span><span>Master akademske studije</span></li>
      <li><span class="yr">Beograd · Jagodina</span><span>Profesor muzičke kulture; saradnik u nastavi na Fakultetu pedagoških nauka</span></li>
      <li><span class="yr">od 2014.</span><span>Suosnivač KUD-a „Jovanča Micić“, predavač vokalne tehnike</span></li>
      <li><span class="yr">Austrija</span><span>Stručno usavršavanje; predavanja iz vokalne tehnike u Beču</span></li>
      <li><span class="yr">u pripremi</span><span>Nova publikacija o osnovama vokalne tehnike</span></li>
    </ul>
  </div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Metoda</span><h2>24/7 Online Singing Support</h2>
    <p class="lead">Napredak se ne dešava samo na času. Zato Sanja prati tvoje vežbanje i između časova.</p></div>
  <div class="steps" style="--cols:4">
    <div class="step"><span class="n">01 · posle časa</span><h3>Pisane smernice</h3><p>Dobijaš uputstva i vežbaš kod kuće.</p></div>
    <div class="step"><span class="n">02 · vežbanje</span><h3>Tvoj snimak</h3><p>Snimiš najbolji audio sa vežbanja i pošalješ ga Sanji.</p></div>
    <div class="step"><span class="n">03 · isti dan</span><h3>Nove smernice</h3><p>Sanja pregleda snimke na kraju radnog dana i brzo šalje nove smernice.</p></div>
    <div class="step"><span class="n">04 · uvek</span><h3>Snimljeni časovi</h3><p>Svi časovi se snimaju, pa možeš da ih pogledaš ponovo.</p></div>
  </div>
</div></section>

<section><div class="wrap split">
  <div style="display:grid;gap:22px"><span class="eyebrow">Zašto online</span>
    <p class="big-quote">Časove održavam online jer imam učenike na svim kontinentima.</p></div>
  <div class="prose">
    <p>Biraš žanr koji voliš: narodna muzika, pop, rock ili etno. Na časovima radimo na svim karakterističnim elementima tvog omiljenog žanra.</p>
    <p>Za napredak su potrebni motivacija i spremnost da vežbaš svakog dana. Mnogi bivši učenici danas pevaju samostalno, a Sanja ostaje u kontaktu sa njima i posle završenih časova.</p>
  </div>
</div></section>
{CTA}'''
page("o-sanji.html", "O Sanji", "Biografija MA Sanje Trifunović Gerginov, vokalnog pedagoga i online profesorke pevanja iz Beča.", about)

# ---------- KURSEVI I CENE ----------
FAQ = [
    ("Koliko časova mi treba da naučim da pevam?", "Zavisi od sluha i osećaja za ritam, od toga koliko vežbaš i koliko često imaš časove. Uz redovno vežbanje, posle dva i po do tri meseca obično si zadovoljan onim što čuješ."),
    ("Na kom jeziku se drže časovi?", "Na srpskom, engleskom ili nemačkom."),
    ("Da li su časovi i za decu?", "Da, časovi su za decu i odrasle."),
    ("Šta je 24/7 Online Singing Support?", "Između časova šalješ snimke vežbanja, a Sanja ti vraća nove smernice. Opciju biraš u prijavi."),
    ("Da li se časovi snimaju?", "Da, svi časovi se snimaju, pa možeš da ih pogledaš ponovo."),
    ("Kako otkazujem čas?", "Čas se otkazuje najkasnije dan ranije."),
]
courses = page_hero("Kursevi i cene", "Individualni časovi, po tvojoj meri.", "Svi časovi su individualni, a termini se prilagođavaju tebi. U prijavi navedi naziv kursa koji te zanima.") + '''
<section><div class="wrap">
  <div class="grid-3">
    <div class="card level"><div class="lvl"><i class="on"></i><i></i><i></i></div><span class="tagline">početni nivo</span><h3>Buđenje muzičkog sluha</h3><p>Prvi koraci u pevanju. Radimo na sluhu i tačnoj intonaciji, da čuješ i ponoviš ton koji sviram.</p></div>
    <div class="card level"><div class="lvl"><i class="on"></i><i class="on"></i><i></i></div><span class="tagline">napredni nivo</span><h3>Pravilna tehnika pevanja</h3><p>Disanje, držanje tela, opseg i karakteristični elementi tvog omiljenog žanra.</p></div>
    <div class="card level"><div class="lvl"><i class="on"></i><i class="on"></i><i class="on"></i></div><span class="tagline">profesionalni nivo</span><h3>Pevačke tajne profesionalaca</h3><p>Za one kojima je pevanje posao ili cilj: scena, takmičenja i sopstveni stil.</p></div>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Cene</span><h2>Jasno i jednostavno.</h2>
    <p class="lead">Zbog velikog interesovanja termini se rezervišu na mesečnom nivou.</p></div>
  <div class="prices">
    <div class="price"><h3>Probni čas</h3><div class="amount">30 € </div><ul><li>Upoznavanje i procena glasa</li><li>Dogovor oko kursa i termina</li></ul><a class="btn btn-ghost" href="prijava.html">Zakaži probni čas</a></div>
    <div class="price featured"><span class="tag">Paket</span><h3>8 časova × 60 minuta</h3><div class="amount">200 € <small>za decu i odrasle</small></div>
      <ul><li>Koristiš za mesec dana (2 časa nedeljno) ili dva meseca (1 čas nedeljno)</li><li>Svi časovi se snimaju</li><li>Opciono: 24/7 Online Singing Support</li></ul>
      <a class="btn" href="prijava.html">Prijavi se</a></div>
  </div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Zakazivanje</span><h2>Od prijave do prvog časa.</h2></div>
  <div class="steps" style="--cols:4">
    <div class="step"><span class="n">01</span><h3>Popuni prijavu</h3><p>Odgovori na nekoliko pitanja u formi za prijavu i pošalji.</p></div>
    <div class="step"><span class="n">02</span><h3>Stiže ti email</h3><p>Dobijaš sve potrebne informacije i slobodne termine.</p></div>
    <div class="step"><span class="n">03</span><h3>Rezerviši termine</h3><p>Sa mentorkom dogovaraš fiksne termine za ceo paket.</p></div>
    <div class="step"><span class="n">04</span><h3>Uplata</h3><p>Podaci za uplatu stižu emailom. Dokaz o uplati šalješ najkasnije dan pre prvog časa.</p></div>
  </div>
  <p class="muted" style="margin-top:28px">Ako dokaz o uplati ne stigne na vreme, rezervisani termin se otkazuje. Konsultacije sa mentorkom moguće su svakog dana.</p>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Česta pitanja</span><h2>Pre nego što se prijaviš.</h2></div>
  <div class="faq">''' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ) + '''</div>
</div></section>''' + CTA
page("kursevi.html", "Kursevi i cene", "Kursevi pevanja (početni, napredni, profesionalni), cene i postupak zakazivanja online časova.", courses)

# ---------- PRIJAVA ----------
def radios(name, opts):
    return '<div class="options">' + "".join(f'<label class="opt"><input type="radio" name="{name}" value="{E(o)}"{" checked" if i == 0 else ""}><span>{E(o)}</span></label>' for i, o in enumerate(opts)) + "</div>"
signup = page_hero("Prijava", "Prijavi se i zakaži čas.", "Popuni prijavu i pošalji. Na email ti stižu sve informacije i slobodni termini.") + f'''
<section><div class="wrap split">
  <div class="prose" style="align-content:start">
    <span class="eyebrow">Šta se dešava posle</span>
    <ul class="creds">
      <li><span class="yr">korak 1</span><span>Šalješ prijavu</span></li>
      <li><span class="yr">korak 2</span><span>Email sa informacijama i terminima</span></li>
      <li><span class="yr">korak 3</span><span>Dogovor fiksnih termina</span></li>
      <li><span class="yr">korak 4</span><span>Uplata i prvi čas</span></li>
    </ul>
    <p>Probni čas košta 30 €, a paket od 8 časova 200 €. <a class="textlink" href="kursevi.html">Detalji</a></p>
  </div>
  <form class="signup" id="signup" novalidate>
    <div class="form-row">
      <div class="field"><label for="f-name">Ime i prezime</label><input id="f-name" name="ime" autocomplete="name" required></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="form-row">
      <div class="field"><label for="f-birth">Datum rođenja</label><input id="f-birth" name="datum_rodjenja" type="date"></div>
      <div class="field"><label for="f-course">Kurs</label><select id="f-course" name="kurs"><option>Probni čas</option><option>Buđenje muzičkog sluha (početni)</option><option>Pravilna tehnika pevanja (napredni)</option><option>Pevačke tajne profesionalaca</option></select></div>
    </div>
    <fieldset class="field"><legend>Prethodno muzičko iskustvo</legend>{radios("iskustvo", ["Ne", "Da"])}</fieldset>
    <div class="field"><label for="f-genre">Koji žanr te najviše zanima?</label><input id="f-genre" name="zanr" placeholder="npr. pop, narodna, rock, etno"></div>
    <fieldset class="field"><legend>24/7 Online Singing Support</legend>{radios("podrska", ["Da", "Ne"])}</fieldset>
    <fieldset class="field"><legend>Za časove sam saznao/la preko</legend>{radios("izvor", ["Preporuke", "Sajta", "Reklame", "Facebook-a", "Instagrama", "TikTok-a"])}</fieldset>
    <label class="consent"><input type="checkbox" id="f-consent"> <span>Saglasan/na sam sa <a href="privatnost.html">Politikom privatnosti</a> i <a href="uslovi.html">Uslovima korišćenja</a> i sa tim da se moji podaci čuvaju i koriste za internet marketing.</span></label>
    <button class="btn btn-primary" type="submit">Pošalji prijavu</button>
    <p class="form-msg" id="form-msg" aria-live="polite"></p>
  </form>
</div></section>'''
page("prijava.html", "Prijava", "Prijava za online časove pevanja kod MA Sanje Trifunović Gerginov.", signup)

# ---------- VEŽBAONICA ----------
opts = "".join(f'<option value="{m}"{" selected" if m == 60 else ""}>{n}</option>' for m, n in [(48, "C3 · niži muški"), (53, "F3"), (55, "G3"), (57, "A3"), (60, "C4 · srednji"), (62, "D4"), (65, "F4 · viši ženski"), (67, "G4")])
practice = '''<section class="dark" style="padding-top:clamp(40px,6vw,80px)"><div class="wrap piano-panel">
  <div class="sec-head" style="margin-bottom:6px"><span class="eyebrow">Vežbaonica</span>
    <h1 style="font-size:clamp(2.4rem,6vw,4.4rem);font-weight:800;letter-spacing:-.04em">Zagrej glas uz klavir.</h1>
    <p class="lead">Izaberi vežbu i početni ton, pa pritisni Pokreni. Pevaj slogove dok klavir svira. Posle svakog kruga vežba se podiže za pola stepena. Dirke možeš i sam da sviraš.</p></div>
  <div class="exercises">
    <button class="ex" type="button" data-ex="lestvica" aria-pressed="true"><b>Lestvica do kvinte</b><span>do · re · mi · fa · sol · fa · mi · re · do</span></button>
    <button class="ex" type="button" data-ex="trozvuk" aria-pressed="false"><b>Razloženi akord</b><span>ma · ma · ma · ma (do · mi · sol · do)</span></button>
    <button class="ex" type="button" data-ex="vokali" aria-pressed="false"><b>Vokali na jednom tonu</b><span>mi · me · ma · mo · mu</span></button>
  </div>
  <div class="piano-scroll"><div class="piano" id="piano" aria-label="Klavijatura od C3 do C6"></div></div>
  <div class="controls">
    <button class="btn btn-rose" id="play" type="button">▶ Pokreni</button>
    <button class="btn btn-ghost" id="stop" type="button">■ Stani</button>
    <label class="ctrl" for="start">Početni ton <select id="start">''' + opts + '''</select></label>
    <label class="ctrl" for="tempo">Tempo <input id="tempo" type="range" min="60" max="160" value="110"></label>
  </div>
  <p class="solf" id="solf" aria-live="polite"></p>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Pre nego što počneš</span><h2>Tri pravila za zdravo zagrevanje.</h2></div>
  <div class="grid-3">
    <div class="card"><span class="tagline">disanje</span><h3>Vazduh je gorivo</h3><p>Udahni mirno i duboko pre svake fraze. Bez vazduha nema pevanja.</p><a class="textlink" href="clanak.html" style="justify-self:start">Pravilno disanje</a></div>
    <div class="card"><span class="tagline">držanje</span><h3>Opušteno telo</h3><p>Stani prirodno, ramena dole, vrat slobodan. Napet mišić znači napet ton.</p><a class="textlink" href="clanak.html" style="justify-self:start">Držanje tela</a></div>
    <div class="card"><span class="tagline">mera</span><h3>Bez forsiranja</h3><p>Kad ton postane težak, stani i vrati se na početni ton. Visina dolazi sa vežbom.</p></div>
  </div>
  <p class="ph-note" style="margin-top:28px">ŠABLON: Sanja proverava vežbe i savete; po želji dodajemo nove vežbe (npr. sirena, staccato, intervali).</p>
</div></section>''' + CTA
page("vezbaonica.html", "Vežbaonica", "Interaktivna klavijatura sa vežbama za zagrevanje glasa.", practice)

# ---------- PEVAČKI SAVETI ----------
cats = ["Disanje", "Tehnika", "Glas", "Nastup", "Učenje"]
blog = page_hero("Pevački saveti", "Saveti za pevače, od daha do scene.", "Kratki tekstovi o disanju, tehnici, glasu i tremi, da vežbaš pametnije između časova.") + '''
<section><div class="wrap">
  <div class="filters" role="group" aria-label="Kategorije"><button class="filter" type="button" data-cat="sve" aria-pressed="true">Sve</button>''' + "".join(f'<button class="filter" type="button" data-cat="{c}" aria-pressed="false">{c}</button>' for c in cats) + '''</div>
  <div class="posts">''' + "".join(pc(p) for p in POSTS) + '''</div>
</div></section>''' + CTA
page("saveti.html", "Pevački saveti", "Saveti o disanju, tehnici pevanja, glasu i tremi od MA Sanje Trifunović Gerginov.", blog)

# ---------- ČLANAK (šablon) ----------
article = f'''<section><div class="wrap"><article class="article">
  <a class="textlink" href="saveti.html" style="justify-self:start">← Pevački saveti</a>
  <span class="eyebrow">Učenje</span>
  <h1 style="font-size:clamp(2.2rem,5vw,3.6rem);font-weight:800;letter-spacing:-.035em">Koliko je časova potrebno da naučim da pevam?</h1>
  <p class="meta">{TEACHER} · 18. 9. 2022.</p>
  <p class="ph-note">ŠABLON STRANICE ZA ČLANAK: ovde ide pun Sanjin tekst sa starog sajta. Ispod je samo kratak pregled njenih glavnih tačaka.</p>
  <p>Koliko brzo će učenik napredovati na časovima pevanja zavisi, zapravo, od nekoliko faktora.</p>
  <h2>1. Znanje i metod profesora</h2><p>Jasno objašnjenje i dobar metod skraćuju put do rezultata.</p>
  <h2>2. Sluh i osećaj za ritam</h2><p>Početnicima kojima je teško da čuju i ponove ton treba više vremena, ali se sluh razvija redovnim radom.</p>
  <h2>3. Koliko vežbaš</h2><p>Najvažniji faktor. Preporuka je oko 30 minuta dnevno, a u gužvi bar 10 do 15 minuta.</p>
  <blockquote>Ne pravi pauzu u vežbanju dužu od 24 sata.</blockquote>
  <h2>4. Koliko često imaš časove</h2><p>Dva časa nedeljno, uz podršku između časova, daju najbrži napredak.</p>
  <div class="btn-row" style="margin-top:12px"><a class="btn btn-rose" href="prijava.html">Prijavi se</a><a class="btn btn-ghost" href="vezbaonica.html">Vežbaj odmah</a></div>
</article></div></section>'''
page("clanak.html", "Koliko je časova potrebno da naučim da pevam?", "Od čega zavisi napredak na časovima pevanja.", article)

# ---------- UTISCI ----------
reviews = page_hero("Utisci", "Učenici iz šest zemalja.", "Srbija, Austrija, Nemačka, Švajcarska, Bosna i Hercegovina. Evo šta kažu oni koji već pevaju sa Sanjom.") + '''
<section><div class="wrap">
  <div class="quotes masonry">''' + "".join(tq(t) for t in TESTIMONIALS) + '''</div>
  <p class="ph-note" style="margin-top:12px">ŠABLON: utisci su skraćeni; pune tekstove prenosimo sa starog sajta. Uz dozvolu učenika mogu se dodati i fotografije ili kratki video snimci.</p>
</div></section>''' + CTA
page("utisci.html", "Utisci", "Utisci učenika online časova pevanja sa Sanjom.", reviews)

# ---------- PRAVNE STRANICE ----------
for fn, t in [("privatnost.html", "Politika privatnosti"), ("uslovi.html", "Uslovi korišćenja")]:
    body = page_hero("Pravne informacije", t, "Poslednja izmena: [datum]") + f'''
<section><div class="wrap"><div class="article"><p class="ph-note">ŠABLON: ovde ide tekst „{t}“ sa postojećeg sajta, preuzet u celosti.</p></div></div></section>'''
    page(fn, t, f"{t} — {SITE}.", body)

print("ok")
