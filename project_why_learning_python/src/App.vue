<!-- src/App.vue -->
<!-- 使用 Vue 3 的 <script setup> 語法，並指定 lang="ts" 表示使用 TypeScript -->
<script setup lang="ts">
// 從 vue-router 中引入兩個組件：
// RouterLink：用來建立可點擊的連結，對應到路由設定
// RouterView：作為路由渲染的容器，會根據當前路由顯示對應的組件
import { RouterLink, RouterView } from 'vue-router'

// 引入自訂組件 HelloWorld，這個組件通常用來顯示歡迎訊息或範例內容
import HelloWorld from './components/HelloWorld.vue'
</script>

<!-- 定義組件的模板 -->
<template>
  <!-- header 區塊，通常放置網站的標誌與導覽連結 -->
  <header>
    <!-- 透過 img 顯示 logo 圖片
         src 使用 @/assets/logo.svg，@ 通常代表 src 目錄，
         設定寬度與高度來控制圖片尺寸 -->
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <!-- 包含其他內容的容器 -->
    <div class="wrapper">
      <!-- 使用 HelloWorld 組件，並透過 msg 屬性傳入訊息 -->
      <HelloWorld msg="You did it!" />

      <!-- 導覽區塊，利用 vue-router 的 RouterLink 建立路由連結 -->
      <nav>
        <!-- 連結到首頁 (路徑 "/" ) -->
        <RouterLink to="/">Home</RouterLink>

        <!-- 新增的 RouterLink，點擊後會導向 /why-learning-python 路由 -->
        <RouterLink to="/why-learning-python">Why Learning Python</RouterLink>

        <!-- 連結到關於頁 (路徑 "/about" ) -->
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <!-- RouterView 作為路由展示容器，根據當前路由顯示對應的組件 -->
  <RouterView />
</template>

<!-- scoped 樣式，僅作用於此組件 -->
<style scoped>
/* header 樣式：設定行高與最大高度 */
header {
  line-height: 1.5;
  max-height: 100vh;
}

/* .logo 類別：設定圖片為區塊元素，置中顯示並加入底部外距 */
.logo {
  display: block;
  margin: 0 auto 2rem;
}

/* nav 樣式：設定寬度、字型大小、文字置中與上方外距 */
nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

/* 當連結處於激活狀態 (當前路由) 時，變更文字顏色 */
nav a.router-link-exact-active {
  color: var(--color-text);
}

/* 當激活狀態下連結被滑鼠懸停時，背景保持透明 */
nav a.router-link-exact-active:hover {
  background-color: transparent;
}

/* nav 中的連結：設定為 inline-block、左右內距，以及左邊邊框 */
nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

/* 第一個連結移除左邊邊框 */
nav a:first-of-type {
  border: 0;
}

/* Media Query：針對螢幕寬度至少 1024px 的設備 */
@media (min-width: 1024px) {
  /* header 調整為 Flex 排版，使內容垂直置中 */
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  /* 調整 .logo 在大螢幕下的外距 */
  .logo {
    margin: 0 2rem 0 0;
  }

  /* header 中的 wrapper 區塊，設定為 Flex 排版，對齊方式為上對齊，並支援換行 */
  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  /* 調整 nav 的樣式：左對齊、調整內外距與字型大小 */
  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;
    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
