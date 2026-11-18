#!/usr/bin/env python3
"""Génère les pages statiques du site Rasso dans ../site (python3 build.py). Modifier DOMAINE puis relancer."""
import json
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent
import os
DOMAINE = os.environ.get("RASSO_DOMAINE", "https://rasso.example").rstrip("/")
APERCU = os.environ.get("RASSO_APERCU") == "1"   # version de démonstration : non indexée par les moteurs
STORE = "https://apps.apple.com/fr/app/rasso/id6758964694"
PIN = '<svg class="pin" viewBox="0 0 100 130" aria-hidden="true"><path d="M50,126 C50,126 8,78 8,48 A42,42 0 1 1 92,48 C92,78 50,126 50,126 Z"/><circle cx="50" cy="48" r="17"/></svg>'
ARROW = '<svg class="arr" viewBox="0 0 40 24" aria-hidden="true"><path d="M2 12 H36 M26 3 L36 12 L26 21"/></svg>'
STOPS = [("index.html", "Départ"), ("rassemblements.html", "Rassemblements"), ("garage.html", "Garage"), ("communaute.html", "Communauté"),
         ("convois.html", "Convois"), ("progression.html", "Progression"), ("questions.html", "Questions")]
def plate(t): return f'<p class="plate"><i aria-hidden="true">F</i><span>{t}</span></p>'
SOON = '<span class="soon" role="note"><i aria-hidden="true"></i>Bientôt sur Android</span>'
def cta(cls="btn-lime", txt="Télécharger sur l'App Store"): return f'<span class="dl"><a class="btn {cls} btn-lg" href="{STORE}" rel="noopener">{txt}</a>{SOON}</span>'
def ticks(*li): return '<ul class="ticks">' + "".join(f"<li>{x}</li>" for x in li) + "</ul>"

import hashlib
def _v():
    h = hashlib.sha1()
    for f in ("css/site.css", "js/site.js", "js/anim.js"):
        try: h.update((OUT / f).read_bytes())
        except FileNotFoundError: pass
    return h.hexdigest()[:8]
V = _v()
def head(fn, title, desc, extra=""):
    url = DOMAINE + "/" + ("" if fn == "index.html" else fn)
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{"noindex, nofollow" if APERCU else "index, follow, max-image-preview:large"}">
<meta name="theme-color" content="#0F0F12">
<meta name="color-scheme" content="dark">
<meta name="apple-itunes-app" content="app-id=6758964694">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Rasso">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAINE}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="fonts/archivo-italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css?v={V}">
{extra}</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
'''
def header(fn):
    li = "".join(f'<li><a href="{f}"{" aria-current=\"page\"" if f == fn else ""}><i aria-hidden="true"></i><span>{l}</span></a></li>' for f, l in STOPS)
    return f'''<div class="announce" role="note"><div class="wrap announce-in"><i aria-hidden="true"></i><p><b>Rasso arrive bientôt sur Android.</b> <span>En attendant, l'application est disponible sur iPhone.</span></p></div></div>
<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="index.html" aria-label="Rasso, accueil">{PIN}<span>RASSO</span></a>
    <nav class="route-nav" id="nav" aria-label="Navigation principale"><ol>{li}</ol></nav>
    <a class="btn btn-lime top-cta" href="{STORE}" rel="noopener">Télécharger</a>
    <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="nav"><span class="sr">Menu</span><i></i><i></i><i></i></button>
  </div>
</header>
<main id="contenu">
'''
def nxt(fn):
    i = [f for f, _ in STOPS].index(fn) if fn in dict(STOPS) else -1
    if i < 0: return ""
    if i == len(STOPS) - 1:
        return f'<section class="next"><div class="wrap next-in"><p>Arrivée</p><a href="{STORE}" rel="noopener"><span>Télécharger Rasso</span>{ARROW}</a>{SOON}</div></section>'
    f, l = STOPS[i + 1]
    return f'<section class="next"><div class="wrap next-in"><p>Étape suivante · {i + 1} sur {len(STOPS) - 1}</p><a href="{f}"><span>{l}</span>{ARROW}</a></div></section>'
def footer(fn):
    app = "".join(f'<a href="{f}">{l}</a>' for f, l in STOPS[1:6])
    return f'''{nxt(fn)}
</main>
<footer class="foot dark">
  <div class="wrap foot-in">
    <div><a class="brand" href="index.html" aria-label="Rasso, accueil">{PIN}<span>RASSO</span></a><p class="foot-tag">Tous les chemins y mènent.</p>{cta("btn-lime", "Télécharger sur l'App Store").replace("btn-lg", "")}</div>
    <nav aria-label="Application"><h3>L'application</h3>{app}</nav>
    <nav aria-label="Informations"><h3>Informations</h3><a href="questions.html">Questions fréquentes</a><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Confidentialité</a><a href="{STORE}" rel="noopener">Rasso sur l'App Store</a></nav>
  </div>
  <div class="wrap foot-end"><p>© 2026 Rasso. App Store est une marque d'Apple Inc.</p></div>
