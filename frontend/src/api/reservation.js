import request from "@/utils/request.js";

export function createReservation(data) {
    return request({
        url: '/api/reservation',
        method: 'POST',
        data
    })
}

export function getReservationList(params) {
    return request({
        url: '/api/reservation/list',
        method: 'GET',
        params
    })
}

export function getReservation(id) {
    return request({
        url: `/api/reservation/${id}`,
        method: 'GET',
    })
}

export function cancelReservation(id) {
    return request({
        url: `/api/reservation/${id}/cancel`,
        method: 'PUT',
    })
}

export function auditReservation(id, status) {
    return request({
        url: `/api/reservation/${id}/audit`,
        method: 'PUT',
        data: { status }
    })
}
