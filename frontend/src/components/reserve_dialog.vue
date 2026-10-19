<template>
  <div>
    <el-dialog :model-value="visible" title="预约" width="500px" @open="formRef?.resetFields()"
               @close="emit('update:visible', false)">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px"
               style="width: 100%; padding-right: 30px; padding-top:15px;">
        <el-form-item label="实验室名称" prop="labName">
          <el-input :model-value="labName" disabled/>
        </el-form-item>
        <el-form-item label="设备名称" prop="deviceName">
          <el-input :model-value="deviceName" disabled/>
        </el-form-item>
        <el-form-item label="日期" prop="date">
          <el-date-picker v-model="form.date" type="date" format="YYYY-MM-DD"
                          value-format="YYYY-MM-DD" placeholder="请输入日期"/>
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-time-picker v-model="form.start_time" type="time" format="HH:mm"
                          value-format="HH:mm" placeholder="请输入开始时间"/>
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-time-picker v-model="form.end_time" type="time" format="HH:mm"
                          value-format="HH:mm" placeholder="请输入结束时间"/>
        </el-form-item>
        <el-form-item label="预约备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" placeholder="请输入预约备注"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="emit('update:visible', false)">取消</el-button>
          <el-button type="primary" :loading="formLoading" @click="submitForm">
            提交
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {reactive, ref} from "vue";
import {ElMessage} from "element-plus";
import {createReservation} from "@/api/reservation.js";

const props = defineProps({
  visible: Boolean,
  labId: Number,
  labName: String,
  deviceId: Number,
  deviceName: String,
})

const emit = defineEmits(['update:visible'])

const formLoading = ref(false);
const formRef = ref(null)

const form = reactive({
  date: '',
  start_time: '09:00',
  end_time: '18:00',
  remark: '',
})

const rules = {
  date: [{required: true, message: '请输入日期', trigger: 'change'}],
  start_time: [{required: true, message: '请输入开始时间', trigger: 'change'}],
  end_time: [{required: true, message: '请输入结束时间', trigger: 'change'}],
}

const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }
  formLoading.value = true
  try {
    form.lab_id = props.labId
    form.device_id = props.deviceId
    const res = await createReservation(form)
    if (res.code === 200) {
      ElMessage.success('操作成功')
      emit('update:visible', false)
    }
  } finally {
    formLoading.value = false
  }
}

</script>