</footer>
<script src="js/vendor/gsap.min.js" defer></script>
<script src="js/vendor/ScrollTrigger.min.js" defer></script>
<script src="js/vendor/MotionPathPlugin.min.js" defer></script>
<script src="js/site.js?v={V}" defer></script>
<script src="js/anim.js?v={V}" defer></script>
</body>
</html>
'''
def page(fn, title, desc, body, extra=""):
    (OUT / fn).write_text(head(fn, title, desc, extra) + header(fn) + body + footer(fn), encoding="utf-8")
def img(src, w, h, alt, lazy=True, cls=""):
    try:
        from PIL import Image
        w, h = Image.open(OUT / "img" / src).size
    except Exception:
        pass
    return f'<img src="img/{src}" width="{w}" height="{h}" alt="{alt}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""}{f" class=\"{cls}\"" if cls else ""}>'
ROAD = '<svg class="road" viewBox="0 0 1440 900" preserveAspectRatio="none" aria-hidden="true"><path d="M-40,760 C 320,700 380,420 720,400 C 1040,380 1100,160 1480,90"/><path d="M-40,880 C 420,860 640,640 900,600 C 1160,560 1280,420 1480,400"/></svg>'

# ============ ACCUEIL ============
CH = [(0, "L'accroche"), (2.9, "La carte"), (5.7, "Le garage"), (9.5, "Le swipe"), (13.5, "La messagerie"), (17, "Le convoi"), (21.5, "L'XP")]
home = f'''<section class="hero dark">{ROAD}
  <div class="wrap hero-in">
    <div class="hero-txt">
      {plate("Auto · Moto")}
      <h1>Tous les chemins<br>mènent à <mark>Rasso.</mark></h1>
      <p class="lead">Trouve les rassemblements près de toi, montre ton garage, rencontre d'autres passionnés et partez rouler en convoi. Tout Rasso tient dans une seule application.</p>
      <div class="cta-row">{cta()}<a class="btn btn-ghost btn-lg" href="#video">Voir la vidéo de 30 s</a></div>
    </div>
    <div class="hero-stage">
      <div class="phone">{img("ecran-carte.webp", 720, 1559, "Écran Explorer de Rasso : carte de France avec les rassemblements regroupés par région", lazy=False)}</div>
      <a class="fl fl-ev" href="rassemblements.html">{img("rassemblement.webp", 1800, 1013, "Rassemblement sur un parking en toiture", lazy=False)}<span><b>Rasso du Lac</b>Dimanche · 10:00</span></a>
      <a class="fl fl-car" href="garage.html">{img("voiture-compacte.webp", 479, 640, "Compacte sportive bleue", lazy=False)}<span><b>Garage de Léo</b>Ajouter en ami</span></a>
      <div class="fl fl-xp" aria-hidden="true"><b>XP</b><i><u></u></i></div>
    </div>
  </div>
  <div class="wrap"><ul class="hero-facts"><li><b>Auto et moto</b>Une seule communauté</li><li><b>Carte</b>France, Luxembourg, d'autres pays bientôt</li><li><b>Convois</b>Virages, autoroute ou équilibré</li><li><b>Application</b>Disponible sur iOS, en développement sur Android</li></ul></div>
</section>

<section class="bento-s paper">
  <div class="wrap">
    <div class="sec-h">{plate("L'itinéraire")}<h2 class="h2">Cinq étapes pour faire le tour de Rasso</h2></div>
    <div class="bento">
      <a class="tile t-rasso" href="rassemblements.html">{img("rassemblement.webp", 1100, 618, "")}<div class="tile-b"><span class="num">1</span><h3>Rassemblements</h3><p>La carte de France des rassos, tes filtres, tes favoris, et un bouton pour créer le tien.</p>{ARROW}</div></a>
      <a class="tile t-garage" href="garage.html">{img("garage-principal.webp", 2000, 1124, "")}<div class="tile-b"><span class="num">2</span><h3>Garage</h3><p>Tes véhicules, tes photos, tes vidéos.</p>{ARROW}</div></a>
      <a class="tile t-commu" href="communaute.html"><div class="mini-deck" aria-hidden="true">{img("voiture-coupe.webp", 415, 739, "")}{img("voiture-compacte.webp", 479, 640, "")}</div><div class="tile-b"><span class="num">3</span><h3>Communauté</h3><p>Swipe les garages, ajoute des amis, discutez.</p>{ARROW}</div></a>
      <a class="tile t-convoi" href="convois.html"><svg viewBox="0 0 600 300" aria-hidden="true"><path d="M40,250 C 220,270 20,130 220,130 C 420,130 180,40 360,40 C 470,40 480,60 560,60"/><circle cx="40" cy="250" r="16"/><circle cx="560" cy="60" r="16"/></svg><div class="tile-b"><span class="num">4</span><h3>Convois</h3><p>Un départ, une destination, ton type de trajet.</p>{ARROW}</div></a>
      <a class="tile t-xp" href="progression.html"><div class="tile-b"><span class="num">5</span><h3>Progression</h3><p>De l'XP, des niveaux, un rôle et des avis sur ton profil.</p>{ARROW}</div><div class="mini-xp" aria-hidden="true"><i><u></u></i><b>Niveau supérieur</b></div></a>
    </div>
  </div>
