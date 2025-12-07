export const useApi = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase
  const aiBase = config.public.aiBase

  const call = async <T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> => {
    const url = `${apiBase}${endpoint}`

    try {
      const token = useCookie('auth_token').value
      const headers: any = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...options.headers,
      }

      if (token) headers['Authorization'] = `Bearer ${token}`

      return await $fetch<T>(url, {
        ...options,
        headers,
      } as any)
    } catch (error: any) {
      console.error('API call error:', error)
      throw error
    }
  }

  const callAI = async <T = any>(
    endpoint: string,
    body: any
  ): Promise<T> => {
    const url = `${aiBase}${endpoint}`

    try {
      return await $fetch<T>(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body
      })
    } catch (error: any) {
      console.error('AI call error:', error)
      throw error
    }
  }

  return {
    call,
    callAI, // ⬅ WAJIB RETURN DI SINI
    get: (endpoint: string, options: any = {}) =>
      call(endpoint, { ...options, method: 'GET' }),
    post: (endpoint: string, data?: any) =>
      call(endpoint, { method: 'POST', body: JSON.stringify(data) }),
    put: (endpoint: string, data?: any) =>
      call(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (endpoint: string) =>
      call(endpoint, { method: 'DELETE' }),
  }
}
