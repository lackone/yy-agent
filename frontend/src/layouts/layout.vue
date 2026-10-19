<template>
  <div class="common-layout">
    <el-container style="min-height: 100vh">
      <el-header style="display: flex; align-items: center; border-bottom: 1px solid #ddd; background-color: #fff">
        <div style="flex: 1; display: flex; align-items: center; font-size: 24px; font-weight: bold">
          <img src="@/assets/imgs/logo.png" alt="" style="width: 40px">
          <div style="margin-left: 5px">智能预约系统</div>
        </div>
        <div>
          <el-dropdown @command="handleCommand">
            <div style="display: flex; align-items: center; cursor: pointer">
              <img :src="userInfo?.avatar || defaultAvatar" alt=""
                   style="width: 30px; height: 30px; border-radius: 50%; object-fit: cover;">
              <div style="margin-left: 5px">{{ userInfo?.username }}</div>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="goProfile">个人中心</el-dropdown-item>
                <el-dropdown-item command="goPassword">修改密码</el-dropdown-item>
                <el-dropdown-item command="logoutBtn">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-container>
        <el-aside width="220px">
          <el-menu router style="height: 100%" :default-active="router.currentRoute.value.path">
            <el-menu-item index="/manager/home">
              <el-icon><Menu /></el-icon>
              <span>系统首页</span>
            </el-menu-item>
            <el-menu-item index="/manager/lab">
              <el-icon><OfficeBuilding /></el-icon>
              <span>实验室管理</span>
            </el-menu-item>
            <el-menu-item index="/manager/lab_list">
              <el-icon><OfficeBuilding /></el-icon>
              <span>实验室列表</span>
            </el-menu-item>
            <el-menu-item index="/manager/my_reservation">
              <el-icon>
                <Document/>
              </el-icon>
              <span>我的预约</span>
            </el-menu-item>
            <el-menu-item index="/manager/audit_reservation">
              <el-icon>
                <Document/>
              </el-icon>
              <span>审核预约</span>
            </el-menu-item>
            <el-menu-item index="/manager/chat">
              <el-icon><ChatDotRound /></el-icon>
              <span>AI智能助手</span>
            </el-menu-item>
            <el-menu-item index="/manager/device">
              <el-icon>
                <Location/>
              </el-icon>
              <span>设备管理</span>
            </el-menu-item>
            <el-menu-item index="/manager/user">
              <el-icon>
                <User/>
              </el-icon>
              <span>用户管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import {
  ChatDotRound,
  OfficeBuilding,
  Document,
  Location,
  Setting,
  User
} from '@element-plus/icons-vue'
import {ElMessage} from "element-plus";
import router from "@/router/index.js";
import {logout} from "@/utils/auth.js";
import {useUser} from "@/utils/user.js";
import defaultAvatar from '@/assets/imgs/logo.png'

const {userInfo} = useUser()

const handleCommand = (command) => {
  if (command === "goProfile") {
    router.push("/manager/profile")
  } else if (command === "logoutBtn") {
    logout()
    ElMessage.success("退出成功")
    router.push("/login")
  } else if (command === "goPassword") {
    router.push("/manager/password")
  }
}

const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}

const handleClose = (key, keyPath) => {
  console.log(key, keyPath)
}

</script>