</section>

<section class="video-s dark" id="video">
  <div class="wrap video-in">
    <div class="video-box"><video id="film" controls preload="none" playsinline poster="img/video-poster.webp" width="720" height="1280"><source src="video/rasso-30s.mp4" type="video/mp4"><track kind="captions" src="video/rasso-30s.fr.vtt" srclang="fr" label="Français" default></video></div>
    <div class="video-txt">
      {plate("30 secondes")}
      <h2 class="h2">Rasso en vidéo</h2>
      <p>De la carte au convoi, le tour de l'application en une demi-minute. Choisis un chapitre pour y aller directement.</p>
      <ol class="chap">{"".join(f'<li><button type="button" data-t="{t}"><span>{int(t)//60}:{int(t)%60:02d}</span>{l}</button></li>' for t, l in CH)}</ol>
    </div>
  </div>
</section>

<section class="charte paper">
  <div class="wrap charte-in">
    <div>{plate("Bon sens")}<h2 class="h2">La passion, pas la prise de risque</h2></div>
    <div class="charte-g"><p><b>On respecte la route.</b>Rasso sert à se retrouver, pas à rouler vite. Le code de la route s'applique à chaque sortie.</p><p><b>On respecte les lieux.</b>Les parkings, les riverains et les organisateurs nous accueillent : on repart en laissant l'endroit propre et calme.</p><p><b>On pose le téléphone.</b>Le trajet se prépare à l'arrêt. En roulant, les mains restent sur le volant ou le guidon.</p></div>
  </div>
</section>
'''
ld = {"@context": "https://schema.org", "@graph": [
 {"@type": "Organization", "@id": DOMAINE + "/#org", "name": "Rasso", "url": DOMAINE + "/", "logo": DOMAINE + "/favicon.svg"},
 {"@type": "WebSite", "@id": DOMAINE + "/#site", "url": DOMAINE + "/", "name": "Rasso", "inLanguage": "fr-FR", "publisher": {"@id": DOMAINE + "/#org"}},
 {"@type": "MobileApplication", "name": "Rasso", "operatingSystem": "iOS", "applicationCategory": "SocialNetworkingApplication", "inLanguage": "fr-FR",
  "description": "Application communautaire auto et moto : carte des rassemblements, garage, découverte et amis, messagerie, convois et progression.", "installUrl": STORE, "downloadUrl": STORE, "publisher": {"@id": DOMAINE + "/#org"}}]}
page("index.html", "Rasso – L'application des rassemblements auto et moto",
     "Rasso réunit les passionnés auto et moto : carte des rassemblements en France, garage à partager, découverte et amis, messagerie, convois et progression. Sur l'App Store.",
     home, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')

# ============ RASSEMBLEMENTS ============
rows = [("Rasso du Lac", "Dimanche · 10:00", "Auto · Moto"), ("Youngtimers & Café", "Dimanche · 9:00", "Auto"), ("Sortie des Crêtes", "Samedi · 14:00", "Moto")]
page("rassemblements.html", "Rassemblements auto et moto près de chez toi – Rasso",
     "Explore la carte de France des rassemblements auto et moto, filtre par département, garde tes favoris et crée ton propre rasso avec l'application Rasso.",
f'''<section class="phero dark">{ROAD}
  <div class="wrap phero-in">
    <div class="phero-txt">{plate("Étape 1 · Explorer")}<h1>Trouve ton<br>prochain <mark>rasso.</mark></h1><p class="lead">Un rasso, c'est un rassemblement de passionnés : une rencontre sur un parking, une sortie, un salon, une journée circuit. Rasso les réunit sur une seule carte.</p>{cta()}</div>
    <div class="phero-vis"><div class="phone">{img("ecran-carte.webp", 720, 1559, "Carte de France de l'écran Explorer, avec les rassemblements regroupés par secteur", lazy=False)}</div></div>
  </div>
