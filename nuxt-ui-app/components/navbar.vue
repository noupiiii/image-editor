<template>
    <!-- Nav Desktop (inchangée, sauf suppression du v-if inutile sur le menu centré) -->
    <div class="backdrop-blur-lg z-50 py-3 fixed top-0 left-0 w-full border-b dark:border-gray-700" v-if="!isMobile">
        <UContainer class="flex justify-between items-center">

            <!-- Logo et auteur -->
            <ul class="flex gap-2 items-center">
                <li>
                    <ULink to="/">
                        <h1 class="text-xl font-semibold">ImageEditor</h1>
                    </ULink>
                </li>
                <li>
                    <ULink to="https://github.com/noupiiii" target="_blank">
                        <UBadge label="by noupiiii" variant="subtle" />
                    </ULink>
                </li>
            </ul>
            
            <!-- Menu centré -->
            <ul class="flex gap-3 absolute left-1/2 transform -translate-x-1/2">
                <li>
                    <ULink active-class="text-primary" to="/">
                        Tools
                    </ULink>
                </li>
                <li>
                    <ULink active-class="text-primary" to="/code">
                        Code
                    </ULink>
                </li>
            </ul>
            
            <!-- Thème -->
            <ul>
                <ThemeSelector />
            </ul>
        </UContainer>
    </div>

    <!-- Nav Mobile -->
    <div v-else>
        <div class="backdrop-blur-lg py-3 fixed top-0 left-0 w-full border-b dark:border-gray-700">
            <UContainer class="flex justify-between items-center">
                <ul class="flex gap-2 items-center">
                    <li>
                        <ULink to="/">
                            <h1 class="text-xl font-semibold">ImageEditor</h1>
                        </ULink>
                    </li>
                    <li>
                        <ULink to="https://github.com/noupiiii" target="_blank">
                            <UBadge label="by noupiiii" variant="subtle" />
                        </ULink>
                    </li>
                </ul>
                <!-- Bouton pour afficher / masquer le menu -->
                 <div class="flex justify-between items-center gap-2">
                     <ThemeSelector />
                     <UButton icon="i-heroicons-list-bullet" variant="ghost" @click="toggleMenu" />
                    </div>
            </UContainer>
        </div>
        
        <!-- Menu mobile plein écran -->
        <transition name="fade" class="backdrop-blur-lg bg-transparent">
            <ul 
                @click="toggleMenu"
              v-if="showMenu" 
              class="fixed top-0 left-0 w-screen h-screen border-t dark:border-gray-700 py-2 flex flex-col items-center justify-center"
            >
                <li class="w-full py-2 text-2xl hover:text-primary-400 text-center transition">
                    <ULink active-class="text-primary" to="/">
                        Tools
                    </ULink>
                </li>
                <li class="w-full py-2 text-2xl hover:text-primary-400 text-center transition">
                    <ULink active-class="text-primary" to="/code">
                        Code
                    </ULink>
                </li>
            </ul>
        </transition>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const isMobile = ref(false)
const showMenu = ref(false)

function checkIsMobile() {
  isMobile.value = window.innerWidth <= 768
}

function toggleMenu() {
  showMenu.value = !showMenu.value
}

onMounted(() => {
  checkIsMobile()
  window.addEventListener('resize', checkIsMobile)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkIsMobile)
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
