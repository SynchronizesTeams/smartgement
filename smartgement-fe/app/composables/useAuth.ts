export const useAuth = () => {
    const token = useCookie('auth_token', {
        path: '/',
        maxAge: 60 * 60 * 24 * 7, // 7 hari
        sameSite: 'strict',
        secure: process.env.NODE_ENV === 'production',
    })

    const user = useState('auth_user', () => null)
    const router = useRouter()
    const api = useApi()

    const setToken = (newToken: string) => {
        token.value = newToken
    }

    const setUser = (newUser: any) => {
        user.value = newUser
    }

    const fetchUser = async () => {
        if (!token.value) {
            user.value = null
            return
        }

        if (user.value) {
            return // Already fetched
        }

        try {
            const response: any = await api.get('/auth/me')
            setUser(response.data.user)
        } catch (error: any) {
            console.warn("Failed to fetch user:", error.response?.status)
            // Only logout if token is actually invalid (401)
            if (error.response?.status === 401) {
                console.warn("Token invalid. Clearing auth.")
                token.value = null
                user.value = null
            }
        }
    }

    const login = async (credentials: any) => {
        const response: any = await api.post('/auth/login', credentials)
        setToken(response.data.token)
        setUser(response.data.user)
        router.push('/dashboard')
        return response
    }

    const register = async (credentials: any) => {
        await api.post('/auth/register', credentials)
        router.push('/login')
    }

    const logout = () => {
        token.value = null
        user.value = null
        router.push('/login')
    }

    return {
        token,
        user,
        login,
        register,
        logout,
        fetchUser,
        isAuthenticated: computed(() => !!token.value),
    }
}