</section>
<section class="tri paper">
  <div class="wrap">
    <div class="sec-h">{plate("Chercher")}<h2 class="h2">Trois façons de tomber sur le bon</h2></div>
    <div class="tri-g">
      <article class="tcard"><div class="tcard-v v-map">{img("carte-france.webp", 760, 755, "La carte de France avec des marqueurs de rassemblements")}</div><h3>Par la carte</h3><p>Les rassemblements sont regroupés par secteur. Tu zoomes sur ta région, tu touches un marqueur, tu ouvres la fiche.</p></article>
      <article class="tcard"><div class="tcard-v v-list"><div class="pills" aria-hidden="true"><span class="pill on">Mon département</span><span class="pill">France</span><span class="pill">Tout</span></div>{"".join(f'<div class="rw"><b>{a}</b><span>{b}</span><em>{c}</em></div>' for a, b, c in rows)}</div><h3>Par la liste</h3><p>Trois filtres : ton département, la France entière, ou tout afficher. Chaque ligne donne le lieu, la date et le type de véhicules.</p></article>
      <article class="tcard"><div class="tcard-v v-search"><div class="field" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 L21 21"/></svg><span>Département ou code…</span></div><div class="sug" aria-hidden="true"><span>Rhône</span><span>69</span><span>Haute-Savoie</span><span>74</span><span>Gironde</span><span>33</span></div></div><h3>Par le département</h3><p>Tu pars en week-end ? Tape le nom ou le code du département et regarde ce qui s'y organise.</p></article>
    </div>
    <p class="note">Les rassemblements affichés sur cette page sont des exemples.</p>
  </div>
</section>
<section class="orga dark">
  <div class="orga-photo">{img("rassemblement-2.webp", 1800, 1200, "Sportives alignées sur un parking pendant un rassemblement, des passionnés autour")}</div>
  <div class="wrap orga-in">
    <div class="orga-card">
      {plate("Organiser")}
      <h2 class="h2">Le tien, quand tu veux</h2>
      <p>Tu connais un bon spot et tu veux y réunir du monde ? Publie ton rassemblement, il apparaît sur la carte.</p>
      <ol class="steps"><li><b>Créer</b>Un bouton, une fiche : le lieu, la date, auto ou moto.</li><li><b>Gérer mes Rassos</b>Tous ceux que tu organises, au même endroit.</li><li><b>Rassos favoris</b>Ceux que tu ne veux pas rater restent sous la main.</li></ol>
    </div>
  </div>
</section>
''')

# ============ GARAGE ============
page("garage.html", "Ton garage en ligne : voitures, motos, photos et vidéos – Rasso",
     "Présente tes voitures et tes motos dans ton garage Rasso : fiche par véhicule, photos, vidéos, description, véhicules aimés et classement des marques.",
f'''<section class="ghero dark">
  <div class="ghero-photo">{img("garage-principal.webp", 2000, 1124, "Compacte sportive noire, jantes grises et étriers rouges, garée en bord de route", lazy=False)}</div>
  <div class="wrap ghero-in">{plate("Étape 2 · Garage")}<h1>Ton garage,<br>ta <mark>fierté.</mark></h1><p class="lead">Chaque véhicule a sa fiche. Tu y mets ce qui le rend unique, et la communauté le découvre.</p>{cta()}</div>
</section>
<section class="fiche paper">
  <div class="wrap fiche-in">
    <div class="gal">
      <figure class="g1">{img("garage-principal.webp", 2000, 1124, "Vue trois quarts avant de la compacte sportive")}<figcaption>Photo principale</figcaption></figure>
      <figure class="g2">{img("detail-interieur.webp", 360, 240, "Volant et tableau de bord")}<figcaption>Intérieur</figcaption></figure>
      <figure class="g3">{img("detail-moteur.webp", 360, 202, "Moteur quatre cylindres, capot ouvert")}<figcaption>Moteur</figcaption></figure>
      <figure class="g4">{img("detail-jante.webp", 360, 539, "Jante grise et étrier de frein rouge")}<figcaption>Jantes</figcaption></figure>
      <figure class="g5">{img("garage-video.webp", 600, 500, "Coupé noir filmé de nuit, feux arrière allumés")}<figcaption><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4 L20 12 L7 20Z"/></svg>Vidéo</figcaption></figure>
    </div>
    <div class="fiche-txt">
      {plate("La fiche véhicule")}
      <h2 class="h2">Tout ce qu'on veut savoir sur ta machine</h2>
      <dl class="spec"><div><dt>Nom</dt><dd>Celui que tu lui donnes</dd></div><div><dt>Modèle</dt><dd>Marque, série, génération</dd></div><div><dt>Année</dt><dd>Celle de ta carte grise</dd></div><div><dt>Photos</dt><dd>Extérieur, intérieur, détails</dd></div><div><dt>Vidéos</dt><dd>Le son, le roulage, la prépa</dd></div><div><dt>Description</dt><dd>Son histoire, en quelques lignes</dd></div></dl>
    </div>
  </div>
