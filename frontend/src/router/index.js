import {createRouter, createWebHistory} from 'vue-router'
import {getToken} from "@/utils/auth.js";

console.log("BASE_URL", import.meta.env.BASE_URL)

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {path: "/", redirect: "/manager/home"},
        {
            path: "/manager",
            name: "layout",
            component: () => import("@/layouts/layout.vue"),
            children: [
                {path: "lab", name: "lab", component: () => import("@/views/lab/lab.vue")},
                {path: "lab_list", name: "lab_list", component: () => import("@/views/lab/lab_list.vue")},
                {path: "lab_device", name: "lab_device", component: () => import("@/views/lab/lab_device.vue")},
                {path: "user", name: "user", component: () => import("@/views/user/user.vue")},
                {path: "device", name: "device", component: () => import("@/views/device/device.vue")},
                {path: "home", name: "home", component: () => import("@/views/home.vue")},
                {path: "profile", name: "profile", component: () => import("@/views/user/profile.vue")},
                {path: "password", name: "password", component: () => import("@/views/user/password.vue")},
                {path: "my_reservation", name: "my_reservation", component: () => import("@/views/reservation/my_reservation.vue")},
                {path: "audit_reservation", name: "audit_reservation", component: () => import("@/views/reservation/audit_reservation.vue")},
                {path: "chat", name: "chat", component: () => import("@/views/ai/chat.vue")},
            ]
        },
        {path: "/login", name: "login", component: () => import("@/views/login.vue")},
        {path: "/register", name: "register", component: () => import("@/views/register.vue")},
    ],
})

// 路由守卫
router.beforeEach((to, from) => {
    const token = getToken()
    if (to.path === '/login' || to.path === '/register') {
        return true
    } else {
        return token ? true : '/login'
    }
})

export default router
