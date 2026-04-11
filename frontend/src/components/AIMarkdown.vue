<script setup lang="ts">
import { computed } from "vue";
import markdownit from "markdown-it";
import hljs from "highlight.js";
import DOMPurify from "dompurify";

// 自定义代码块渲染
const md = markdownit({
  highlight: (str, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${
          hljs.highlight(str, { language: lang }).value
        }</code></pre>`;
      } catch {}
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
  },
});

// 支持数学公式
// import markdownItKatex from "markdown-it-katex";
// md.use(markdownItKatex);

const props = defineProps<{
  content: string;
}>();

const html = computed(() => {
  const rendered = md.render(props.content);
  return DOMPurify.sanitize(rendered, {
    ADD_TAGS: ["iframe"],
    ADD_ATTR: ["src", "allow", "allowfullscreen"],
  });
});
</script>

<template>
  <div class="ai-markdown" v-html="html" />
</template>

<style scoped>
.ai-markdown {
  :deep(pre) {
    background: #1e1e1e;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
  }

  :deep(code) {
    font-family: "JetBrains Mono", monospace;
    font-size: 14px;
  }

  :deep(table) {
    border-collapse: collapse;
    width: 100%;
  }

  :deep(th),
  :deep(td) {
    border: 1px solid #ddd;
    padding: 8px;
  }
}
</style>

<style>
@import "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css";
</style>
