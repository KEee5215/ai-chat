const BASE_URL = '/api/v1'

function headers(token?: string, contentType = 'application/json') {
  const h: Record<string, string> = {}
  if (token) h['Authorization'] = `Bearer ${token}`
  if (contentType) h['Content-Type'] = contentType
  return h
}

async function request<T>(path: string, options: RequestInit & { token?: string } = {}): Promise<T> {
  const { token, ...rest } = options
  const contentType = options.headers?.['Content-Type'] ?? (options.body instanceof FormData ? undefined : 'application/json')
  const res = await fetch(`${BASE_URL}${path}`, {
    ...rest,
    headers: headers(token, contentType as string | undefined),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(Array.isArray(err.detail) ? err.detail.map((d: any) => d.msg).join(', ') : err.detail)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

// --- Auth ---

export function register(username: string, email: string, password: string) {
  return request<{ id: string; username: string; email: string; is_active: boolean; created_at: string }>(
    '/auth/register',
    { method: 'POST', body: JSON.stringify({ username, email, password }) }
  )
}

export function login(username: string, password: string) {
  const body = new URLSearchParams()
  body.set('grant_type', 'password')
  body.set('username', username)
  body.set('password', password)
  return request<{ access_token: string; token_type: string }>(
    '/auth/login',
    { method: 'POST', body, headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  )
}

export function getMe(token: string) {
  return request<{ id: string; username: string; email: string; is_active: boolean; created_at: string }>(
    '/auth/me',
    { token }
  )
}

// --- Chat Sessions ---

export function listSessions(token: string) {
  return request<Array<Record<string, unknown>>>(
    '/chats/sessions',
    { token }
  )
}

export function createSession(token: string, title?: string) {
  return request<{ id: string; user_id: string; title?: string; created_at: string; updated_at: string; messages?: MessageResponse[] }>(
    '/chats/sessions',
    { method: 'POST', body: JSON.stringify(title ? { title } : {}), token }
  )
}

export interface MessageResponse {
  id: string
  session_id: string
  role: string
  content: string
  tokens_used: number
  created_at: string
}

export interface ChatSessionResponse {
  id: string
  user_id: string
  title: string | null
  created_at: string
  updated_at: string
  messages: MessageResponse[]
}

export function getSession(token: string, sessionId: string) {
  return request<ChatSessionResponse>(
    `/chats/sessions/${sessionId}`,
    { token }
  )
}

export function sendMessage(token: string, sessionId: string, content: string) {
  return request<Record<string, unknown>>(
    `/chats/sessions/${sessionId}/messages`,
    { method: 'POST', body: JSON.stringify({ content }), token }
  )
}

export async function streamMessage(
  token: string,
  sessionId: string,
  content: string,
  onChunk: (text: string, done: boolean) => void,
  onDone: () => void,
  onError: (err: string) => void
) {
  try {
    const res = await fetch(`${BASE_URL}/chats/sessions/${sessionId}/messages/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ content }),
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }))
      onError(Array.isArray(err.detail) ? err.detail.map((d: any) => d.msg).join(', ') : err.detail)
      return
    }

    const reader = res.body?.getReader()
    if (!reader) {
      onError('Stream not available')
      return
    }

    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        const trimmed = line.trim()
        if (!trimmed || !trimmed.startsWith('data:')) continue
        const jsonStr = trimmed.slice(5).trim()
        try {
          const data = JSON.parse(jsonStr)
          onChunk(data.content || '', data.done ?? false)
          if (data.done) {
            onDone()
            return
          }
        } catch {
          // ignore parse errors for non-JSON lines
        }
      }
    }
    onDone()
  } catch (e: any) {
    onError(e.message || 'Stream error')
  }
}

// --- API Keys ---

export interface ApiKeyResponse {
  id: string
  name: string
  key_preview: string
  last_used_at: string | null
  created_at: string
}

export function listApiKeys(token: string) {
  return request<{ keys: ApiKeyResponse[] }>('/api-keys', { token })
}

export function createApiKey(token: string, name: string) {
  return request<{ key: string } & ApiKeyResponse>(
    '/api-keys',
    { method: 'POST', body: JSON.stringify({ name }), token }
  )
}

export function deleteApiKey(token: string, keyId: string) {
  return request<void>(
    `/api-keys/${keyId}`,
    { method: 'DELETE', token }
  )
}
