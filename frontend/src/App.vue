<script setup>
import SiteHeader from './components/SiteHeader.vue';
import Hero from './components/Hero.vue';
import Features from './components/Features.vue';
import HowItWorks from './components/HowItWorks.vue';
import Testimonials from './components/Testimonials.vue';
import FinalCta from './components/FinalCta.vue';
import SiteFooter from './components/SiteFooter.vue';
</script>

<template>
  <SiteHeader />
  <main>
    <Hero />
    <Features />
    <HowItWorks />
    <Testimonials />
    <FinalCta />
  </main>
  <SiteFooter />
</template>
