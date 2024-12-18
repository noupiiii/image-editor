<template>
  <div
    class="border-2 my-4 border-dashed border-gray-300 rounded-lg items-center justify-center cursor-pointer"
    @dragover.prevent="handleDragOver"
    @dragleave="handleDragLeave"
    @drop.prevent="handleDrop"
    @click="handleClick"
    :class="{'border-blue-500 bg-blue-100': isDragging, 'p-4' : !fileInput.value}"
  >
    <input
      type="file"
      accept="image/*"
      ref="fileInput"
      class="hidden"
      @change="handleFileChange"
    />
    <div v-if="isLoading" class="flex justify-center items-center h-32">
      <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary-500"></div>
    </div>
    <div v-else-if="preview" class="w-full">
      <img :src="preview" alt="Preview" class="rounded-lg w-full h-auto object-cover" />
    </div>
    <p v-else class="text-gray-500 text-center">
      Cliquez ou glissez une image ici pour la télécharger.
    </p>
  </div>
  <div v-if="fileInput.value != ''" class="flex gap-2 justify-end">
    <UTooltip text="Delete">
      <UButton icon="i-heroicons-trash" square variant="outline" @click="deleteImage" />
    </UTooltip>
    <UTooltip text="Replace">
      <UButton icon="i-heroicons-arrow-path-solid" square variant="outline" @click="replaceImage" />
    </UTooltip>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

// Refs pour stocker l'élément <input> et l'état du drag & drop
const fileInput = ref("");
const isDragging = ref(false);
const preview = ref(null);
const isLoading = ref(false); // État pour gérer le chargement


// Déclare l'événement que ce composant peut émettre
const emit = defineEmits(['file-selected']);

// Bouton "delete image"
const deleteImage = () => {
  fileInput.value.value = null;
  preview.value = null;
};

// Bouton "replace image"
const replaceImage = () => {
  // On appelle à nouveau le clic sur l'input
  fileInput.value.click();
};

// Gère l'événement "drag over"
const handleDragOver = () => {
  isDragging.value = true;
};

// Gère l'événement "drag leave"
const handleDragLeave = () => {
  isDragging.value = false;
};

// Gère l'événement "drop"
const handleDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) {
    processFile(file);
  }
};

// Gère le clic sur la zone (ouvre la boîte de dialogue)
const handleClick = () => {
  fileInput.value.click();
};

// Gère le changement de fichier via l'input
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file && file.type.startsWith('image/')) {
    processFile(file);
  }
};

// Lit le fichier et met à jour l'aperçu
const processFile = (file) => {
  isLoading.value = true; // Activer le chargement
  const reader = new FileReader();
  reader.onload = (e) => {
    preview.value = e.target.result;
    isLoading.value = false; // Désactiver le chargement
    emit('file-selected', { file, preview: e.target.result });
  };
  reader.readAsDataURL(file);
};
</script>

<style scoped>
.cursor-pointer {
  transition: border-color 0.3s ease, background-color 0.3s ease;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