</section>
<section class="duo dark">
  <div class="wrap duo-in">
    <article class="duo-a">{plate("Coups de cœur")}<h2 class="h2">Véhicules aimés</h2><p>Une voiture ou une moto te plaît ? Un like, et elle rejoint ta liste. Tu la retrouves à côté de tes rassos favoris.</p><div class="liked">{img("moto-profil.webp", 1200, 800, "Café racer noir, vu de profil")}{img("voiture-youngtimer.webp", 1200, 800, "Youngtimer blanche sur un parking, de nuit")}{img("voiture-compacte.webp", 479, 640, "Compacte sportive bleue")}</div></article>
    <article class="duo-b">{plate("Classement")}<h2 class="h2">Les marques les plus présentes</h2><p>Le classement compte les véhicules de chaque marque dans les garages de la communauté. À toi de faire monter la tienne.</p><div class="podium" aria-hidden="true"><i class="p2"><b>2</b></i><i class="p1"><b>1</b></i><i class="p3"><b>3</b></i></div></article>
  </div>
</section>
''')

# ============ COMMUNAUTÉ ============
deck = [("voiture-compacte.webp", 479, 640, "profil-leo.webp", "Léo"), ("voiture-coupe.webp", 415, 739, "profil-sam.webp", "Sam"), ("moto-cafe-racer.webp", 900, 879, "profil-moi.webp", "Inès"), ("voiture-youngtimer.webp", 1200, 800, "profil-sam.webp", "Malo")]
cards = "".join(f'<div class="sw" data-nom="{n}">{img(p, w, h, "")}<span class="stamp s-pass">Passer</span><span class="stamp s-add">Ajouter en ami</span><div class="own">{img(a, 160, 160, "")}<b>Garage de {n}</b></div></div>' for p, w, h, a, n in reversed(deck))
roles = [("Visiteur", "Tu viens voir, rencontrer et profiter des rassemblements autour de chez toi."), ("Exposant", "Tu viens avec ton véhicule et tu le présentes à la communauté."), ("Organisateur", "Tu crées des rassemblements et tu fais venir du monde."), ("Mécanicien", "Tu as les mains dans le cambouis et tu le fais savoir.")]
page("communaute.html", "Rencontre des passionnés auto et moto : swipe, amis, messagerie – Rasso",
     "Découvre les garages des autres membres, swipe pour ajouter des amis, discute en messagerie, retrouve vos croisements sur la carte et partage des stories sur Rasso.",
f'''<section class="phero dark">{ROAD}
  <div class="wrap phero-in">
    <div class="phero-txt">{plate("Étape 3 · Découverte")}<h1>Un garage te plaît ?<br><mark>Swipe.</mark></h1><p class="lead">La découverte te présente les garages des autres membres, un par un. À gauche tu passes, à droite tu envoies une demande d'ami au propriétaire.</p><p class="hint">Essaie avec les deux boutons, ou les flèches du clavier.</p></div>
    <div class="phero-vis">
      <div class="swipe" id="swipe"><div class="sw-stack">{cards}</div>
        <div class="sw-btns"><button type="button" class="sb sb-pass" data-dir="left"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="M11 11 L29 29 M29 11 L11 29"/></svg><span>Passer</span></button><button type="button" class="sb sb-add" data-dir="right"><svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="16" cy="14" r="6"/><path d="M5 33 C5 24 27 24 27 33 M31 10 V22 M25 16 H37"/></svg><span>Ajouter en ami</span></button></div>
        <p class="sw-msg" id="swmsg" aria-live="polite">Profils et garages fictifs, pour la démonstration.</p></div>
    </div>
  </div>
</section>
<section class="amis paper">
  <div class="wrap amis-in">
    <div class="amis-txt">{plate("Amis")}<h2 class="h2">Une demande, une réponse, une amitié</h2><p>Swiper à droite n'ajoute personne d'office : ça envoie une demande. L'amitié commence quand l'autre accepte.</p>{ticks("Cherche un membre par son <b>pseudo</b>.", "Parcours les <b>suggestions</b> et ajoute en un geste.", "Filtre les membres par <b>rôle</b> pour trouver les bonnes personnes.")}</div>
    <ol class="flow"><li><span>Swipe à droite</span></li><li><span>Demande d'ami envoyée</span></li><li class="wait"><span>Il ou elle accepte</span></li><li class="ok"><span>Amitié acceptée</span></li></ol>
  </div>
  <div class="wrap"><ul class="role-grid">{"".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in roles)}</ul></div>
