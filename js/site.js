/* Rasso — interactions du site (aucun cookie, aucun traceur, aucune requête externe). */
(function () {
  'use strict';
  var $ = function (s) { return document.querySelector(s); }, $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

  // changement de page : toujours repartir du haut (sauf lien vers une ancre)
  try { history.scrollRestoration = 'manual'; } catch (e) {}
  var toTop = function () {
    if (location.hash && location.hash.length > 1) return;
    window.scrollTo(0, 0); document.documentElement.scrollTop = 0; document.body.scrollTop = 0;
    var top = document.querySelector('.top'); if (top && top.scrollIntoView) top.scrollIntoView({ block: 'start' });
  };
  toTop(); window.addEventListener('pageshow', toTop); window.addEventListener('load', toTop);

  // menu mobile : l'itinéraire se déplie
  var burger = $('#burger'), nav = $('#nav');
  if (burger && nav) {
    var close = function () { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); };
    burger.addEventListener('click', function () { burger.setAttribute('aria-expanded', nav.classList.toggle('open') ? 'true' : 'false'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  // vidéo : chapitres
  var film = $('#film');
  $$('.chap button').forEach(function (b) {
    b.addEventListener('click', function () {
      if (!film) return;
      var t = parseFloat(b.dataset.t), go = function () { film.currentTime = t; var p = film.play(); if (p && p.catch) p.catch(function () {}); };
      if (film.readyState >= 1) go(); else { film.addEventListener('loadedmetadata', go, { once: true }); film.load(); }
    });
  });

  // convoi : les trois types de trajet redessinent le tracé
  var TRAJETS = {
    v: ['M130,450 C 380,480 60,290 340,285 C 620,280 260,130 500,135 C 630,138 600,100 690,100', 'Virages : la route qui tourne, pour le plaisir de conduire.'],
    a: ['M130,450 C 220,395 290,340 360,295 C 440,245 500,200 560,165 C 610,135 650,112 690,100', 'Autoroute : le plus direct, pour arriver ensemble sans détour.'],
    e: ['M130,450 C 290,455 260,340 380,300 C 510,258 450,165 560,148 C 630,136 650,106 690,100', 'Équilibré : un peu des deux, selon l’envie du groupe.']
  };
  var path = $('#trajet'), chips = $$('.chip[data-trajet]'), ttxt = $('#trajet-txt');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (o) { o.setAttribute('aria-pressed', o === c ? 'true' : 'false'); });
      var t = TRAJETS[c.dataset.trajet];
      path.style.d = 'path("' + t[0] + '")'; path.setAttribute('d', t[0]);
      if (ttxt) ttxt.textContent = t[1];
    });
  });

  // découverte : démonstration du swipe
  var swipe = $('#swipe');
  if (swipe) {
    var stack = swipe.querySelector('.sw-stack'), msg = $('#swmsg'), busy = false;
    var act = function (dir) {
      if (busy) return; var card = stack.lastElementChild; if (!card) return; busy = true;
      card.classList.add(dir === 'left' ? 'go-left' : 'go-right');
      msg.textContent = dir === 'left' ? 'Tu passes au garage suivant.' : 'Demande d’ami envoyée à ' + card.dataset.nom + '. L’amitié commence quand la demande est acceptée.';
      setTimeout(function () { card.classList.remove('go-left', 'go-right'); stack.insertBefore(card, stack.firstElementChild); busy = false; }, 480);
    };
    swipe.querySelectorAll('.sb').forEach(function (b) { b.addEventListener('click', function () { act(b.dataset.dir); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') act('left'); if (e.key === 'ArrowRight') act('right'); });
  }

  // progression : démonstration de la barre d'XP
  var xp = $('#xp');
  if (xp) {
    var fill = $('#xfill'), lvl = $('#lvl'), v = 16;
    xp.querySelectorAll('button.xrow').forEach(function (b) {
      b.addEventListener('click', function () {
        v += parseInt(b.dataset.xp, 10);
        if (v >= 100) {
          fill.style.width = '100%'; lvl.textContent = 'Niveau supérieur'; lvl.classList.remove('up'); void lvl.offsetWidth; lvl.classList.add('up');
          v = 8; setTimeout(function () { fill.style.width = v + '%'; }, 900);
        } else { fill.style.width = v + '%'; lvl.classList.remove('up'); lvl.textContent = 'Encore un effort…'; }
      });
    });
  }
})();
