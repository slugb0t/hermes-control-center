export default defineEventHandler(async (event) => {
  const path = getRequestURL(event).pathname

  if (
    !path.startsWith('/api/') ||
    path === '/api/health' ||
    path.startsWith('/api/_auth/') ||
    path === '/api/auth/login' ||
    path === '/api/auth/logout'
  ) {
    return
  }

  await requireUserSession(event)
})
