<template>
  <div>
    <h1
      class="text-6xl w-fit font-bold text-primary-500 bg-clip-text"
    >
      Color Palette
    </h1>
    <p>Upload an image to extract its color palette.</p>
    <FileInput
    @file-selected="handleFileSelected"
    :colors="colors"
    />
    <div class="flex w-full gap-3 justify-between items-end" id="fromFormActionsSection">
      <UFormGroup label="Number of colors">
        <UInput type="number" placeholder="" v-model="numColors" />
      </UFormGroup>
      <UFormGroup class="w-full">
        <UButton :label="isLoading ? 'Submitting':'Submit'" :icon="isLoading ? 'i-svg-spinners-3-dots-bounce' : ''" block variant="outline" @click="fetchApiData" :disabled="!fileInfo || isLoading" />
      </UFormGroup>
    </div>

    <UCard v-if="colors.length" class="my-3 w-full">
      <h2 class="text-xl mb-2 font-semibold">Extracted colors</h2>
      <div
        v-for="(color, index) in colors"
        :key="index"
        class="w-full h-12 mb-2 rounded justify-around flex items-center px-2"
        :class="getTextColorClass(color)"
        :style="{ backgroundColor: color }"
        id="colorsSection"
      >
        <div @click="copyClipboard(color)">
          <UTooltip text="Copy to clipboard">
            <p class="cursor-pointer">
              {{ color }}
            </p>
          </UTooltip>
        </div>
        <div @click="copyClipboard(rgbaValues[index])">
          <UTooltip text="Copy to clipboard">
            <p class="cursor-pointer">
              {{ rgbaValues[index] }}
            </p>
          </UTooltip>
        </div>
      </div>
    </UCard>
  </div>
</template>

<script setup>
const fileInfo = ref(null);
const numColors = ref(5);
const colors = ref([]);
const rgbaValues = ref([]);
const isLoading = ref(false);

const toast = useToast();
const colorsComposable = useColors();
const config = useRuntimeConfig();

const handleFileSelected = async (fileData) => {
  fileInfo.value = fileData;
  await nextTick();
  const section = document.getElementById('formActionsSection')
  if (section) {
    section.scrollIntoView({behavior: 'smooth'});
  }
};

const fetchApiData = async () => {
  isLoading.value = true;
  if (!fileInfo.value || !fileInfo.value.file) {
    console.error('No file selected.');
    return;
  }

  if (numColors.value <= 0) {
    console.error('Number of colors must be greater than 0.');
    return;
  }

  try {
    const formData = new FormData();
    formData.append('file', fileInfo.value.file);
    formData.append('n_colors', numColors.value);

    const data = await $fetch('/extract-colors', {
      baseURL: config.public.API_URL,
      method: 'POST',
      body: formData,
    });

    colors.value = data.palette;
    rgbaValues.value = colors.value.map((color) =>
      colorsComposable.hexToRGB(color)
    );

    // renvoyer l'utilisateur à la bonne section (celle des couleurs) une fois les couleurs renvoyés par l'api
    await nextTick();
    const section = document.getElementById('colorsSection')
    if (section) {
      section.scrollIntoView({behavior: 'smooth'});
    }

    isLoading.value = false;

    console.log('Extracted Colors:', colors.value);
    console.log('RGBA Values:', rgbaValues.value);
  } catch (error) {
    console.error('Erreur lors de la requête API:', error);
  } finally {
    isLoading.value = false
  }
};

// Fonction pour copier dans le presse-papiers
const copyClipboard = (stringValue) => {
  navigator.clipboard.writeText(stringValue).then(() => {
    console.log(`Copied to clipboard: ${stringValue}`);
    toast.add({
    id: 'copy_clipboard',
    title: 'Copied to clipboard.',
    description: `${stringValue} has been copied to the clipboard.`,
    icon: 'i-heroicons-clipboard',
  })
  }).catch((error) => {
    console.error('Failed to copy text to clipboard:', error);
  });
};

// Fonction pour déterminer la luminosité et ajuster la classe de texte
const getTextColorClass = (hex) => {
  const getBrightness = (hex) => {
    const [r, g, b] = hex.match(/\w\w/g).map((c) => parseInt(c, 16));
    return (r * 299 + g * 587 + b * 114) / 1000; // Formule YIQ
  };

  return getBrightness(hex) > 128 ? 'text-black' : 'text-white';
};
</script>