
export const useAuth = () => {
    const token = useCookie('auth_token')
    const user = useState('auth_user', () => null)
    const router = useRouter()
    const api = useApi()

    const setToken = (newToken: string) => {
        token.value = newToken
    }

    const setUser = (newUser: any) => {
        user.value = newUser
    }

    // Fetch user data if token exists but user data is missing
    const fetchUser = async () => {
        if (token.value && !user.value) {
            try {
                const response: any = await api.get('/auth/me')
                setUser(response.data.user)
            } catch (error) {
                console.error('Failed to fetch user:', error)
                // If token is invalid, clear it
                token.value = null
                user.value = null
            }
        }
    }

    const login = async (credentials: any) => {
        try {
            const response: any = await api.post('/auth/login', credentials)
            setToken(response.data.token)
            setUser(response.data.user)
            router.push('/dashboard')
            return response
        } catch (error) {
            throw error
        }
    }

    const register = async (credentials: any) => {
        try {
            await api.post('/auth/register', credentials)
            // Auto login after register or redirect to login
            router.push('/login')
        } catch (error) {
            throw error
        }
    }

    const logout = () => {
        token.value = null
        user.value = null
        router.push('/login')
    }

    // Initialize user on mount if token exists
    if (process.client && token.value && !user.value) {
        fetchUser()
    }

    return {
        token,
        user,
        login,
        register,
        logout,
        fetchUser,
        isAuthenticated: computed(() => !!token.value)
    }
}
