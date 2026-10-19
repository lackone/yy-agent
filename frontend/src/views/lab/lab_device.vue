<template>
  <div>
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="font-size: 16px; font-weight: bold">
            <span>{{ lab?.name || "-" }} 实验室设备列表</span>
          </div>
          <div>
            <el-button type="primary" @click="reserveLab">预约实验室</el-button>
            <el-button @click="router.push('/manager/lab_list')">返回实验室列表</el-button>
          </div>
        </div>
      </template>

      <div v-if="lab" style="color: #606266; margin-bottom: 10px; background-color: #f5f7fa; padding: 10px; border-radius: 5px;">
        <div>
          简介: {{ lab.description || '无' }}
        </div>
        <div>
          位置: {{ lab.location || '无' }} |
          容量: {{ lab.capacity || '无' }} |
          开放时间: {{ lab.open_time || '无' }} |
          关闭时间: {{ lab.close_time || '无' }}
        </div>
      </div>

      <div style="margin-bottom: 10px;">
        <el-input v-model="params.keyword" placeholder="请输入设备名称" @keyup.enter="search" clearable
                  @clear="search"
                  style="width: 180px; margin-right: 10px;"></el-input>
        <el-button type="primary" :icon="Search" @click="search">查询</el-button>
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
            <el-button type="primary" text bg :disabled="row.status != 1" @click="reserveDevice(row)">预约</el-button>
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

    <reserve-dialog v-model:visible="reserveVisible" :lab-id="lab?.id" :lab-name="lab?.name" :device-id="currentDevice?.id" :device-name="currentDevice?.name"></reserve-dialog>
  </div>
</template>

<script setup>

import {onMounted, reactive, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {getDeviceList} from "@/api/device.js";
import {getLab} from "@/api/lab.js";
import reserveDialog from "@/components/reserve_dialog.vue";
import {Search} from "@element-plus/icons-vue";

const reserveVisible = ref(false);
const currentDevice = ref(null);

const route = useRoute();
const router = useRouter();

const params = reactive({
  keyword: "",
  page: 1,
  page_size: 10,
  lab_id: Number(route.query.lab_id),
})

const tableData = ref([]);
const total = ref(0);
const loading = ref(false);
const lab = ref({});

const reserveLab = async () => {
  currentDevice.value = null;
  reserveVisible.value = true;
}

const reserveDevice = async (row) => {
  currentDevice.value = row;
  reserveVisible.value = true;
}

const loadLab = async () => {
  if (!params.lab_id) {
    return;
  }
  const res = await getLab(params.lab_id);
  if (res.code == 200) {
    lab.value = res.data || {};
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

const search = async () => {
  params.page = 1;
  load();
}

onMounted(() => {
  load();
  loadLab();
})

</script>