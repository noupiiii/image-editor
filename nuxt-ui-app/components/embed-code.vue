<template>
    <div>
      <pre>
        <code v-html="highlightedCode" class="hljs"></code>
      </pre>
    </div>
  </template>
  
  <script setup>
  import hljs from 'highlight.js/lib/core'
  import python from 'highlight.js/lib/languages/python'
  
  const { codeSnippet } = defineProps({
    codeSnippet: String
  })
  
  hljs.registerLanguage('python', python)
  
  const highlightedCode = hljs.highlight(codeSnippet, { language: 'python' }).value
  </script>
  
  <style lang="postcss">
  /* Tailwind-based highlight styling */
  .hljs {
    @apply block p-4 rounded-md overflow-x-auto 
      bg-gray-100 text-gray-800 
      dark:bg-gray-800 dark:text-gray-200;
  }
  
  .hljs-keyword, .hljs-name { @apply text-purple-600 dark:text-purple-400; }
  .hljs-string, .hljs-title, .hljs-section { @apply text-green-600 dark:text-green-400; }
  .hljs-number, .hljs-literal { @apply text-blue-600 dark:text-blue-400; }
  .hljs-comment { @apply text-gray-500 dark:text-gray-400 italic; }
  .hljs-function .hljs-title { @apply text-indigo-600 dark:text-indigo-400 font-semibold; }
  .hljs-built_in { @apply text-pink-600 dark:text-pink-400; }
  </style>
  