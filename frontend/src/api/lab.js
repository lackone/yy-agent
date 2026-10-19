import request from "@/utils/request.js";

export function getLabList(data) {
    return request({
        url: '/api/lab/list',
        method: 'GET',
        params: data
    })
}

export function getLab(id) {
    return request({
        url: `/api/lab/${id}`,
        method: 'GET',
    })
}

export function createLab(data) {
    return request({
        url: '/api/lab',
        method: 'POST',
        data
    })
}

export function updateLab(id, data) {
    return request({
        url: `/api/lab/${id}`,
        method: 'PUT',
        data
    })
}

export function deleteLab(id) {
    return request({
        url: `/api/lab/${id}`,
        method: 'DELETE',
    })
}