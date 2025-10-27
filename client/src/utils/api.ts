export function apiBase (): string {
  const base = (import.meta as any).env?.VITE_API_BASE_URL as string | undefined
  if (base && typeof base === 'string' && base.trim().length > 0) {
    return base.replace(/\/$/, '')
  }
  return '/api'
}

export function apiUrl (path: string): string {
  const normalized = path.startsWith('/') ? path : `/${path}`
  return `${apiBase()}${normalized}`
}

export async function apiFetch (path: string, init?: RequestInit): Promise<Response> {
  return fetch(apiUrl(path), init)
}
