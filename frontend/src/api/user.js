import request from "@/utils/request.js";

export function getUserInfo() {
    return request({
        url: '/api/user/me',
        method: 'GET',
    })
}

export function updateUserInfo(data) {
    return request({
        url: '/api/user/me',
        method: 'PUT',
        data
    })
}

export function updatePassword(data) {
    return request({
        url: '/api/user/password',
        method: 'PUT',
        data
    })
}

export function getUserList(data) {
    return request({
        url: '/api/user/list',
        method: 'GET',
        params: data
    })
}

export function createUser(data) {
    return request({
        url: '/api/user',
        method: 'POST',
        data
    })
}

export function updateUser(id, data) {
    return request({
        url: `/api/user/${id}`,
        method: 'PUT',
        data
    })
}

export function deleteUser(id) {
    return request({
        url: `/api/user/${id}`,
        method: 'DELETE',
    })
}
