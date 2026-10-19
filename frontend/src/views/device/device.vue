<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>设备管理</span>
        </div>
      </template>
      <div style="margin-bottom: 10px;">
        <el-input v-model="params.keyword" placeholder="请输入设备名称" @keyup.enter="search" clearable
                  @clear="search"
                  style="width: 180px; margin-right: 10px;"></el-input>
        <el-select style="width: 180px; margin-right: 10px;" v-model="params.lab_id" placeholder="请选择实验室"
                   @change="search" clearable
                   @clear="search">
          <el-option v-for="item in labOptions" :key="item.id" :value="item.id" :label="item.name"></el-option>
        </el-select>
        <el-button type="primary" :icon="Search" @click="search">查询</el-button>
        <el-button type="success" :icon="Plus" @click="createDeviceBtn">创建设备</el-button>
      </div>

      <el-table :data="tableData" :header-cell-style="{background: '#f5f7fa', color: '#303133'}" style="width: 100%"
                v-loading="loading">
        <el-table-column prop="id" label="ID" width="180"></el-table-column>
        <el-table-column prop="name" label="设备名称"></el-table-column>
        <el-table-column prop="image" label="设备图片">
          <template #default="{ row }">
            <el-image v-if="row.image" :src="row.image" fit="fill"
                      style="width: 50px; height: 50px; border-radius: 50%;"></el-image>
          </template>
        </el-table-column>
        <el-table-column prop="spec" label="设备规格"></el-table-column>
        <el-table-column prop="quantity" label="设备数量"></el-table-column>
        <el-table-column prop="lab_name" label="所属实验室"></el-table-column>
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
            <el-button type="primary" text bg @click="editDeviceBtn(row)">编辑</el-button>
            <el-button type="danger" text bg @click="deleteDeviceBtn(row)">删除</el-button>
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

    <el-dialog v-model="deviceFormVisible" :title="form.id ? '编辑设备' : '创建设备'" width="800">
      <el-form :model="form" :rules="rules" ref="formRef" v-loading="loading" label-width="100px" style="width:100%">
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="form.name" placeholder="设备名称"/>
        </el-form-item>
        <el-form-item label="设备描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入描述"/>
        </el-form-item>
        <el-form-item label="设备图片" prop="image">
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
        <el-form-item label="设备规格" prop="spec">
          <el-input v-model="form.spec" placeholder="请输入规格"/>
        </el-form-item>
        <el-form-item label="设备数量" prop="quantity">
          <el-input-number v-model="form.quantity" :min="1" :max="99999" placeholder="请输入数量"/>
        </el-form-item>
        <el-form-item label="所属实验室" prop="lab_id">
          <el-select v-model="form.lab_id" placeholder="请选择实验室">
            <el-option v-for="item in labOptions" :key="item.id" :value="item.id" :label="item.name"></el-option>
          </el-select>
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
          <el-button @click="deviceFormVisible = false">取消</el-button>
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
import {createDevice, deleteDevice, getDeviceList, updateDevice} from "@/api/device.js";
import {Search, Plus} from "@element-plus/icons-vue"
import {ElMessage, ElMessageBox} from "element-plus";
import {uploadFile} from "@/api/upload.js";
import {getLabList} from "@/api/lab.js";

const form = reactive({
  id: null,
  name: '',
  description: '',
  image: '',
  spec: '',
  quantity: 0,
  lab_id: null,
  status: 1,
})

const params = reactive({
  keyword: "",
  lab_id: null,
  page: 1,
  page_size: 10,
})

const rules = {
  name: [{required: true, message: '请输入设备名称', trigger: 'blur'}],
}

const formRef = ref()
const deviceFormVisible = ref(false);
const loading = ref(false);
const formLoading = ref(false);
const tableData = ref([]);
const total = ref(0);
const labOptions = ref([]);

const resetForm = () => {
  Object.assign(form, {
    id: null,
    name: '',
    description: '',
    image: '',
    spec: '',
    quantity: 0,
    lab_id: null,
    status: 1,
  })
}

const createDeviceBtn = async () => {
  resetForm()
  deviceFormVisible.value = true
}

const editDeviceBtn = async (row) => {
  resetForm()
  Object.assign(form, row)
  deviceFormVisible.value = true
}

const deleteDeviceBtn = async (row) => {
  ElMessageBox.confirm(`确认删除设备 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    const res = await deleteDevice(row.id)
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
    const res = form.id ? await updateDevice(form.id, form) : await createDevice(form)
    if (res.code === 200) {
      ElMessage.success('操作成功')
      deviceFormVisible.value = false
      load()
    }
  } finally {
    formLoading.value = false
  }
}

const load = async () => {
  loading.value = true;
  try {
    const res = await getDeviceList(params);
    if (res.code == 200) {
      tableData.value = res.data?.list || [];
      total.value = res.data?.total || 0;
    }
  } finally {
    loading.value = false;
  }
}

const loadLabOptions = async () => {
  const res = await getLabList({
    page: 1,
    page_size: 1000,
  })
  if (res.code === 200) {
    labOptions.value = res.data?.list || []
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
  loadLabOptions()
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