<!-- src/views/WhyLearningPython.vue -->
<template>
  <div>
    <!-- 頁面標題 -->
    <h1>Why Learning Python</h1>
    <p>
      Python 主是要抓取格式文件的資料，要做爬蟲，比如有些文件做在google docs上的話，就會用到Python。
      透過Python
      爬回來的資料，可以透過Python提供的「函式庫」，把資料轉為JSON格式。有了JSON檔後，就可以給JavaScript
      做使用。JavaScript 會把JSON資料轉成物件，再透過JavaScript
      去訪問這些物件，就可以做資料的展示與渲染。
    </p>

    <!-- 頁面標題 -->
    <h1>爬取 Google Docs 資料</h1>

    <!-- 使用者輸入文件 ID 的表單 -->
    <input v-model="docId" placeholder="請輸入文件 ID" />
    <button @click="fetchData">取得資料</button>

    <!-- 錯誤訊息區塊：當 error 不為空時顯示詳細錯誤資訊 -->
    <div v-if="error" class="error-box">
      <p>發生錯誤：</p>
      <!-- 使用 pre 來保留錯誤訊息的格式 -->
      <pre>{{ error }}</pre>
    </div>

    <!-- 顯示取得的文件資料 -->
    <div v-if="documentData">
      <!-- 文件標題 -->
      <h2>文件標題：{{ documentData.title }}</h2>
      <!-- 以 pre 格式顯示文件內容，方便閱讀原始資料（可依需求調整格式） -->
      <pre>{{ documentData.content }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
/*
  使用 Vue 3 的 <script setup> 與 TypeScript
  - ref 用來定義反應式變數
  - axios 用來發送 HTTP 請求
*/
import { ref } from 'vue'
import axios from 'axios'

// 定義反應式變數，用於儲存使用者輸入的文件 ID
const docId = ref('')
// 定義反應式變數，用於儲存後端回傳的文件資料
const documentData = ref<any>(null)
// 定義反應式變數，用來儲存錯誤訊息
const error = ref('')

// 定義 fetchData 函式，在使用者點擊「取得資料」按鈕時呼叫
const fetchData = async () => {
  // 清空前一次的錯誤與資料
  error.value = ''
  documentData.value = null
  try {
    // 發送 GET 請求到後端 API，並傳入文件 ID 作為查詢參數
    const response = await axios.get('http://127.0.0.1:5000/api/data', {
      params: { docId: docId.value },
    })
    // 將取得的資料存入 documentData 變數
    documentData.value = response.data
  } catch (err: any) {
    // 若發生錯誤，將詳細錯誤訊息轉成 JSON 字串顯示
    error.value = JSON.stringify(err.response?.data || err.message, null, 2)
    // 同時在瀏覽器控制台輸出錯誤資訊以便除錯
    console.error('Error fetching data:', err)
  }
}
</script>

<style scoped>
/* 輸入框與按鈕的基本樣式 */
input {
  padding: 0.5rem;
  margin-right: 0.5rem;
}
button {
  padding: 0.5rem;
}

/* 錯誤訊息區塊的樣式 */
.error-box {
  margin-top: 1rem;
  padding: 1rem;
  border: 1px solid red;
  background-color: #ffe6e6;
  color: red;
  white-space: pre-wrap;
}
</style>