</section>
<section class="msg dark">
  <div class="wrap msg-in">
    <div class="ui chat"><div class="stories" aria-hidden="true"><span class="st me">{img("profil-moi.webp", 160, 160, "")}<em>Ma story</em></span><span class="st">{img("profil-leo.webp", 160, 160, "")}<em>Léo</em></span><span class="st">{img("profil-sam.webp", 160, 160, "")}<em>Sam</em></span></div>
      <div class="chat-h">{img("profil-leo.webp", 160, 160, "")}<div><b>Léo</b><span>Ami · en ligne</span></div></div><p class="bub">On se retrouve au rasso ?</p><p class="bub me">On prépare un convoi !</p></div>
    <div class="msg-txt">{plate("Entre deux sorties")}<h2 class="h2">Restez en contact</h2>
      <div class="trio"><div><h3>Messagerie</h3><p>Une fois amis, la conversation continue dans l'application : pour organiser la prochaine sortie ou parler mécanique.</p></div><div><h3>Croisements</h3><p>Tu as croisé un ami sur la route ? Retrouve l'endroit sur la carte.</p></div><div><h3>Stories</h3><p>Partage un moment de ta journée. Tes amis peuvent y réagir.</p></div></div>
      <div class="cross"><svg viewBox="0 0 400 150" aria-hidden="true"><g class="grid"><path d="M-10,30 L410,5 M-10,90 L410,65 M-10,150 L410,125 M60,-10 L85,160 M180,-10 L205,160 M300,-10 L325,160"/></g><path class="t1" d="M10,135 C 110,120 150,95 200,75 C 250,55 310,30 395,15"/><path class="t2" d="M20,20 C 90,40 150,58 200,75 C 260,95 320,118 390,136"/><circle cx="200" cy="75" r="9"/></svg><span class="cross-l">Ami croisé ici</span></div>
    </div>
  </div>
</section>
''')

# ============ CONVOIS ============
page("convois.html", "Convois auto et moto : balade en groupe et choix du trajet – Rasso",
     "Crée un convoi ou rejoins-en un près de toi : point de rendez-vous, départ, destination et type de trajet au choix (virages, autoroute ou équilibré) avec Rasso.",
f'''<section class="chero dark">
  <div class="wrap chero-in">
    <div class="phero-txt">{plate("Étape 4 · Convois")}<h1>Un départ.<br>Une destination.<br><mark>Votre convoi.</mark></h1><p class="lead">Le convoi, c'est la balade en groupe : un point de rendez-vous, un itinéraire commun, et tout le monde part ensemble.</p></div>
    <div class="ui route">
      <svg viewBox="0 0 830 560" role="img" aria-label="Schéma d'un trajet entre un point A et un point B"><g class="grid"><path d="M-20,90 L850,20 M-20,230 L850,160 M-20,370 L850,300 M-20,510 L850,440 M110,-20 L170,580 M330,-20 L390,580 M550,-20 L610,580 M770,-20 L830,580"/></g><path id="trajet" class="trajet" d="M130,450 C 380,480 60,290 340,285 C 620,280 260,130 500,135 C 630,138 600,100 690,100"/><g class="pt"><circle cx="130" cy="450" r="30"/><text x="130" y="463">A</text></g><g class="pt b"><circle cx="690" cy="100" r="30"/><text x="690" y="113">B</text></g></svg>
      <div class="chips" role="group" aria-label="Type de trajet"><button type="button" class="chip" data-trajet="v" aria-pressed="true">Virages</button><button type="button" class="chip" data-trajet="a" aria-pressed="false">Autoroute</button><button type="button" class="chip" data-trajet="e" aria-pressed="false">Équilibré</button></div>
      <p class="ui-note" id="trajet-txt" aria-live="polite">Virages : la route qui tourne, pour le plaisir de conduire.</p>
    </div>
  </div>
</section>
<section class="road-s paper">
  <div class="wrap road-in">
    <div class="sec-h">{plate("Feuille de route")}<h2 class="h2">De l'idée au départ</h2><p>Tu peux lancer ton propre convoi ou en rejoindre un près de toi.</p></div>
    <ol class="roadmap"><li><b>Le rendez-vous</b><p>Un lieu et une heure pour se retrouver avant de partir.</p></li><li><b>Le départ et la destination</b><p>Tu poses le point A et le point B.</p></li><li><b>Le type de trajet</b><p>Virages, autoroute ou équilibré : le tracé s'adapte à ce que le groupe a envie de rouler.</p></li><li><b>Le convoi</b><p>Tes amis rejoignent, et vous partez ensemble.</p></li></ol>
  </div>
</section>
<section class="charte dark">
  <div class="wrap charte-in">
    <div>{plate("Bon sens")}<h2 class="h2">Rouler ensemble, rouler propre</h2></div>
    <div class="charte-g"><p><b>Pas de course.</b>Un convoi n'est pas une épreuve de vitesse. On roule au rythme du groupe et dans les limites.</p><p><b>Des distances.</b>On garde ses distances de sécurité, on ne force aucun dépassement pour rester groupés.</p><p><b>Le téléphone à l'arrêt.</b>Le trajet se choisit avant de partir, pas en roulant.</p></div>
  </div>
