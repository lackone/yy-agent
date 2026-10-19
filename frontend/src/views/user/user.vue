<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
        </div>
      </template>
      <div style="margin-bottom: 10px;">
        <el-input v-model="params.keyword" placeholder="请输入用户名" @keyup.enter="search" clearable @clear="search"
                  style="width: 180px; margin-right: 10px;"></el-input>
        <el-button type="primary" :icon="Search" @click="search">查询</el-button>
        <el-button type="success" :icon="Plus" @click="createUserBtn">创建用户</el-button>
      </div>

      <el-table :data="tableData" :header-cell-style="{background: '#f5f7fa', color: '#303133'}" style="width: 100%"
                v-loading="loading">
        <el-table-column prop="id" label="ID" width="180"></el-table-column>
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="avatar" label="头像">
          <template #default="{ row }">
            <el-image v-if="row.avatar" :src="row.avatar" fit="fill"
                      style="width: 50px; height: 50px; border-radius: 50%;"></el-image>
          </template>
        </el-table-column>
        <el-table-column prop="account" label="账号"></el-table-column>
        <el-table-column prop="email" label="邮箱"></el-table-column>
        <el-table-column prop="phone" label="手机号"></el-table-column>
        <el-table-column prop="is_super" label="是否超级用户">
          <template #default="{ row }">
            <el-tag v-if="row.is_super == 1" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag v-if="row.status == 1" type="success">正常</el-tag>
            <el-tag v-else type="danger">禁用</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created" label="创建时间"></el-table-column>
        <el-table-column prop="updated" label="更新时间"></el-table-column>
        <el-table-column prop="id" label="操作">
          <template #default="{ row }">
            <el-button type="primary" text bg @click="editUserBtn(row)">编辑</el-button>
            <el-button type="danger" text bg @click="deleteUserBtn(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top: 10px; display: flex; justify-content: flex-end">
        <el-pagination
            background
            @current-change="load"
            v-model:current-page="params.page"
            v-model:page-size="params.page_size"
            layout="prev, pager, next, total"
            :total="total"/>
      </div>
    </el-card>

    <el-dialog v-model="userFormVisible" :title="form.id ? '编辑用户' : '创建用户'" width="800">
      <el-form :model="form" :rules="rules" ref="formRef" v-loading="loading" label-width="100px" style="width:100%">
        <el-form-item label="账号" prop="account">
          <el-input v-model="form.account" :disabled="!!form.id" placeholder="账号" disabled/>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="请输入密码"/>
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
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :label="1">正常</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="是否超级用户" prop="is_super">
          <el-radio-group v-model="form.is_super">
            <el-radio :label="1">是</el-radio>
            <el-radio :label="0">否</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="userFormVisible = false">取消</el-button>
          <el-button type="primary" :loading="formLoading" @click="submitForm">
            提交
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {reactive, ref, onMounted} from "vue";
import {createUser, deleteUser, getUserList, updateUser} from "@/api/user.js";
import {Search, Plus} from "@element-plus/icons-vue"
import {ElMessage, ElMessageBox} from "element-plus";

const form = reactive({
  id: null,
  account: '',
  username: '',
  password: '',
  email: '',
  phone: '',
  avatar: '',
  status: 1,
  is_super: 0,
})

const params = reactive({
  keyword: "",
  page: 1,
  page_size: 10,
})

const rules = {
  account: [{required: true, message: '请输入账号', trigger: 'blur'}],
  password: [{required: true, message: '请输入密码', trigger: 'blur'}],
  username: [{required: true, message: '请输入用户名', trigger: 'blur'}],
  email: [{type: 'email', message: '请输入正确的邮箱', trigger: 'blur'}],
  phone: [
    {pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur'},
  ],
}

const formRef = ref()
const userFormVisible = ref(false);
const loading = ref(false);
const formLoading = ref(false);
const tableData = ref([]);
const total = ref(0);

const resetForm = () => {
  Object.assign(form, {
    id: null,
    account: '',
    username: '',
    password: '',
    email: '',
    phone: '',
    avatar: '',
    status: 1,
    is_super: 0,
  })
}

const createUserBtn = async () => {
  resetForm()
  userFormVisible.value = true
}

const editUserBtn = async (row) => {
  resetForm()
  Object.assign(form, row)
  userFormVisible.value = true
}

const deleteUserBtn = async (row) => {
  ElMessageBox.confirm(`确认删除用户 ${row.username} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    const res = await deleteUser(row.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      load()
    }
  })
}

const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  formLoading.value = true
  try {
    const res = form.id ? await updateUser(form.id, form) : await createUser(form)
    if (res.code === 200) {
      ElMessage.success('操作成功')
      userFormVisible.value = false
      load()
    }
  } finally {
    formLoading.value = false
  }
}

const load = async () => {
  loading.value = true;
  try {
    const res = await getUserList(params);
    if (res.code == 200) {
      tableData.value = res.data?.list || [];
      total.value = res.data?.total || 0;
    }
  } finally {
    loading.value = false;
  }
}

const search = async () => {
  params.page = 1;
  load();
}

onMounted(() => {
  load();
})

</script>

<style scoped>
.card-header {
  font-size: 16px;
  font-weight: bold;
}
</style>