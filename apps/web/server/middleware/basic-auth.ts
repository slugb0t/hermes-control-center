import { timingSafeEqual } from 'node:crypto'

const unauthorized = (event: Parameters<typeof defineEventHandler>[0], message = 'Authentication required') => {
  setResponseHeader(event, 'WWW-Authenticate', 'Basic realm="Hermes Control Center"')
  setResponseStatus(event, 401)
  return message
}

const safeEqual = (left: string, right: string) => {
  const leftBuffer = Buffer.from(left)
  const rightBuffer = Buffer.from(right)

  if (leftBuffer.length !== rightBuffer.length) {
    return false
  }

  return timingSafeEqual(leftBuffer, rightBuffer)
}

export default defineEventHandler((event) => {
  const path = getRequestURL(event).pathname

  if (path === '/api/health') {
    return
  }

  const required = process.env.CONTROL_CENTER_REQUIRE_AUTH === 'true'
  const expectedPassword = process.env.CONTROL_CENTER_BASIC_AUTH_PASSWORD

  if (!required && !expectedPassword) {
    return
  }

  if (!expectedPassword) {
    setResponseStatus(event, 503)
    return 'Hermes Control Center auth is required but no password is configured.'
  }

  const expectedUser = process.env.CONTROL_CENTER_BASIC_AUTH_USER || 'slugb0t'
  const authorization = getHeader(event, 'authorization') || ''

  if (!authorization.startsWith('Basic ')) {
    return unauthorized(event)
  }

  let decoded = ''
  try {
    decoded = Buffer.from(authorization.slice('Basic '.length), 'base64').toString('utf8')
  } catch {
    return unauthorized(event)
  }

  const separator = decoded.indexOf(':')
  if (separator === -1) {
    return unauthorized(event)
  }

  const user = decoded.slice(0, separator)
  const password = decoded.slice(separator + 1)

  if (!safeEqual(user, expectedUser) || !safeEqual(password, expectedPassword)) {
    return unauthorized(event)
  }
})
