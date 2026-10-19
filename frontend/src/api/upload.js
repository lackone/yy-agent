import request from "@/utils/request.js";

export function uploadFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request({
        url: '/api/upload/file',
        method: 'POST',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}