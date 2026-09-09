// Google Analytics (GA4) / Google Tag Manager loader.
//
// IDs come from env vars (VITE_GA_ID / VITE_GTM_ID) — nothing is
// hardcoded. Set them in `.env` locally or as Environment Variables
// in Vercel. If a var isn't set, that snippet is simply skipped
// instead of loading with a fake placeholder ID.

const GA_ID = import.meta.env.VITE_GA_ID;
const GTM_ID = import.meta.env.VITE_GTM_ID;

function initGtag() {
  if (!GA_ID) return;

  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA_ID);
}

function initGtm() {
  if (!GTM_ID) return;

  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });

  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtm.js?id=${GTM_ID}`;
  document.head.appendChild(script);

  // <noscript> fallback (mainly for completeness — this is a Vue SPA,
  // so the app itself already requires JS to render anything).
  const noscript = document.createElement('noscript');
  const iframe = document.createElement('iframe');
  iframe.src = `https://www.googletagmanager.com/ns.html?id=${GTM_ID}`;
  iframe.height = '0';
  iframe.width = '0';
  iframe.style.display = 'none';
  iframe.style.visibility = 'hidden';
  noscript.appendChild(iframe);
  document.body.insertBefore(noscript, document.body.firstChild);
}

export function initAnalytics() {
  initGtag();
  initGtm();
}
