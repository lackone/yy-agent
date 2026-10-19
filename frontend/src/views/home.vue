<template>
  <div>
    <el-card shadow="never" style="margin-bottom: 15px;">
      <div style="display: flex; justify-content: space-between; align-items: center; gap: 16px">
        <div>
          <div style="font-size:20px;color: #303133">欢迎 {{ userInfo?.username }}</div>
          <div style="font-size:14px;color: #909399;margin-top: 5px;">欢迎使用预约系统</div>
        </div>
        <el-button type="primary" @click="router.push('/manager/chat')">打开AI助手</el-button>
      </div>
    </el-card>

    <el-card shadow="never" style="margin-bottom: 15px;">
      <div style="display: flex; align-items: center; gap: 32px;">
        <div>开放的实验室 <b style="margin-left: 10px; font-size: 18px;"> {{ labCount }}</b></div>
        <div>开放的设备 <b style="margin-left: 10px; font-size: 18px;"> {{ deviceCount }}</b></div>
      </div>
    </el-card>

    <div style="margin-bottom: 15px;">
      <div style="font-size: 20px;font-weight: bold;margin-bottom: 10px;">功能介绍</div>
      <el-row :gutter="16">
        <el-col v-for="(item, index) in features" :key="index" :span="8">
          <el-card shadow="never">
            <div style="padding: 10px">
              <div style="font-size: 16px; font-weight: bold; color: #303133;">{{ item.title }}</div>
              <div style="margin-top: 8px; color: #606266; font-size: 14px;">{{ item.desc }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div style="margin-bottom: 15px;">
      <div style="font-size: 20px;font-weight: bold;margin-bottom: 10px;">快捷入口</div>
      <el-row :gutter="16">
        <el-col v-for="(item, index) in shortcuts" :key="index" :span="8">
          <el-card shadow="never">
            <div style="padding: 10px">
              <div>
                <router-link style="color: #409eff;" :to="item.path">{{ item.label }}</router-link>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import {useUser} from "@/utils/user.js";
import router from "@/router/index.js";
import {computed, onMounted, ref} from "vue";
import {getLabList} from "@/api/lab.js";
import {getDeviceList} from "@/api/device.js";

const {userInfo} = useUser()
const labCount = ref(0)
const deviceCount = ref(0)

const features = [
  {
    title: '业务预约',
    desc: '实验室 / 设备浏览、提交预约，我的预约和管理员审核'
  },
  {
    title: '知识库问答',
    desc: 'RAG 检索规则和开放时间等文档，回答有依据'
  },
  {
    title: '智能Agent',
    desc: '根据用户输入的自然语言主动进行Tool Call和节点编排循环调用，可以查库，流式对话，确认表单提交'
  }
]

const shortcuts = computed(() => {
  const list = [
    {
      label: 'AI智能助手',
      path: '/manager/chat'
    },
    {
      label: '实验室列表',
      path: '/manager/lab_list'
    },
    {
      label: '我的预约',
      path: '/manager/my_reservation'
    },
  ]
  return list
})

onMounted(async () => {
  try {
    const res = await getLabList({page: 1, page_size: 1})
    if (res.code === 200) {
      labCount.value = res.data.total
    }
  } catch {
    labCount.value = 0
  }

  try {
    const res = await getDeviceList({page: 1, page_size: 1})
    if (res.code === 200) {
      deviceCount.value = res.data.total
    }
  } catch {
    deviceCount.value = 0
  }
})

</script>
