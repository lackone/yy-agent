import request from '@/utils/request.js'
import {getToken} from "@/utils/auth.js";

export function chatApi(data) {
    return request({
        url: '/api/ai/chat',
        method: 'POST',
        data,
        timeout: 30000,
    })
}

export async function chatStreamApi(data, onEvent) {
    const baseUrl = import.meta.env.VITE_API_BASE_URL
    const token = getToken()

    const res = await fetch(`${baseUrl}/api/ai/chat/stream`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            "Accept": "text/event-stream",
        },
        body: JSON.stringify(data),
    })
    if (res.status === 401) {
        throw new Error("token过期，请重新登录")
    }
    if (!res.ok || !res.body) {
        throw new Error("请求失败")
    }
    const contentType = res.headers.get('content-type')
    if (!contentType || !contentType.includes('text/event-stream')) {
        throw new Error("响应内容类型错误")
    }
    const reader = res.body.getReader()
    const decoder = new TextDecoder("utf-8")
    let buffer = ''

    while (true) {
        const {done, value} = await reader.read()
        if (done) {
            break // 响应结束
        }
        buffer += decoder.decode(value, {stream: true}) // 解码为字符串

        const chunks = buffer.split("\n\n")
        buffer = chunks.pop() // 保留未处理的字符串

        for (const chunk of chunks) {
            const line = chunk.split('\n')
                .map((i) => i.trim())
                .find((i) => i.startsWith("data:"))
            if (!line) {
                continue
            }
            const res = line.slice(5).trim()
            if (!res || res === '[DONE]') {
                continue
            }
            try {
                onEvent(JSON.parse(res))
            } catch {

            }
        }
    }
}
