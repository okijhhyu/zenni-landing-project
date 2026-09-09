<script setup>
import { fireCta } from '../config.js';
</script>

<template>
  <section id="top" class="hero">
    <div class="wrap hero__inner">
      <div class="hero__copy">
        <p class="eyebrow">Очки по рецепту без лишних сложностей</p>
        <h1 class="hero__title">
          Видеть чётко.
          <span class="underline-wrap">
            Платить меньше.
            <svg class="underline" viewBox="0 0 300 24" preserveAspectRatio="none" aria-hidden="true">
              <path d="M2 18C60 8 220 6 298 16" stroke="#FFC93C" stroke-width="10" stroke-linecap="round" fill="none" />
            </svg>
          </span>
        </h1>
        <p class="hero__sub">
          Полный комплект очков по рецепту от $6.95, больше 1000 оправ и
          примерка через камеру — вы точно увидите, как они будут выглядеть,
          ещё до доставки.
        </p>

        <div class="hero__ctas">
          <button class="btn btn-primary" @click="fireCta('hero_primary', 'Выбрать очки от $6.95')">
            Выбрать очки от $6.95
          </button>
          <button class="btn btn-ghost" @click="fireCta('hero_secondary', 'Примерить оправу онлайн')">
            Примерить оправу онлайн
          </button>
        </div>

        <ul class="hero__trust">
          <li>Бесплатная доставка от $49</li>
          <li>Возврат в течение 100 дней</li>
          <li>Доставка за 3–7 рабочих дней</li>
        </ul>
      </div>

      <div class="hero__art" aria-hidden="true">
        <svg viewBox="0 0 420 380" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="205" cy="190" r="180" fill="#D7E5E4" />
          <circle cx="330" cy="90" r="46" fill="#FFC93C" />
          <g transform="translate(52 150)">
            <circle cx="70" cy="70" r="66" fill="none" stroke="#16181D" stroke-width="7" />
            <circle cx="248" cy="70" r="66" fill="none" stroke="#16181D" stroke-width="7" />
            <path d="M136 62c0-14-12-18 0-18s0 4 0 18z" stroke="#16181D" stroke-width="7" stroke-linecap="round" fill="none" />
            <path d="M4 58L-30 34" stroke="#16181D" stroke-width="7" stroke-linecap="round" />
            <path d="M314 58l34-24" stroke="#16181D" stroke-width="7" stroke-linecap="round" />
            <circle cx="70" cy="70" r="66" fill="#FF4B3E" fill-opacity="0.18" />
            <circle cx="248" cy="70" r="66" fill="#FF4B3E" fill-opacity="0.18" />
          </g>
        </svg>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  padding: 64px 0 88px;
}

.hero__inner {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 48px;
  align-items: center;
}

.eyebrow {
  font-size: 15px;
  color: var(--coral-dark);
  font-weight: 600;
  margin: 0 0 18px;
}

.hero__title {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: clamp(40px, 5.6vw, 68px);
  line-height: 1.05;
  letter-spacing: -0.01em;
  margin: 0 0 22px;
  max-width: 15ch;
}

.underline-wrap {
  position: relative;
  display: inline-block;
}

.underline {
  position: absolute;
  left: -4px;
  right: -4px;
  bottom: -6px;
  width: calc(100% + 8px);
  height: 0.28em;
  z-index: -1;
}

.hero__sub {
  font-size: 18px;
  color: var(--ink-70);
  max-width: 46ch;
  margin: 0 0 32px;
}

.hero__ctas {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 28px;
}

.hero__trust {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px 22px;
  font-size: 14px;
  color: var(--ink-45);
}

.hero__trust li {
  position: relative;
  padding-left: 16px;
}

.hero__trust li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 7px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--coral);
}

.hero__art svg {
  width: 100%;
  height: auto;
}

@media (max-width: 860px) {
  .hero__inner {
    grid-template-columns: 1fr;
  }
  .hero__art {
    order: -1;
    max-width: 320px;
    margin: 0 auto;
  }
  .hero {
    padding: 36px 0 56px;
  }
}
</style>
