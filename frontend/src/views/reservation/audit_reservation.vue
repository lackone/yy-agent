<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>预约审核</span>
        </div>
      </template>
      <div style="margin-bottom: 10px;">
        <el-select style="width: 180px; margin-right: 10px;" v-model="params.status" placeholder="请选择状态"
                   @change="search" clearable
                   @clear="search">
          <el-option v-for="(name, id) in statusList" :key="id" :value="Number(id)" :label="name"></el-option>
        </el-select>
        <el-button type="primary" :icon="Search" @click="search">查询</el-button>
      </div>

      <el-table :data="tableData" :header-cell-style="{background: '#f5f7fa', color: '#303133'}" style="width: 100%"
                v-loading="loading">
        <el-table-column prop="id" label="ID" width="180"></el-table-column>
        <el-table-column prop="user_name" label="预约人"></el-table-column>
        <el-table-column prop="lab_name" label="实验室名称"></el-table-column>
        <el-table-column prop="device_name" label="设备名称"></el-table-column>
        <el-table-column prop="type" label="预约类型">
          <template #default="{ row }">
            <el-tag :type="row.type === '实验室' ? 'success' : 'primary'">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="预约日期"></el-table-column>
        <el-table-column label="预约时间">
          <template #default="{ row }">
            {{ row.start_time }} - {{ row.end_time }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注"></el-table-column>
        <el-table-column prop="created" label="创建时间"></el-table-column>
        <el-table-column prop="updated" label="更新时间"></el-table-column>
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button v-if="row.status === 0" type="danger" text bg @click="auditReservationBtn(row, -1)">拒绝</el-button>
            <el-button v-if="row.status === 0" type="success" text bg @click="auditReservationBtn(row, 1)">通过</el-button>
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
  </div>
</template>

<script setup>
import {onMounted, reactive, ref} from "vue";
import {auditReservation, cancelReservation, getReservationList} from "@/api/reservation.js";
import {ElMessage, ElMessageBox} from "element-plus";
import {Plus, Search} from "@element-plus/icons-vue";

const statusType = (status) => {
  return {
    0: 'warning',
    1: 'success',
    '-1': 'danger',
    '-2': 'info',
  }[status] || 'info'
}

const statusList = {
  0: '待审核',
  1: '已通过',
  '-1': '已拒绝',
  '-2': '已取消',
};

const statusText = (status) => {
  return statusList[status] || '未知状态'
}

const params = reactive({
  status: null,
  page: 1,
  page_size: 10,
})

const tableData = ref([]);
const total = ref(0);
const loading = ref(false);

const load = async () => {
  loading.value = true;
  try {
    const res = await getReservationList(params);
    if (res.code == 200) {
      tableData.value = res.data?.list || [];
      total.value = res.data?.total || 0;
    }
  } finally {
    loading.value = false;
  }
}

const auditReservationBtn = async (row, status) => {
  ElMessageBox.confirm(`确认${status === -1 ? '拒绝' : '通过'}预约 ${row.id} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    const res = await auditReservation(row.id, status)
    if (res.code === 200) {
      ElMessage.success(status === -1 ? '拒绝成功' : '通过成功')
      load()
    }
  })
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