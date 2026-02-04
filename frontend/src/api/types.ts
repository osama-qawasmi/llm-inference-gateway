export type RoutingRule = {
  max_characters: number
  model: string
}

export type RoutingConfig = {
  default_model: string
  rules: RoutingRule[]
}

export type ChatResponse = {
  reply: string
  model: string
  latency_ms?: number | null
  input_tokens?: number | null
  output_tokens?: number | null
  total_tokens?: number | null
  cost_usd?: number | null
}

export type UsageRecord = {
  id: string
  created_at: string
  provider: string
  model: string
  success: boolean
  latency_ms?: number | null
  input_tokens?: number | null
  output_tokens?: number | null
  total_tokens?: number | null
  cost_usd?: number | null
  error_message?: string | null
  message: string
  response: string
}

export type UsageListResponse = {
  items: UsageRecord[]
}

export type ModelInfo = {
  name: string
  input_cost_per_1k?: number | null
  output_cost_per_1k?: number | null
}

export type ModelListResponse = {
  items: ModelInfo[]
}

export type MetricSummary = {
  total_requests: number
  success_count: number
  failure_count: number
  success_rate: number
  avg_latency_ms?: number | null
  p95_latency_ms?: number | null
  avg_tokens?: number | null
  avg_cost_usd?: number | null
  cost_per_request_usd?: number | null
}

export type ModelMetrics = {
  model: string
  total_requests: number
  success_rate: number
  avg_latency_ms?: number | null
  avg_tokens?: number | null
  avg_cost_usd?: number | null
}

export type MetricsResponse = {
  summary: MetricSummary
  by_model: ModelMetrics[]
}
