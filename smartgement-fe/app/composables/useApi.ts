export const useApi = () => {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const call = async <T = any>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<T> => {
        const url = `${apiBase}${endpoint}`
        console.log('[useApi] Calling:', url, 'with Base:', apiBase)

        try {
            const token = useCookie('auth_token').value
            console.log("Auth Token from cookies:", token)

            const headers: any = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                ...options.headers,
            }

            if (token) {
                headers['Authorization'] = `Bearer ${token}`
            }

            const response = await $fetch<T>(url, {
                ...options,
                headers,
            } as any)

            return response
        } catch (error: any) {
            console.error('API call error:', error)
            throw error
        }
    }

    const get = <T = any>(endpoint: string, options: any = {}) => {
        return call<T>(endpoint, { ...options, method: 'GET' })
    }

    const post = <T = any>(endpoint: string, data?: any) => {
        return call<T>(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        })
    }

    const put = <T = any>(endpoint: string, data?: any) => {
        return call<T>(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        })
    }

    const del = <T = any>(endpoint: string) => {
        return call<T>(endpoint, { method: 'DELETE' })
    }

    return {
        call,
        get,
        post,
        put,
        delete: del,
    }
}