</section>
''')

# ============ PROGRESSION ============
page("progression.html", "XP, niveaux, rôle et avis : ton profil de passionné – Rasso",
     "Sur Rasso, tu gagnes de l'expérience en likant et en créant des rassemblements, tu montes de niveau, tu affiches ton rôle et tu reçois des avis sur ton profil.",
f'''<section class="phero dark">{ROAD}
  <div class="wrap phero-in">
    <div class="phero-txt">{plate("Étape 5 · Progression")}<h1>Participe.<br>Gagne de <mark>l'XP.</mark></h1><p class="lead">Plus tu fais vivre la communauté, plus ton profil progresse. Ton niveau s'affiche à côté de ton pseudo.</p><p class="hint">Essaie : chaque action remplit la barre.</p></div>
    <div class="phero-vis">
      <div class="ui xp" id="xp">
        <button type="button" class="xrow" data-xp="34"><svg viewBox="0 0 100 100" aria-hidden="true"><path d="M50 6 L62 37 L95 39 L69 60 L78 93 L50 74 L22 93 L31 60 L5 39 L38 37 Z"/></svg><b>Liker un rasso</b><span>+ XP</span></button>
        <button type="button" class="xrow" data-xp="50"><svg viewBox="0 0 100 100" aria-hidden="true" class="plus"><path d="M50 18 V82 M18 50 H82"/></svg><b>Créer un rasso</b><span>+ XP</span></button>
        <div class="xbar"><span>XP</span><i><b id="xfill"></b></i></div>
        <div class="lvl" id="lvl" aria-live="polite">Continue…</div>
        <p class="ui-note">Démonstration : les gains réels dépendent de l'application.</p>
      </div>
    </div>
  </div>
</section>
<section class="profil paper">
  <div class="wrap profil-in">
    <div class="pcard">
      <div class="pcard-top">{img("moto-cafe-racer.webp", 900, 879, "")}<div class="pid">{img("profil-moi.webp", 160, 160, "")}<div><b>Inès</b><span class="niv">Niv. 3</span></div></div></div>
      <div class="pcard-b"><span class="role">Exposant</span><div class="stars" role="img" aria-label="Avis des membres : cinq étoiles"><i></i><i></i><i></i><i></i><i></i></div><dl><div><dt>Garage</dt><dd>2</dd></div><div><dt>Rassos</dt><dd>4</dd></div></dl></div>
      <p class="ui-note">Profil fictif</p>
    </div>
    <div class="profil-txt">{plate("Ton profil")}<h2 class="h2">Une carte de visite de passionné</h2>
      <div class="trio"><div><h3>Niveau</h3><p>Il monte avec ton XP et s'affiche à côté de ton pseudo.</p></div><div><h3>Rôle</h3><p>Visiteur, exposant, organisateur ou mécanicien : tu choisis celui qui te ressemble.</p></div><div><h3>Avis</h3><p>Les autres membres peuvent laisser un avis sur ton profil.</p></div></div>
      {ticks("Ton <b>garage</b> et tes <b>rassos</b> sont visibles depuis ton profil.", "Tu peux <b>partager</b> ton profil.")}
    </div>
  </div>
