# Site Rasso — mise en ligne

Site de 9 pages : accueil, rassemblements, garage, communauté, convois, progression, questions, mentions légales, confidentialité.
Les pages sont générées par `source/build.py` (en-tête, pied et navigation communs) : modifier les textes dans ce fichier puis lancer `python3 source/build.py`.

Site statique : aucun serveur applicatif, aucune base de données, aucun cookie, aucun traceur, aucune ressource tierce.

## Avant de publier
1. **Nom de domaine** : changer `DOMAINE` en tête de `source/build.py` puis relancer le script (il met à jour toutes les pages, `robots.txt` et `sitemap.xml`).
2. **Pages légales** : compléter les champs surlignés de `mentions-legales.html` et `confidentialite.html`.
3. **Droits des photos** (`img/`) : vérifier que chaque image peut être publiée.
4. Informations à confirmer dans les textes : annonces de vente (non mentionnées), prix de l'app (non mentionné), Android (non mentionné).

## Hébergement
Déposer le contenu du dossier tel quel chez un hébergeur avec HTTPS (Netlify, Cloudflare Pages, Vercel, OVH…).
- Netlify / Cloudflare Pages : le fichier `_headers` applique les en-têtes de sécurité.
- Apache (OVH, o2switch…) : `.htaccess` force HTTPS et applique les mêmes en-têtes.
- Vérifier ensuite sur securityheaders.com et pagespeed.web.dev, puis déclarer `sitemap.xml` dans Google Search Console.

## Sécurité en place
HTTPS forcé + HSTS, Content-Security-Policy stricte (aucun script ni style en ligne, aucune origine externe), anti-clickjacking, pas de formulaire, polices auto-hébergées.

## Référencement en place
Balises title/description, URL canonique, Open Graph + image de partage (`img/og.jpg`), données structurées (Organisation, Site, Application mobile, FAQ), bannière App Store sur Safari iOS (`apple-itunes-app`), sitemap, robots.txt, HTML sémantique, textes alternatifs, images WebP en chargement différé.

## Modifier
Textes : `source/build.py`. Couleurs et typographie : variables en tête de `css/site.css`. Vidéo : `video/rasso-30s.mp4` (+ sous-titres `.vtt`).

## Photos (mise à jour du 16/11/2026)
Les photos de véhicules, de rassemblements et de détails viennent de Pexels (licence Pexels : usage commercial gratuit, attribution non obligatoire). Page d'origine : `https://www.pexels.com/photo/<identifiant>/`.
| Fichier | Identifiant Pexels | Retouche |
|---|---|---|
| rassemblement.webp | 29865673 | plaque et logo de cigarettier floutés |
| rassemblement-2.webp | 37301080 | plaques floutées |
| garage-principal.webp, detail-jante.webp | 16634773, 16634765 | aucune |
| detail-interieur.webp, detail-moteur.webp | 3076827, 16545849 | aucune |
| voiture-compacte.webp, voiture-coupe.webp, voiture-youngtimer.webp | 33271353, 16626639, 16896047 | recadrage |
| moto-cafe-racer.webp, moto-profil.webp | 36755706, 9924837 | recadrage |
| profil-leo.webp, profil-sam.webp, profil-moi.webp | 5504082, 8072136, 33524147 | recadrage carré |
`ecran-carte.webp`, `carte-france.webp` (captures de l'app) et `garage-video.webp` (ton clip) sont inchangés. La vidéo de 30 s contient encore les photos d'origine.

## Animations (GSAP)
GSAP 3.15, ScrollTrigger et MotionPath sont hébergés dans `js/vendor/` (aucun CDN). Les animations sont dans `js/anim.js` ; le site reste entièrement lisible sans elles et elles se désactivent si le visiteur a demandé moins de mouvement. GSAP posant des styles en ligne, la politique de contenu autorise `style-src 'unsafe-inline'` ; les scripts restent limités au site.

## Version de démonstration (GitHub Pages, Vercel)
`RASSO_APERCU=1 RASSO_DOMAINE=https://<adresse> python3 source/build.py` génère une version non indexée par les moteurs de recherche. Sans ces variables, le script génère la version de production. `vercel.json` applique les en-têtes de sécurité sur Vercel ; GitHub Pages ne permet pas d'en-têtes personnalisés.
