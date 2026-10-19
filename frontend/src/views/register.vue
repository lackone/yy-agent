<template>
  <div class="register-container">
    <div class="register-box">
      <h1 style="text-align: center; font-size: 24px;">实验室预约系统</h1>
      <div style="text-align: center; margin-top: 5px; margin-bottom: 30px">基于 AI Agent智能预约系统</div>

      <el-form ref="formRef" :rules="rules" :model="form" label-width="0px" style="width: 100%">
        <el-form-item prop="account">
          <el-input v-model="form.account" placeholder="输入账号" prefix-icon="User" size="large"/>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" show-password v-model="form.password" placeholder="输入密码" :prefix-icon="Lock"
                    size="large"/>
        </el-form-item>
        <el-form-item prop="repassword">
          <el-input type="password" show-password v-model="form.repassword" placeholder="确认密码" :prefix-icon="Lock"
                    size="large"/>
        </el-form-item>
        <div>
          <el-button type="primary" style="width: 100%" size="large" @click="registerBtn" :loading="loadingValue">注册
          </el-button>
          <div style="text-align: right; margin-top: 20px">已有账号？请
            <router-link style="color: var(--el-color-primary)"
                         to="/login">登录
            </router-link>
          </div>
        </div>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-box {
  width: 380px;
  border-radius: 8px;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
  background-color: #fff;
}
</style>

<script setup>
import {reactive, ref} from 'vue'
import {User, Lock} from '@element-plus/icons-vue'
import {registerApi} from "@/api/auth.js";
import {ElMessage} from "element-plus";
import router from "@/router/index.js";
// do not use same name with ref

const formRef = ref()

const form = reactive({
  account: '',
  password: '',
  repassword: '',
})

const loadingValue = ref(false)

const rules = {
  account: [{required: true, message: '请输入账号', trigger: 'blur'}],
  password: [{required: true, message: '请输入密码', trigger: 'blur'}],
  repassword: [
    {required: true, message: '请确认密码', trigger: 'blur'},
    {
      validator: (rule, value, callback) => {
        if (value !== form.password) {
          callback(new Error('两次密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
}

const registerBtn = async () => {
  // 校验表单
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  loadingValue.value = true
  try {
    const res = await registerApi(form)
    if (res.code === 200) {
      ElMessage.success("注册成功")
      await router.push("/login")
    } else {
      ElMessage.error(res.msg)
    }
  } finally {
    loadingValue.value = false
  }
}
</script>