import { timingSafeEqual } from 'node:crypto'

interface LoginBody {
  username?: string
  password?: string
}

const safeEqual = (left: string, right: string) => {
  const leftBuffer = Buffer.from(left)
  const rightBuffer = Buffer.from(right)

  if (leftBuffer.length !== rightBuffer.length) {
    return false
  }

  return timingSafeEqual(leftBuffer, rightBuffer)
}

export default defineEventHandler(async (event) => {
  const body = await readBody<LoginBody>(event)
  const expectedUser = process.env.CONTROL_CENTER_AUTH_USER || 'slugb0t'
  const expectedPassword = process.env.CONTROL_CENTER_AUTH_PASSWORD

  if (!expectedPassword) {
    throw createError({
      statusCode: 503,
      statusMessage: 'Control Center authentication is not configured'
    })
  }

  if (!body?.username || !body?.password) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Username and password are required'
    })
  }

  if (!safeEqual(body.username, expectedUser) || !safeEqual(body.password, expectedPassword)) {
    throw createError({
      statusCode: 401,
      statusMessage: 'Invalid username or password'
    })
  }

  await setUserSession(event, {
    user: {
      login: expectedUser,
      name: expectedUser
    },
    loggedInAt: new Date().toISOString()
  })

  return { ok: true }
})
