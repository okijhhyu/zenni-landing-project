<script setup>
import { fireCta } from '../config.js';
</script>

<template>
  <section class="final">
    <div class="wrap final__inner">
      <h2>Новые очки не должны стоить дороже, чем того заслуживает оправа.</h2>
      <div class="final__ctas">
        <button class="btn btn-primary" @click="fireCta('final_primary', 'Смотреть все оправы')">
          Смотреть все оправы
        </button>
        <button class="btn btn-ghost" @click="fireCta('final_secondary', 'Очки от $6.95')">
          Очки от $6.95
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.final {
  padding: 80px 0 96px;
  text-align: center;
}

.final__inner h2 {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: clamp(28px, 4vw, 42px);
  max-width: 20ch;
  margin: 0 auto 32px;
  line-height: 1.15;
}

.final__ctas {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 14px;
}
</style>
