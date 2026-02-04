import type {
  ChatResponse,
  MetricsResponse,
  ModelListResponse,
  RoutingConfig,
  UsageListResponse,
} from './types'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? ''

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers ?? {}),
    },
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(detail || `Request failed with ${response.status}`)
  }

  const contentType = response.headers.get('content-type') ?? ''
  if (!contentType.includes('application/json')) {
    const body = await response.text()
    throw new Error(
      `Expected JSON but received ${contentType || 'unknown content type'}: ${body.slice(0, 200)}`,
    )
  }

  return response.json() as Promise<T>
}

export function getRoutingConfig(): Promise<RoutingConfig> {
  return request('/api/routing')
}

export function updateRoutingConfig(
  config: RoutingConfig,
): Promise<RoutingConfig> {
  return request('/api/routing', {
    method: 'PUT',
    body: JSON.stringify(config),
  })
}

export function sendChat(
  message: string,
  model?: string | null,
): Promise<ChatResponse> {
  return request('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message, model: model || undefined }),
  })
}

export function getUsage(limit = 50): Promise<UsageListResponse> {
  return request(`/api/usage?limit=${limit}`)
}

export function getModels(): Promise<ModelListResponse> {
  return request('/api/models')
}

export function getMetrics(): Promise<MetricsResponse> {
  return request('/api/metrics')
}
