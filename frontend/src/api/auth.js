import request from '@/utils/request.js'

/**
 * 登录
 * @param data
 * @returns {*}
 */
export function loginApi(data) {
    return request({
        url: '/api/auth/login',
        method: 'POST',
        data
    })
}

/**
 * 注册
 * @param data
 * @returns {*}
 */
export function registerApi(data) {
    return request({
        url: '/api/auth/register',
        method: 'POST',
        data
    })
}
