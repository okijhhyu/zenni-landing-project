<script setup></script>

<template>
  <footer class="footer">
    <div class="wrap footer__inner">
      <span class="footer__logo">zenni</span>
      <p>
        Это демонстрационная посадочная страница, созданная в рамках тестового
        задания, и она не связана с Zenni Optical Inc. Все товарные знаки
        принадлежат их правообладателям.
      </p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  border-top: 1px solid var(--line);
  padding: 32px 0 48px;
}

.footer__inner {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer__logo {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 18px;
}

.footer p {
  margin: 0;
  font-size: 13px;
  color: var(--ink-45);
  max-width: 62ch;
}
</style>
