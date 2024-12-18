<template>
  <div>
    <h1 class="text-6xl w-fit font-bold text-primary-500">
      Transfert colors
    </h1>
    <p>Transfer colors from one image to another.</p>

    <!-- From Image Section -->
    <div class="flex items-end gap-2 mt-6">
      <h2 class="text-xl font-semibold">From image</h2>
      <UBadge variant="outline" color="primary" class="h-fit">
        The image from which the colors will be extracted.
      </UBadge>
    </div>
    <FileInput @file-selected="handleFromFileSelected" />

    <!-- To Image Section -->
    <div class="flex items-end gap-2 mt-6" id="toImageSection">
      <h2 class="text-xl font-semibold">To image</h2>
      <UBadge variant="outline" color="primary" class="h-fit">
        The image to which the colors will be applied.
      </UBadge>
    </div>
    <FileInput @file-selected="handleToFileSelected" />

    <!-- Form Actions Section -->
    <div class="flex max-w-full gap-3 justify-between items-end mt-8" id="formActionsSection">
      <UFormGroup class="w-56" label="Number of colors (max 5)">
        <UInput
          type="number"
          v-model="numColors"
          min="1"
          max="5"
          placeholder="Enter a number"
        />
      </UFormGroup>
      <UFormGroup class="w-full">
        <UButton :label="isLoading ? 'Submitting':'Submit'" :icon="isLoading ? 'i-svg-spinners-3-dots-bounce' : ''" block variant="outline" @click="fetchApiData" :disabled="!fromFileInfo || !toFileInfo || isLoading" />
      </UFormGroup>
    </div>

    <!-- Result Section -->
    <div v-if="recreateImage?.transferred_image" class="mt-10 w-full" id="resultSection">
      <UDivider class="mb-6" />
      <div class="flex justify-between items-center">
        <h2 class="text-xl">Result</h2>
        <div>
          <!-- AJOUT : Bouton de téléchargement -->
          <UButton
            label="Download"
            variant="outline"
            icon="i-heroicons-document-arrow-down"
            @click="handleDownload"
          />
        </div>
      </div>
      <img
        :src="recreateImage.transferred_image"
        alt="Transferred Image"
        class="mt-4 w-full rounded-md"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const fromFileInfo = ref(null);
const toFileInfo = ref(null);
const numColors = ref(5);
const recreateImage = ref(null);
const isLoading = ref(false)

const config = useRuntimeConfig()

const handleFromFileSelected = async (fileData) => {
  fromFileInfo.value = fileData;
  await nextTick();
  const section = document.getElementById('toImageSection')
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' })
  }
};

const handleToFileSelected = async (fileData) => {
  toFileInfo.value = fileData;
  await nextTick();
  const section = document.getElementById('formActionsSection')
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' })
  }
};

const fetchApiData = async () => {
  isLoading.value = true;

  if (!fromFileInfo.value?.file) {
    console.error('No source file selected.');
    return;
  }

  if (!toFileInfo.value?.file) {
    console.error('No target file selected.');
    return;
  }

  if (numColors.value < 1) {
    console.error('Number of colors must be between 1 and 5.');
    return;
  }

  try {
    const formData = new FormData();
    formData.append('fromFile', fromFileInfo.value.file);
    formData.append('toFile', toFileInfo.value.file);
    formData.append('n_colors', numColors.value);

    const data = await $fetch('/transfert-colors', {
      baseURL: config.public.API_URL,
      method: 'POST',
      body: formData,
    });

    recreateImage.value = {
      ...data,
    };

    await nextTick()
    const section = document.getElementById('resultSection')
    if (section) {
    section.scrollIntoView({ behavior: 'smooth' })
    } else {
      console.log(section)
    }
    console.log('Transferred Image:', recreateImage.value.transferred_image);
  } catch (error) {
    console.error('Error during API request:', error);
  } finally {
    isLoading.value = false;
  }
};

const handleDownload = () => {
  // Vérifie si l'image est disponible
  if (!recreateImage.value?.transferred_image) {
    console.warn("Pas d'image à télécharger");
    return;
  }

  // On suppose que `recreateImage.value.transferred_image` est une URL base64 ou un blob
  const link = document.createElement('a');
  link.href = recreateImage.value.transferred_image;
  link.download = 'transferred_image.png'; // Nom du fichier lors du téléchargement
  link.click();
};
</script>
