<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>个人信息</span>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" v-loading="loading" label-width="100px" style="width:100%">
        <el-form-item label="头像" prop="avatar">
          <el-upload
              class="avatar-uploader"
              :http-request="avatarUpload"
              :show-file-list="false"
              accept="image/jpeg,image/png,image/gif,image/jpg,image/webp"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
          >
            <img v-if="form.avatar" :src="form.avatar" class="avatar"/>
            <el-icon v-else class="avatar-uploader-icon">
              <Plus/>
            </el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="账号" prop="account">
          <el-input v-model="form.account" placeholder="账号" disabled/>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名"/>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱"/>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="submitForm">提交</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import {onMounted, reactive, ref} from 'vue'
import {getUserInfo, updateUserInfo} from "@/api/user.js";
import {ElMessage} from "element-plus";
import {useUser} from "@/utils/user.js";
import {uploadFile} from "@/api/upload.js";

const {updateUser} = useUser()

const formRef = ref()
const loading = ref(false)
const submitting = ref(false)

const rules = {
  username: [{required: true, message: '请输入用户名', trigger: 'blur'}],
  email: [{type: 'email', message: '请输入正确的邮箱', trigger: 'blur'}],
  phone: [
    {pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur'},
  ],
}

const form = reactive({
  account: '',
  username: '',
  email: '',
  phone: '',
  avatar: '',
})

const avatarUpload = async (option) => {
  try {
    const res = await uploadFile(option.file)
    if (res.code === 200) {
      form.avatar = res.data?.url
    }
  } catch (error) {
    console.error(error)
  }
}

const handleAvatarSuccess = (response, uploadFile) => {
  // form.avatar = URL.createObjectURL(uploadFile.raw)
  console.log(uploadFile)
}

const beforeAvatarUpload = (rawFile) => {
  const imageTypes = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/jpg',
    'image/webp',
  ]
  if (!imageTypes.includes(rawFile.type)) {
    ElMessage.error('请上传 JPG, PNG, GIF, JPG, WEBP 格式的图片!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

const loadUserInfo = async () => {
  loading.value = true
  try {
    const res = await getUserInfo()
    if (res.code === 200) {
      Object.assign(form, res.data)
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  submitting.value = true
  try {
    const res = await updateUserInfo(form)
    if (res.code === 200) {
      updateUser(res.data)
      ElMessage.success('更新成功')
    }
  } catch (error) {
    console.error(error)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadUserInfo()
})

</script>

<style scoped>
.card-header {
  font-size: 16px;
  font-weight: bold;
}

.avatar-uploader .avatar {
  width: 120px;
  height: 120px;
  display: block;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  text-align: center;
}
</style>