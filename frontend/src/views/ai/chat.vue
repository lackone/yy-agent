<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>AI智能助手</span>
        </div>
      </template>

      <div ref="listRef" style="height: 480px; overflow-y: auto; padding: 8px 8px;background-color: #f5f7fa;">
        <div v-for="(message, index) in messages" :key="index"
             :style="{
              display: 'flex',
              justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
              marginBottom: '8px'
            }"
             class="message-item">
          <div :style="{
            maxWidth:'70%',
            padding: '10px 12px',
            borderRadius: '8px',
            backgroundColor: message.role === 'user' ? '#e6f7ff' : '#fff',
            lineHeight: '1.6',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.06)'
          }">
            <div v-if="message.role === 'assistant' && message.status"
                 style="margin-bottom: 6px; font-size:12px; color: #909399;">
              {{ message.status }}
            </div>
            <div v-if="message.role === 'assistant' && message.steps?.length"
                 style="margin-bottom: 8px; font-size:12px; color: #909399;">
              <div v-for="(step, i) in message.steps" :key="i">{{ step }}</div>
            </div>
            <div v-html="parseMarkdown(message.content)"></div>
          </div>
        </div>
      </div>

      <div style="margin-top: 12px; display: flex; align-items: flex-end; gap: 8px">
        <el-input v-model="input" type="textarea" :rows="2" placeholder="请输入" clearable @keydown.enter.shift.stop
                  @keydown.enter.exact.prevent="sendMessageStream"></el-input>
        <el-button type="primary" @click="sendMessageStream" :loading="loading" size="large">发送</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import {ref, reactive, nextTick} from 'vue'
import {chatApi, chatStreamApi} from "@/api/ai.js";
import {marked} from "marked";
import DOMPurify from 'dompurify'
import {ElMessage} from "element-plus";

const parseMarkdown = (text) => {
  if (!text) {
    return ''
  }
  marked.setOptions({breaks: true})
  const rawHtml = marked.parse(text)
  return DOMPurify.sanitize(rawHtml)
}

const messages = ref([
  {
    'role': 'assistant',
    'content': '你好，我是 AI 智能助手，你可以向我提问怎么预约，取消，也可以说帮我预约明天下午的实验室，确认后我会帮你提交'
  }
])

const input = ref('')
const loading = ref(false)
const listRef = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    const elem = listRef.value
    if (elem) {
      elem.scrollTop = elem.scrollHeight
    }
  })
}

const sendMessageStream = async () => {
  const text = input.value.trim()
  if (!text || loading.value) {
    return
  }
  loading.value = true
  messages.value.push({
    'role': 'user',
    'content': text
  })
  input.value = ''
  scrollToBottom()

  // 模拟流式输出
  const assistant = reactive({
    role: 'assistant',
    content: '',
    status: '正在思考...',
    steps: []
  })
  messages.value.push(assistant)

  const history = messages.value
      .filter((item) => item.role === 'user' || item.role === 'assistant')
      .slice(0, -1)
      .map(({role, content}) => ({role, content}))

  try {
    await chatStreamApi({messages: history}, (evt) => {
      if (evt.type === 'status') {
        assistant.status = evt.message || '正在思考...'
      } else if (evt.type === 'tool_start') {
        const label = evt.label || evt.name || '工具'
        assistant.status = `正在${label}...`
        assistant.steps.push(`开始：${label}...`)
      } else if (evt.type === 'tool_end') {
        const label = evt.label || evt.name || '工具'
        assistant.status = `${label}完成`
        assistant.steps.push(`完成：${label}`)
        if (evt.preview) {
          assistant.steps.push(`结果：${evt.preview}`)
        }
      } else if (evt.type === 'token') {
        assistant.content += evt.content || ''
        assistant.status = ''
      } else if (evt.type === 'done') {
        assistant.status = ''
      } else if (evt.type === 'error') {
        assistant.status = ''
        if (!assistant.content) {
          assistant.content = evt.message || '请求失败'
        }
        ElMessage.error(evt.message || '请求失败')
      }
      scrollToBottom()
    })

  } catch (err) {
    assistant.status = ''
    if (!assistant.content) {
      assistant.content = err.message || '请求失败'
    }
    ElMessage.error(err.message || '请求失败')
  } finally {
    loading.value = false
    assistant.status = ''
    scrollToBottom()
  }
}

const sendMessage = async () => {
  const text = input.value.trim()
  if (!text || loading.value) {
    return
  }
  loading.value = true
  messages.value.push({
    'role': 'user',
    'content': text
  })
  input.value = ''
  scrollToBottom()
  try {
    const msg = messages.value.filter(
        (item) => item.role === 'user' || item.role === 'assistant'
    )
    const res = await chatApi({messages: msg})
    if (res.code === 200) {
      messages.value.push(res.data)
      scrollToBottom()
    } else {
      ElMessage.error(res.msg || '对话失败')
    }
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>
.card-header {
  font-size: 16px;
  font-weight: bold;
}
</style>