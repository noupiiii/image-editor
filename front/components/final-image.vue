<template>
    <div v-if="recreateImage?.transferred_image" class="mt-6">
      <img
        :src="recreateImage.transferred_image"
        alt="Transferred Image"
        class="mt-4"
      />
    </div>
    <div v-else class="mt-6 text-gray-500">
      No image transferred yet.
    </div>
  </template>
  
  <script setup>
  defineProps({
    recreateImage: {
      type: Object,
      required: true,
    },
  });
  </script>
  