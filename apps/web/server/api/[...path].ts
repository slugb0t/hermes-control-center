export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const rawPath = event.context.params?.path || ''
  const path = Array.isArray(rawPath) ? rawPath.join('/') : rawPath
  const query = getQuery(event)
  const target = new URL(`/` + path, config.apiInternalBase)

  for (const [key, value] of Object.entries(query)) {
    if (Array.isArray(value)) {
      for (const item of value) {
        target.searchParams.append(key, String(item))
      }
    } else if (value !== undefined) {
      target.searchParams.set(key, String(value))
    }
  }

  return await $fetch(target.toString(), {
    method: event.method,
    headers: {
      accept: getHeader(event, 'accept') || 'application/json'
    }
  })
})
