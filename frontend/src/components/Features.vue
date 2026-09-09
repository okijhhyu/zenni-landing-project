<script setup>
const features = [
  {
    title: 'Цены, которые понятны',
    body: 'Полный комплект — оправа, линзы, покрытия — от $6.95. Без наценок из ниоткуда и цен как в кабинете офтальмолога.',
    tint: '#FFC93C',
  },
  {
    title: '1000+ оправ на выбор',
    body: 'Металл, ацетат, безободковые, с фильтром синего света, солнцезащитные — новинки каждый месяц, размеры под любое лицо.',
    tint: '#D7E5E4',
  },
  {
    title: 'Примерка перед покупкой',
    body: 'Загрузите селфи или используйте камеру, чтобы увидеть любую оправу на своём лице ещё до заказа.',
    tint: '#FF4B3E',
  },
];
</script>

<template>
  <section id="features" class="features">
    <div class="wrap">
      <h2 class="section-title">Почему выбирают Zenni</h2>
      <div class="features__grid">
        <article v-for="f in features" :key="f.title" class="feature-card">
          <span class="feature-card__dot" :style="{ background: f.tint }"></span>
          <h3>{{ f.title }}</h3>
          <p>{{ f.body }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.features {
  padding: 72px 0;
  border-top: 1px solid var(--line);
}

.section-title {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: clamp(28px, 3.4vw, 38px);
  max-width: 16ch;
  margin: 0 0 44px;
}

.features__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 36px;
}

.feature-card h3 {
  font-family: var(--font-display);
  font-size: 21px;
  font-weight: 600;
  margin: 18px 0 10px;
}

.feature-card p {
  font-size: 15.5px;
  color: var(--ink-70);
  margin: 0;
  max-width: 32ch;
}

.feature-card__dot {
  display: block;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

@media (max-width: 860px) {
  .features__grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}
</style>
