<script setup>
import { fireCta } from '../config.js';
</script>

<template>
  <header class="header">
    <div class="wrap header__inner">
      <a href="#top" class="logo" aria-label="Zenni Optical">
        <svg width="28" height="28" viewBox="0 0 64 64" fill="none" aria-hidden="true">
          <circle cx="21" cy="34" r="12" stroke="#FF4B3E" stroke-width="5" />
          <circle cx="43" cy="34" r="12" stroke="#FF4B3E" stroke-width="5" />
          <path d="M33 31.5c0-2.5-2-3.5 0-3.5s0 1 0 3.5z" stroke="#FF4B3E" stroke-width="5" stroke-linecap="round" />
          <path d="M9 32l3-6" stroke="#FF4B3E" stroke-width="5" stroke-linecap="round" />
          <path d="M55 32l-3-6" stroke="#FF4B3E" stroke-width="5" stroke-linecap="round" />
        </svg>
        <span>zenni</span>
      </a>

      <nav class="nav" aria-label="Основное меню">
        <a href="#features">Почему Zenni</a>
        <a href="#how">Как это работает</a>
        <a href="#reviews">Отзывы</a>
      </nav>

      <button class="btn btn-dark header__cta" @click="fireCta('header_nav', 'Выбрать очки')">
        Выбрать очки
      </button>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 40;
  background: rgba(251, 250, 246, 0.88);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--line);
}

.header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--ink);
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 22px;
  letter-spacing: -0.01em;
}

.nav {
  display: flex;
  gap: 28px;
  font-size: 15px;
}

.nav a {
  text-decoration: none;
  color: var(--ink-70);
}

.nav a:hover {
  color: var(--ink);
}

.header__cta {
  padding: 11px 20px;
  font-size: 14px;
  white-space: nowrap;
}

@media (max-width: 720px) {
  .nav {
    display: none;
  }
  .header__inner {
    height: 64px;
  }
  .logo span {
    display: none;
  }
}
</style>
