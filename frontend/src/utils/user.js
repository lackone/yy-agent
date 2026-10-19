// 仅供页面 setup 中使用
import {ref} from 'vue'
import {getUser, setToken, setUser} from "@/utils/auth.js";

// 响应式对象
const userInfo = ref(getUser())

export function useUser() {
    function saveLoginData(data) {
        setToken(data.token)
        setUser(data)

        userInfo.value = data
    }

    function updateUser(data) {
        setUser(data)

        userInfo.value = data
    }

    function reloadUser() {
        userInfo.value = getUser()
    }

    return {
        userInfo,
        saveLoginData,
        updateUser,
        reloadUser
    }
}