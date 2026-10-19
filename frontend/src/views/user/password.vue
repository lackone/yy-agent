<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>修改密码</span>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" style="width:100%">
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="form.old_password" show-password placeholder="旧密码"/>
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="form.new_password" show-password placeholder="新密码"/>
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirm_password">
          <el-input v-model="form.confirm_password" show-password placeholder="确认新密码"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="submitForm">提交</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>

import {reactive, ref} from "vue";
import {updatePassword} from "@/api/user.js";
import {ElMessage} from "element-plus";

const formRef = ref()
const submitting = ref(false)

const rules = {
  old_password: [{required: true, message: '请输入旧密码', trigger: 'blur'}],
  new_password: [{required: true, message: '请输入新密码', trigger: 'blur'}],
  confirm_password: [
    {required: true, message: '请输入确认新密码', trigger: 'blur'},
    {
      validator: (rule, value, callback) => {
        if (value !== form.new_password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      }, trigger: 'blur'
    }
  ],
}

const form = reactive({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  submitting.value = true
  try {
    const res = await updatePassword(form)
    if (res.code === 200) {
      ElMessage.success('更新成功')
    }
  } catch (error) {
    console.error(error)
  } finally {
    submitting.value = false
  }
}

</script>