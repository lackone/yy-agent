import request from "@/utils/request.js";

export function getDeviceList(data) {
    return request({
        url: '/api/device/list',
        method: 'GET',
        params: data
    })
}

export function createDevice(data) {
    return request({
        url: '/api/device',
        method: 'POST',
        data
    })
}

export function updateDevice(id, data) {
    return request({
        url: `/api/device/${id}`,
        method: 'PUT',
        data
    })
}

export function deleteDevice(id) {
    return request({
        url: `/api/device/${id}`,
        method: 'DELETE',
    })
}