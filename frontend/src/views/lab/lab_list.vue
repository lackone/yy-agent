<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>实验室列表</span>
        </div>
      </template>
      <div style="margin-bottom: 10px;">
        <el-input v-model="params.keyword" placeholder="请输入实验室名称" @keyup.enter="search" clearable
                  @clear="search"
                  style="width: 180px; margin-right: 10px;"></el-input>
        <el-button type="primary" :icon="Search" @click="search">查询</el-button>
      </div>

      <div>
        <el-row :gutter="16" v-loading="loading">
          <el-col v-for="item in tableData" :key="item.id" :span="6" style="margin-bottom: 10px">
            <el-card shadow="hover">
              <img v-if="item.image" :src="item.image" alt="实验室图片"
                   style="width: 100%; height: 200px; object-fit: cover; border-radius: 4px;">
              <div v-else style="width: 100%; height: 200px; background-color: #f5f7fa; border-radius: 4px;">
              </div>
              <div style="font-size: 16px; font-weight: bold; margin-bottom: 5px;">
                {{ item.name }}
              </div>
              <div style="font-size: 14px; color: #606266; margin-bottom: 5px;">
                位置: {{ item.location || '无' }}
              </div>
              <div style="font-size: 14px; color: #606266; margin-bottom: 5px;">
                容量: {{ item.capacity || '无' }}
              </div>
              <div style="font-size: 14px; color: #606266; margin-bottom: 5px;">
                开放时间: {{ item.open_time || '无' }}
              </div>
              <div style="font-size: 14px; color: #606266; margin-bottom: 5px;">
                关闭时间: {{ item.close_time || '无' }}
              </div>
              <div style="font-size: 14px; color: #606266; margin-bottom: 5px; display: flex; gap: 8px">
                <el-button style="flex:1;" @click="lookDevice(item)">查看设备</el-button>
                <el-button style="flex:1;" type="primary" @click="reserveLab(item)">预约</el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

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

    <reserve-dialog v-model:visible="reserveVisible" :lab-id="currentLab?.id" :lab-name="currentLab?.name"></reserve-dialog>

  </div>
</template>

<script setup>
import {onMounted, reactive, ref} from "vue";
import {getLabList} from "@/api/lab.js";
import {ElMessage} from "element-plus";
import {Search, Plus} from "@element-plus/icons-vue"
import router from "@/router/index.js";
import reserveDialog from "@/components/reserve_dialog.vue";

const reserveVisible = ref(false);

const tableData = ref([]);
const total = ref(0);
const loading = ref(false);
const currentLab = ref(null);

const params = reactive({
  keyword: "",
  page: 1,
  page_size: 10,
})

const lookDevice = async (item) => {
  router.push({
    path: '/manager/lab_device',
    query: {
      lab_id: item.id,
    }
  })
}

const reserveLab = async (item) => {
  currentLab.value = item;
  reserveVisible.value = true;
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