<template>
    <div class="my-12">
        <h1 class="my-6 font-semibold text-5xl">
            Edit your images as you wish
        </h1>
        <p class="mb-12">This project is under development and may contain bugs.</p>
        <div class="flex gap-2 my-4 mb-12">
            <UButton variant="outline" label="Explore tools" @click=goToToolsSection() />
            <UButton to="/code" variant="outline" color="black" label="About the code" />
        </div>
        <div id="toolsSection">
            <UCard class="mb-4">
                <h1 class="text-lg text-primary-500">Color palette</h1>
                <p>Get an image's color palette.</p>
                <UButton label="Use this tool" variant="outline" to="/color-palette" class="mt-2" />
            </UCard>
            <UCard class="mb-4">
                <h1 class="text-lg text-primary-500">Remove background</h1>
                <p>Remove background from an image.</p>
                <UButton label="Use this tool" variant="outline" to="/remove-background" class="mt-2" />
            </UCard>
            <UCard class="mb-4">
                <h1 class="text-lg text-primary-500">Transfert colors</h1>
                <p>Transfert colors.</p>
                <UButton label="Use this tool" variant="outline" to="/transfert-colors" class="mt-2" />
            </UCard>
        </div>
    </div>
</template>

<script setup>
const goToToolsSection = () => {
    const section = document.getElementById('toolsSection');
    if (section) {
        section.scrollIntoView({behavior: 'smooth'})
    }
}
</script>