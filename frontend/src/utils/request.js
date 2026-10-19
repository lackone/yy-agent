import axios from 'axios'
import {getToken, logout} from "@/utils/auth.js";
import {ElMessage} from "element-plus";
import router from "@/router/index.js";


const service = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '',
    timeout: 30000, // 30秒
})

console.log('API_BASE_URL:', import.meta.env.VITE_API_BASE_URL)

// 请求拦截器
service.interceptors.request.use(
    config => {
        const token = getToken()
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// 响应拦截器
service.interceptors.response.use(
    response => {
        const data = response.data
        if (data.code !== 200) {
            ElMessage.error(data.msg || '请求失败')
            if (data.code === 401) {
                // 清除token
                logout()
                router.push('/login')
                return Promise.reject(data)
            }
        }
        return data
    },
    error => {
        if (error.response) {
            const httpStatus = error.response.status
            if (httpStatus === 401) {
                ElMessage.error('登录过期，请重新登录')
                // 清除token
                logout()
                router.push('/login')
            } else {
                ElMessage.error(error.response.data?.msg || '请求失败')
            }
        } else {
            ElMessage.error(error.message || '请求失败')
        }
        return Promise.reject(error)
    }
)

export default service
