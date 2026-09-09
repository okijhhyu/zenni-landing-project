<script setup>
const quotes = [
  {
    text: 'Взяла запасную пару дешевле, чем раньше стоила одна доплата по страховке. Теперь всегда есть очки в машине.',
    name: 'Прия Р.',
    detail: 'Заказала прогрессивные линзы',
  },
  {
    text: 'Виртуальная примерка реально совпала с тем, что пришло в посылке. Впервые заказ очков онлайн сработал как надо.',
    name: 'Маркус Д.',
    detail: 'Заказал очки с фильтром синего света',
  },
  {
    text: 'Сломал очки в воскресенье — к следующим выходным уже носил новые. Самый простой повторный заказ в моей жизни.',
    name: 'Анна Л.',
    detail: 'Заказала безободковую оправу',
  },
];
</script>

<template>
  <section id="reviews" class="reviews">
    <div class="wrap">
      <h2 class="section-title">Что говорят новые клиенты</h2>
      <div class="reviews__grid">
        <figure v-for="q in quotes" :key="q.name" class="quote">
          <blockquote>{{ q.text }}</blockquote>
          <figcaption>
            <strong>{{ q.name }}</strong>
            <span>{{ q.detail }}</span>
          </figcaption>
        </figure>
      </div>
    </div>
  </section>
</template>

<style scoped>
.reviews {
  padding: 72px 0;
}

.reviews__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

.quote {
  margin: 0;
  padding: 28px;
  background: var(--mint);
  border-radius: 20px;
}

.quote blockquote {
  margin: 0 0 20px;
  font-family: var(--font-display);
  font-size: 18px;
  line-height: 1.4;
  font-style: italic;
}

.quote figcaption {
  display: flex;
  flex-direction: column;
  font-size: 14px;
}

.quote figcaption span {
  color: var(--ink-45);
}

@media (max-width: 860px) {
  .reviews__grid {
    grid-template-columns: 1fr;
  }
}
</style>
