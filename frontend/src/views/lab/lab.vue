<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>实验室管理</span>
        </div>
      </template>
      <div style="margin-bottom: 10px;">
        <el-input v-model="params.keyword" placeholder="请输入实验室名称" @keyup.enter="search" clearable
                  @clear="search"
                  style="width: 180px; margin-right: 10px;"></el-input>
        <el-button type="primary" :icon="Search" @click="search">查询</el-button>
        <el-button type="success" :icon="Plus" @click="createLabBtn">创建实验室</el-button>
      </div>

      <el-table :data="tableData" :header-cell-style="{background: '#f5f7fa', color: '#303133'}" style="width: 100%"
                v-loading="loading">
        <el-table-column prop="id" label="ID" width="180"></el-table-column>
        <el-table-column prop="name" label="实验室名称"></el-table-column>
        <el-table-column prop="image" label="实验室图片">
          <template #default="{ row }">
            <el-image v-if="row.image" :src="row.image" fit="fill"
                      style="width: 50px; height: 50px; border-radius: 50%;"></el-image>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="实验室位置"></el-table-column>
        <el-table-column prop="capacity" label="实验室容量"></el-table-column>
        <el-table-column prop="open_time" label="实验室开放时间"></el-table-column>
        <el-table-column prop="close_time" label="实验室关闭时间"></el-table-column>
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
            <el-button type="primary" text bg @click="editLabBtn(row)">编辑</el-button>
            <el-button type="danger" text bg @click="deleteLabBtn(row)">删除</el-button>
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

    <el-dialog v-model="labFormVisible" :title="form.id ? '编辑实验室' : '创建实验室'" width="800">
      <el-form :model="form" :rules="rules" ref="formRef" v-loading="loading" label-width="100px" style="width:100%">
        <el-form-item label="实验室名称" prop="name">
          <el-input v-model="form.name" placeholder="实验室名称"/>
        </el-form-item>
        <el-form-item label="实验室描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入描述"/>
        </el-form-item>
        <el-form-item label="实验室图片" prop="image">
          <el-upload
              class="avatar-uploader"
              :http-request="imageUpload"
              :show-file-list="false"
              accept="image/jpeg,image/png,image/gif,image/jpg,image/webp"
              :before-upload="beforeImageUpload"
          >
            <img v-if="form.image" :src="form.image" class="avatar"/>
            <el-icon v-else class="avatar-uploader-icon">
              <Plus/>
            </el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="实验室位置" prop="location">
          <el-input v-model="form.location" placeholder="请输入位置"/>
        </el-form-item>
        <el-form-item label="实验室容量" prop="capacity">
          <el-input-number v-model="form.capacity" :min="1" :max="99999" placeholder="请输入容量"/>
        </el-form-item>
        <el-form-item label="开放时间" prop="open_time">
          <el-time-picker v-model="form.open_time" type="time" format="HH:mm"
                          value-format="HH:mm" placeholder="请输入开放时间"/>
        </el-form-item>
        <el-form-item label="关闭时间" prop="close_time">
          <el-time-picker v-model="form.close_time" type="time" format="HH:mm"
                          value-format="HH:mm" placeholder="请输入关闭时间"/>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :label="1">正常</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="labFormVisible = false">取消</el-button>
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
import {createLab, deleteLab, getLabList, updateLab} from "@/api/lab.js";
import {Search, Plus} from "@element-plus/icons-vue"
import {ElMessage, ElMessageBox} from "element-plus";
import {uploadFile} from "@/api/upload.js";

const form = reactive({
  id: null,
  name: '',
  description: '',
  image: '',
  location: '',
  capacity: '',
  open_time: '09:00',
  close_time: '18:00',
  status: 1,
})

const params = reactive({
  keyword: "",
  page: 1,
  page_size: 10,
})

const rules = {
  name: [{required: true, message: '请输入实验室名称', trigger: 'blur'}],
}

const formRef = ref()
const labFormVisible = ref(false);
const loading = ref(false);
const formLoading = ref(false);
const tableData = ref([]);
const total = ref(0);

const resetForm = () => {
  Object.assign(form, {
    id: null,
    name: '',
    description: '',
    image: '',
    location: '',
    capacity: '',
    open_time: '09:00',
    close_time: '18:00',
    status: 1,
  })
}

const createLabBtn = async () => {
  resetForm()
  labFormVisible.value = true
}

const editLabBtn = async (row) => {
  resetForm()
  Object.assign(form, row)
  labFormVisible.value = true
}

const deleteLabBtn = async (row) => {
  ElMessageBox.confirm(`确认删除实验室 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    const res = await deleteLab(row.id)
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
    const res = form.id ? await updateLab(form.id, form) : await createLab(form)
    if (res.code === 200) {
      ElMessage.success('操作成功')
      labFormVisible.value = false
      load()
    }
  } finally {
    formLoading.value = false
  }
}

const load = async () => {
  loading.value = true;
  try {
    const res = await getLabList(params);
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

const imageUpload = async (option) => {
  try {
    const res = await uploadFile(option.file)
    if (res.code === 200) {
      form.image = res.data?.url
    }
  } catch (error) {
    console.error(error)
  }
}

const beforeImageUpload = (rawFile) => {
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

onMounted(() => {
  load();
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