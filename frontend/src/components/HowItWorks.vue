<script setup>
import { fireCta } from '../config.js';

const steps = [
  {
    n: '01',
    title: 'Выберите оправу',
    body: 'Фильтруйте по форме лица, размеру и стилю — или примерьте десятки вариантов онлайн, пока не найдёте подходящий.',
  },
  {
    n: '02',
    title: 'Укажите рецепт',
    body: 'Введите его вручную, загрузите фото рецепта или назовите бренд текущих очков — мы подберём аналог.',
  },
  {
    n: '03',
    title: 'Носите уже через несколько дней',
    body: 'Каждая пара делается под заказ и доставляется за 3–7 рабочих дней, вернуть можно в течение 100 дней.',
  },
];
</script>

<template>
  <section id="how" class="how">
    <div class="wrap how__inner">
      <h2 class="section-title">От выбора до примерки — три шага</h2>

      <ol class="steps">
        <li v-for="s in steps" :key="s.n" class="step">
          <span class="step__n">{{ s.n }}</span>
          <div>
            <h3>{{ s.title }}</h3>
            <p>{{ s.body }}</p>
          </div>
        </li>
      </ol>

      <button class="btn btn-primary how__cta" @click="fireCta('how_it_works', 'Пройти тест по подбору оправы')">
        Пройти тест по подбору оправы
      </button>
    </div>
  </section>
</template>

<style scoped>
.how {
  padding: 72px 0;
  background: var(--ink);
  color: var(--paper);
  border-radius: 28px;
  margin: 0 20px;
}

.how .section-title {
  color: var(--paper);
}

.steps {
  list-style: none;
  margin: 0 0 40px;
  padding: 0;
  display: grid;
  gap: 28px;
}

.step {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 20px;
  padding-bottom: 28px;
  border-bottom: 1px solid rgba(251, 250, 246, 0.14);
}

.step:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.step__n {
  font-family: var(--font-display);
  font-size: 28px;
  color: var(--amber);
}

.step h3 {
  font-family: var(--font-display);
  font-size: 21px;
  font-weight: 600;
  margin: 0 0 6px;
}

.step p {
  margin: 0;
  color: rgba(251, 250, 246, 0.72);
  max-width: 50ch;
  font-size: 15.5px;
}

.how__cta {
  background: var(--amber);
  color: var(--ink);
  box-shadow: 0 6px 0 #dba928;
}

@media (max-width: 860px) {
  .how {
    margin: 0;
    border-radius: 0;
  }
}
</style>
