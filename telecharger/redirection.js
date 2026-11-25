// Page de téléchargement Rasso : un seul lien (et un seul QR code) pour iPhone et Android.
// Quand l'application Android sera publiée, colle son lien Google Play ci-dessous : les téléphones Android y seront redirigés.
(function () {
  var APP_STORE = "https://apps.apple.com/fr/app/rasso/id6758964694";
  var GOOGLE_PLAY = ""; // ex. "https://play.google.com/store/apps/details?id=..."
  var ua = navigator.userAgent || "";
  var ios = /iPhone|iPad|iPod/i.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  var android = /Android/i.test(ua);
  if (ios) { location.replace(APP_STORE); return; }
  if (android && GOOGLE_PLAY) { location.replace(GOOGLE_PLAY); return; }
  var play = document.getElementById("play");
  if (GOOGLE_PLAY) { play.href = GOOGLE_PLAY; play.textContent = "Télécharger sur Google Play"; play.removeAttribute("aria-disabled"); }
})();
