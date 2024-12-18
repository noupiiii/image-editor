<template>
    <div>
        <h1
      class="text-6xl w-fit font-bold"
    >
      Remove Background
    </h1>
    <p>Upload an image to remove its background.</p>
    <FileInput @file-selected="handleFileSelected" />
    </div>
</template>

<script setup>
const fileInfo = ref(null)

const handleFileSelected = (fileData) => {
    fileInfo.value = fileData
}
</script>