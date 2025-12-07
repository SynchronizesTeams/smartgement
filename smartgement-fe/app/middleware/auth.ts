export default defineNuxtRouteMiddleware(async (to, from) => {
    const { isAuthenticated, token, user, fetchUser } = useAuth()

    // If no token, redirect to login
    if (!isAuthenticated.value) {
        return navigateTo('/login')
    }

    // If token exists but user not loaded yet, fetch user first
    if (token.value && !user.value) {
        await fetchUser()

        // After fetch, check again if still authenticated
        if (!isAuthenticated.value) {
            return navigateTo('/login')
        }
    }
})
