// Base URL of the click-tracking backend (Part 2 of the task).
// Set VITE_BACKEND_URL in a .env / .env.production file when deploying;
// falls back to a local dev server otherwise.
export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000';

// The brand this landing page represents. Sent as the `offer` param.
export const OFFER = 'Zenni Optical';

/**
 * Build the backend /click URL for a given CTA.
 * `sub1` identifies which button/section triggered the click, so it is
 * possible to see which CTA converts best just by reading the sub1 column.
 */
export function clickUrl(sub1) {
  const params = new URLSearchParams({ offer: OFFER, sub1 });
  return `${BACKEND_URL}/click?${params.toString()}`;
}

/**
 * Push a GTM/GA4 event for the CTA click, then navigate to the backend
 * redirect endpoint. Called from every CTA button in the page.
 */
export function fireCta(sub1, label) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'cta_click',
    cta_id: sub1,
    cta_label: label,
    offer: OFFER,
  });
  window.location.href = clickUrl(sub1);
}
