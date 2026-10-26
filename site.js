/* Časovi pevanja sa Sanjom — zajednički skript */

/* mobilni meni */
document.querySelectorAll(".menu-btn").forEach(b => b.addEventListener("click", () => {
  const nav = b.closest(".nav"), open = nav.classList.toggle("open");
  b.setAttribute("aria-expanded", open); b.textContent = open ? "Zatvori" : "Meni";
}));

/* godina u podnožju */
document.querySelectorAll("[data-year]").forEach(el => el.textContent = new Date().getFullYear());

/* filter na blogu */
const filters = document.querySelectorAll(".filter");
filters.forEach(f => f.addEventListener("click", () => {
  filters.forEach(x => x.setAttribute("aria-pressed", x === f));
  const c = f.dataset.cat;
  document.querySelectorAll(".post-card").forEach(p => p.hidden = c !== "sve" && p.dataset.cat !== c);
}));

/* forma za prijavu — u šablonu se ne šalje nigde (vidi uputstvo: Formspree / Netlify Forms) */
const form = document.getElementById("signup");
if (form) form.addEventListener("submit", e => {
  e.preventDefault();
  const msg = document.getElementById("form-msg");
  const need = ["f-name", "f-email"].map(id => document.getElementById(id)).filter(i => !i.value.trim());
  if (need.length) { msg.textContent = "Upiši ime i email da bi Sanja mogla da ti pošalje slobodne termine."; need[0].focus(); return; }
  if (!document.getElementById("f-consent").checked) { msg.textContent = "Potrebna je saglasnost sa Politikom privatnosti i Uslovima korišćenja."; return; }
  msg.textContent = "Ovo je šablon: forma još nije povezana sa email-om, pa prijava nije poslata.";
});

/* ===== Vežbaonica: klavir + vežbe ===== */
const piano = document.getElementById("piano");
if (piano) {
  const NAMES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];
  const LOW = 48, HIGH = 84; // C3 – C6
  const keys = {}, whites = [];
  for (let m = LOW; m <= HIGH; m++) {
    const n = NAMES[m % 12]; if (n.includes("#")) continue;
    const k = document.createElement("div"); k.className = "wk"; k.dataset.m = m;
    k.textContent = n === "C" ? n + (Math.floor(m / 12) - 1) : "";
    piano.appendChild(k); keys[m] = k; whites.push(m);
  }
  const wW = 100 / whites.length;
  for (let m = LOW; m <= HIGH; m++) {
    if (!NAMES[m % 12].includes("#")) continue;
    const k = document.createElement("div"); k.className = "bk"; k.dataset.m = m;
    k.style.left = `calc(${(whites.indexOf(m - 1) + 1) * wW}% - ${wW * .3}%)`; k.style.width = `${wW * .6}%`;
    piano.appendChild(k); keys[m] = k;
  }

  /* Zvuk na telefonima: iPhone/Android puštaju zvuk tek posle dodira, a iPhone
     ga po difoltu utišava kad je uključen nečujni režim. Zato zvuk "otključavamo"
     pri prvom dodiru i tražimo režim reprodukcije (kao muzička aplikacija). */
  let ctx;
  function audio() {
    if (!ctx) {
      try { if (navigator.audioSession) navigator.audioSession.type = "playback"; } catch (e) {}
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      const b = ctx.createBuffer(1, 1, 22050), s = ctx.createBufferSource();
      s.buffer = b; s.connect(ctx.destination); s.start(0);
    }
    if (ctx.state !== "running") ctx.resume();
    return ctx;
  }
  ["touchend", "click", "keydown"].forEach(ev => document.addEventListener(ev, audio, { passive: true }));

  function tone(m, dur = .5) {
    audio();
    const f = 440 * Math.pow(2, (m - 69) / 12), t = ctx.currentTime, g = ctx.createGain();
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(.28, t + .01); g.gain.exponentialRampToValueAtTime(.001, t + dur + .6);
    [[1, "triangle", 1], [2, "sine", .25], [3, "sine", .08]].forEach(([h, type, a]) => {
      const o = ctx.createOscillator(), og = ctx.createGain(); o.type = type; o.frequency.value = f * h; og.gain.value = a;
      o.connect(og).connect(g); o.start(t); o.stop(t + dur + .7);
    });
    g.connect(ctx.destination);
    const k = keys[m]; if (k) { k.classList.add("on"); setTimeout(() => k.classList.remove("on"), Math.max(dur * 700, 160)); }
  }
  piano.addEventListener("pointerdown", e => { const m = e.target.dataset.m; if (m) { e.preventDefault(); tone(+m); } });

  /* vežbe: koraci u polustepenima od osnovnog tona + slogovi */
  const EX = {
    lestvica: { steps: [0,2,4,5,7,5,4,2,0], syl: ["do","re","mi","fa","sol","fa","mi","re","do"] },
    trozvuk:  { steps: [0,4,7,12,7,4,0],    syl: ["ma","ma","ma","ma","ma","ma","ma"] },
    vokali:   { steps: [0,0,0,0,0,2,4,2,0], syl: ["mi","me","ma","mo","mu","a","a","a","a"] }
  };
  let current = "lestvica";
  document.querySelectorAll(".ex").forEach(b => b.addEventListener("click", () => {
    document.querySelectorAll(".ex").forEach(x => x.setAttribute("aria-pressed", x === b));
    current = b.dataset.ex; stop(); show();
  }));

  const startSel = document.getElementById("start"), tempo = document.getElementById("tempo"), solf = document.getElementById("solf");
  const nameOf = m => NAMES[m % 12] + (Math.floor(m / 12) - 1);
  let timer = null, root = +startSel.value;
  function markRoot() { Object.values(keys).forEach(k => k.classList.remove("root")); keys[root] && keys[root].classList.add("root"); }
  function show(i = -1) {
    const ex = EX[current];
    solf.innerHTML = ex.syl.map((s, j) => j === i ? `<b>${s}</b>` : s).join(" · ") + ` &nbsp;(${nameOf(root)})`;
    markRoot();
  }
  function stop() { clearTimeout(timer); timer = null; }
  function run() {
    stop(); let i = 0; const ex = EX[current];
    const beat = () => 60000 / +tempo.value;
    const tick = () => {
      if (i < ex.steps.length) {
        const last = i === ex.steps.length - 1;
        tone(root + ex.steps[i], last ? .9 : beat() / 1100);
        show(i); i++;
        timer = setTimeout(tick, last ? beat() * 2.2 : beat());
      } else {
        root++; if (root + Math.max(...ex.steps) > HIGH) root = +startSel.value;
        i = 0; markRoot(); tone(root, .3); timer = setTimeout(tick, beat() * 1.4);
      }
    };
    tick();
  }
  startSel.addEventListener("change", () => { root = +startSel.value; stop(); show(); });
  document.getElementById("play").addEventListener("click", () => { root = +startSel.value; run(); });
  document.getElementById("stop").addEventListener("click", () => { stop(); solf.innerHTML = `Stalo na: <b>${nameOf(root)}</b>`; });
  show();
}
