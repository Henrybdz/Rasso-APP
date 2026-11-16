/* Rasso — animations GSAP (ScrollTrigger + MotionPath).
   Tout le contenu reste lisible sans ce fichier ; rien ne s'anime si l'utilisateur a demandé moins de mouvement. */
(function () {
  'use strict';
  if (!window.gsap || !window.ScrollTrigger) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger); gsap.config({ nullTargetWarn: false });
  var has = function (s) { return !!document.querySelector(s); };
  if (window.MotionPathPlugin) gsap.registerPlugin(MotionPathPlugin);
  var $$ = function (s, r) { return gsap.utils.toArray((r || document).querySelectorAll(s)); };
  var OUT = 'power3.out';

  /* ---------- 1. Titres : les mots montent un par un ---------- */
  function splitWords(h) {
    var out = [];
    Array.prototype.slice.call(h.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        var frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
          var w = document.createElement('span'), i = document.createElement('span');
          w.className = 'w'; i.className = 'wi'; i.textContent = part; w.appendChild(i); frag.appendChild(w); out.push(i);
        });
        h.replaceChild(frag, n);
      } else if (n.nodeName === 'MARK') { out.push(n); }
    });
    return out;
  }
  var h1 = document.querySelector('main h1');
  if (h1 && !h1.closest('.legal')) {
    var words = splitWords(h1), mark = h1.querySelector('mark'), tl = gsap.timeline({ defaults: { ease: 'power4.out' } });
    tl.from(words.filter(function (w) { return w !== mark; }), { yPercent: 115, rotate: 5, duration: .9, stagger: .07 }, .05);
    if (mark) tl.from(mark, { scaleX: 0, transformOrigin: '0 50%', duration: .6, ease: 'power3.inOut' }, '-=.45').from(mark, { color: 'rgba(15,15,18,0)', duration: .3 }, '-=.2');
    var intro = $$('.hero-txt > *:not(h1), .phero-txt > *:not(h1), .ghero-in > *:not(h1), .qhero .wrap > *:not(h1)');
    tl.from(intro, { y: 26, autoAlpha: 0, duration: .7, stagger: .08, ease: OUT }, .25);
  }

  /* ---------- 2. Héros : le téléphone et ses cartes ---------- */
  var stage = document.querySelector('.hero-stage');
  if (stage) {
    var parallaxe = function () {   // lancée après l'entrée, pour ne pas se disputer les mêmes éléments
      var st = { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: .6 };
      gsap.to('.hero-stage .phone', { yPercent: 9, ease: 'none', scrollTrigger: st });
      gsap.to('.fl-ev', { yPercent: -70, ease: 'none', scrollTrigger: st });
      gsap.to('.fl-car', { yPercent: -45, ease: 'none', scrollTrigger: st });
      gsap.to('.fl-xp', { yPercent: -120, ease: 'none', scrollTrigger: st });
    };
    gsap.timeline({ onComplete: parallaxe })
      .from('.hero-stage .phone', { y: 90, rotate: 7, autoAlpha: 0, duration: 1.1, ease: OUT }, .15)
      .fromTo('.hero-stage .fl', { scale: .4, autoAlpha: 0 }, { scale: 1, autoAlpha: 1, duration: .7, stagger: .14, ease: 'back.out(1.8)' }, .7)
      .from('.fl-xp u', { scaleX: 0, transformOrigin: '0 50%', duration: 1, ease: 'power2.out' }, 1.2);
    gsap.from('.hero-facts li', { y: 24, autoAlpha: 0, duration: .6, stagger: .08, ease: OUT, delay: .9 });
  }
  gsap.from('.phero-vis > *, .chero .ui', { y: 70, autoAlpha: 0, rotate: 3, duration: 1, ease: OUT, delay: .3 });

  /* ---------- 3. En-tête : les arrêts de l'itinéraire s'allument ---------- */
  gsap.from('.route-nav li', { y: -14, autoAlpha: 0, duration: .5, stagger: .05, ease: OUT });
  gsap.to('.route-nav a[aria-current] i', { scale: 1.25, duration: .9, repeat: -1, yoyo: true, ease: 'sine.inOut' });

  /* ---------- 4. Apparitions au défilement ---------- */
  function batch(sel, from, stagger) {
    var els = $$(sel); if (!els.length) return;
    gsap.set(els, from);
    ScrollTrigger.batch(els, {
      start: 'top 88%', once: true,
      onEnter: function (b) { gsap.to(b, { x: 0, y: 0, scale: 1, rotate: 0, autoAlpha: 1, duration: .8, ease: OUT, stagger: stagger || .09, overwrite: true, clearProps: 'transform,opacity,visibility' }); }
    });
  }
  batch('.sec-h > *, .fiche-txt > *, .amis-txt > *, .msg-txt > *, .profil-txt > *, .video-txt > *:not(.chap), .orga-card > *, .charte-in > div:first-child > *', { y: 30, autoAlpha: 0 }, .07);
  batch('.tile', { y: 60, autoAlpha: 0, scale: .96 }, .1);
  batch('.tcard', { y: 60, autoAlpha: 0 }, .12);
  batch('.trio > div, .charte-g p, .role-grid li', { y: 34, autoAlpha: 0 }, .1);
  batch('.steps li, .roadmap li, .flow li', { x: -36, autoAlpha: 0 }, .13);
  batch('.spec div, .chap li, .faq-col details', { y: 20, autoAlpha: 0 }, .06);
  batch('.duo article, .pcard, .msg-in > .ui, .video-box', { y: 70, autoAlpha: 0, rotate: 2 }, .12);
  batch('.liked img', { y: 40, autoAlpha: 0, scale: .9 }, .1);

  /* galerie du garage : chaque photo se dévoile par le bas */
  $$('.gal figure').forEach(function (f, i) {
    gsap.from(f, { clipPath: 'inset(100% 0% 0% 0%)', duration: 1, ease: 'power3.inOut', delay: i * .09, scrollTrigger: { trigger: '.gal', start: 'top 82%', once: true } });
    gsap.from(f.querySelector('img'), { scale: 1.35, duration: 1.4, ease: OUT, delay: i * .09, scrollTrigger: { trigger: '.gal', start: 'top 82%', once: true } });
  });

  /* grandes photos : parallaxe lente */
  $$('.ghero-photo img, .orga-photo img').forEach(function (im) {
    gsap.fromTo(im, { yPercent: -7, scale: 1.16 }, { yPercent: 7, ease: 'none', scrollTrigger: { trigger: im.parentNode.parentNode, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  $$('.tile > img').forEach(function (im) {
    gsap.fromTo(im, { yPercent: -5, scale: 1.12 }, { yPercent: 5, ease: 'none', scrollTrigger: { trigger: im.parentNode, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* podium, barres, tracé de la tuile Convois */
  if (has('.podium')) gsap.from('.podium i', { scaleY: 0, transformOrigin: '50% 100%', duration: .8, stagger: .12, ease: 'back.out(1.4)', scrollTrigger: { trigger: '.podium', start: 'top 88%', once: true } });
  if (has('.mini-xp')) gsap.from('.mini-xp u', { scaleX: 0, transformOrigin: '0 50%', duration: 1.2, ease: 'power2.out', scrollTrigger: { trigger: '.mini-xp', start: 'top 90%', once: true } });
  $$('.t-convoi > svg path, .cross .t1, .cross .t2').forEach(function (p) {
    var len = p.getTotalLength();
    gsap.fromTo(p, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: 1.6, ease: 'power2.inOut', scrollTrigger: { trigger: p, start: 'top 88%', once: true } });
  });
  if (has('.cross')) gsap.from('.cross circle, .cross-l', { scale: 0, autoAlpha: 0, transformOrigin: '50% 50%', duration: .5, delay: 1.2, ease: 'back.out(2)', scrollTrigger: { trigger: '.cross', start: 'top 88%', once: true } });
  if (has('.stars')) gsap.from('.stars i', { scale: 0, rotate: -90, duration: .5, stagger: .08, ease: 'back.out(2)', scrollTrigger: { trigger: '.stars', start: 'top 90%', once: true } });
  if (has('.sw')) gsap.fromTo('.sw', { y: 80, rotate: function (i) { return (i - 1.5) * 9; }, autoAlpha: 0 }, { y: 0, rotate: 0, autoAlpha: 1, duration: .9, stagger: .1, ease: OUT, delay: .35, clearProps: 'transform,opacity,visibility' });

  /* ---------- 5. Convois : trois véhicules suivent le tracé choisi ---------- */
  var trajet = document.getElementById('trajet');
  if (trajet && window.MotionPathPlugin) {
    var svg = trajet.ownerSVGElement, dots = ['#B0F20A', '#FFFFFF', '#9AA0A6'].map(function (c) {
      var d = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      d.setAttribute('r', 14); d.setAttribute('fill', c); d.setAttribute('class', 'cvd'); svg.insertBefore(d, svg.querySelector('.pt')); return d;
    });
    var len = trajet.getTotalLength();
    gsap.fromTo(trajet, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: 1.4, ease: 'power2.inOut', delay: .5, onComplete: function () { gsap.set(trajet, { clearProps: 'strokeDasharray,strokeDashoffset' }); } });
    var roule = function (delay) {
      gsap.killTweensOf(dots); gsap.set(dots, { autoAlpha: 0 });
      dots.forEach(function (d, i) {
        gsap.fromTo(d, { autoAlpha: 1 }, { motionPath: { path: trajet, align: trajet, alignOrigin: [.5, .5], start: 0, end: .97 - i * .07 }, duration: 3.4, delay: (delay || 0) + i * .28, ease: 'power1.inOut', repeat: -1, repeatDelay: .9, immediateRender: false,
          onStart: function () { gsap.set(d, { autoAlpha: 1 }); } });
      });
    };
    roule(1.9);
    $$('.chip[data-trajet]').forEach(function (c) { c.addEventListener('click', function () { setTimeout(function () { roule(.1); }, 620); }); });
  }

  /* ---------- 6. Bandeau « Étape suivante » ---------- */
  var nx = document.querySelector('.next');
  if (nx) {
    var tn = gsap.timeline({ scrollTrigger: { trigger: nx, start: 'top 85%', once: true } });
    tn.from('.next p', { y: 20, autoAlpha: 0, duration: .5, ease: OUT })
      .from('.next a span', { xPercent: -14, autoAlpha: 0, duration: .9, ease: 'power4.out' }, '-=.3')
      .fromTo('.next .arr', { x: -120, autoAlpha: 0 }, { x: 0, autoAlpha: 1, duration: .8, ease: 'back.out(1.6)' }, '-=.6')
      .to('.next .arr', { x: 16, duration: .8, repeat: -1, yoyo: true, ease: 'sine.inOut' });
  }

  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