</section>
''')

# ============ QUESTIONS ============
FAQ = [("Les rassemblements", [
 ("C'est quoi, un rasso ?", "Un rasso, c'est un rassemblement de passionnés auto ou moto : une rencontre sur un parking, une sortie, un salon, une journée circuit. Dans l'application, chaque rasso a sa fiche avec le lieu, la date et le type de véhicules."),
 ("Comment trouver un rassemblement près de chez moi ?", "Ouvre Explorer : la carte de France affiche les rassemblements. Tu peux aussi filtrer la liste par ton département, par France entière, ou chercher un département par son nom ou son code."),
 ("Puis-je créer mon propre rassemblement ?", "Oui. Le bouton Créer te permet de publier ton rasso, et l'espace Gérer mes Rassos regroupe ceux que tu organises."),
 ("Rasso, c'est aussi pour les motos ?", "Oui. Rasso s'adresse aux passionnés auto et moto. Chaque rassemblement indique le type de véhicules concerné.")]),
 ("La communauté", [
 ("Comment ajouter un ami ?", "Dans la découverte, swipe à droite sur un garage qui te plaît pour envoyer une demande d'ami à son propriétaire, ou à gauche pour passer. Tu peux aussi chercher quelqu'un par son pseudo. L'amitié est créée quand la demande est acceptée."),
 ("À quoi servent les rôles ?", "Ton rôle (visiteur, exposant, organisateur ou mécanicien) s'affiche sur ton profil. Il aide les autres membres à savoir ce que tu viens chercher, et permet de filtrer les membres."),
 ("Que sont les croisements ?", "Quand tu as croisé un ami, Rasso te permet de retrouver l'endroit sur la carte.")]),
 ("Les convois et la progression", [
 ("Comment fonctionne un convoi ?", "Un convoi est une balade en groupe avec un point de rendez-vous. Tu choisis un départ, une destination et un type de trajet : virages, autoroute ou équilibré. Tu peux aussi rejoindre un convoi près de toi."),
 ("Comment gagner de l'expérience ?", "Tu gagnes de l'XP en participant à la vie de l'application, par exemple en ajoutant un rasso à tes favoris ou en créant le tien. L'XP fait monter ton niveau, affiché sur ton profil."),
 ("Où télécharger Rasso ?", "Rasso est disponible sur l'App Store pour iPhone. La version Android arrive bientôt."),
 ("Rasso est-il disponible sur Android ?", "Pas encore : la version Android arrive bientôt. En attendant, Rasso est disponible sur iPhone, sur l'App Store.")])]
fl = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, qs in FAQ for q, a in qs]}
page("questions.html", "Questions fréquentes sur l'application Rasso",
     "Les réponses aux questions sur Rasso : rassemblements auto et moto, création d'un rasso, amis et swipe, rôles, croisements, convois, expérience et téléchargement.",
f'''<section class="qhero dark"><div class="wrap">{plate("Questions")}<h1>Avant de<br>te <mark>lancer.</mark></h1><p class="lead">Onze réponses courtes pour comprendre Rasso avant de l'installer.</p></div></section>
<section class="faq paper"><div class="wrap faq-g">{"".join(f'<div class="faq-col"><h2 class="h3">{t}</h2>' + "".join(f"<details{' open' if i == 0 and j == 0 else ''}><summary>{q}</summary><p>{a}</p></details>" for j, (q, a) in enumerate(qs)) + "</div>" for i, (t, qs) in enumerate(FAQ))}</div></section>
''', f'<script type="application/ld+json">{json.dumps(fl, ensure_ascii=False)}</script>\n')

# ============ LÉGAL ============
T = lambda s: f'<span class="todo">{s}</span>'
page("mentions-legales.html", "Mentions légales – Rasso", "Mentions légales du site Rasso : éditeur, hébergeur et propriété intellectuelle.",
f'''<section class="legal paper"><div class="wrap"><h1>Mentions légales</h1>
<p>{T("Page à compléter avant mise en ligne : les champs surlignés sont obligatoires.")}</p>
<h2>Éditeur du site</h2><p>{T("Raison sociale ou nom et prénom")}, {T("forme juridique et capital")}, {T("adresse du siège")}.<br>{T("SIREN / RCS")} · {T("n° de TVA intracommunautaire, le cas échéant")}<br>Contact : {T("adresse e-mail")} · {T("téléphone")}</p>
<h2>Directeur de la publication</h2><p>{T("Nom et prénom")}</p>
<h2>Hébergeur</h2><p>{T("Nom de l’hébergeur, adresse, téléphone")}</p>
<h2>Propriété intellectuelle</h2><p>Le nom Rasso, le site, ses textes et ses éléments graphiques sont la propriété de leur éditeur. Toute reproduction sans autorisation est interdite. Les photographies restent la propriété de leurs auteurs. App Store est une marque d’Apple Inc.</p>
<h2>Signaler un contenu</h2><p>Pour signaler un contenu ou exercer un droit, écris à {T("adresse e-mail")}.</p></div></section>''')
page("confidentialite.html", "Confidentialité – Rasso", "Politique de confidentialité du site Rasso : aucun cookie, aucun traceur, aucun formulaire.",
f'''<section class="legal paper"><div class="wrap"><h1>Confidentialité</h1>
<h2>Ce site</h2><p>Ce site est une vitrine statique. Il ne dépose aucun cookie, n’utilise aucun traceur ni outil de mesure d’audience, ne contient aucun formulaire et ne charge aucune ressource depuis un service tiers. Les polices et les images sont servies depuis le site lui-même.</p>
<p>Comme tout serveur web, l’hébergeur peut conserver des journaux techniques (adresse IP, date, page demandée) pour assurer la sécurité du service. {T("Préciser l’hébergeur et la durée de conservation")}</p>
<h2>L’application Rasso</h2><p>{T("À compléter : reprendre la politique de confidentialité de l’application (données de compte, photos et vidéos publiées, localisation et croisements, messagerie, durées de conservation, sous-traitants, base légale).")}</p>
<h2>Tes droits</h2><p>Conformément au RGPD, tu disposes d’un droit d’accès, de rectification, d’effacement, d’opposition, de limitation et de portabilité. Pour l’exercer : {T("adresse e-mail du responsable de traitement")}. Tu peux aussi saisir la CNIL (cnil.fr).</p>
<h2>Responsable de traitement</h2><p>{T("Raison sociale et adresse")}</p></div></section>''')

urls = [f for f, _ in STOPS] + ["mentions-legales.html", "confidentialite.html"]
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f'  <url><loc>{DOMAINE}/{"" if u == "index.html" else u}</loc><lastmod>2026-11-16</lastmod></url>\n' for u in urls) + "</urlset>\n")
(OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n" if APERCU else f"User-agent: *\nAllow: /\n\nSitemap: {DOMAINE}/sitemap.xml\n")
print("pages :", ", ".join(urls))
