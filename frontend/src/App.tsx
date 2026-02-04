import './App.css'
import { useEffect, useMemo, useState } from 'react'
import { getModels, getUsage, sendChat } from './api/client'
import type { ChatResponse, ModelInfo, UsageRecord } from './api/types'

function App() {
  const [models, setModels] = useState<ModelInfo[]>([])
  const [usage, setUsage] = useState<UsageRecord[]>([])
  const [message, setMessage] = useState('')
  const [selectedModel, setSelectedModel] = useState<string>('')
  const [chatResult, setChatResult] = useState<ChatResponse | null>(null)
  const [status, setStatus] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const samplePrompts = [
    { label: 'Summarize', value: 'Summarize the Apollo program in 3 sentences.' },
    { label: 'Support Reply', value: 'Draft a short reply for a user who cannot reset their password.' },
    { label: 'Explain', value: 'Explain transformer attention in simple terms with one example.' },
    { label: 'Checklist', value: 'Create a quick checklist for reviewing a PR.' },
  ]

  const availableModels = useMemo(
    () => models.map((model) => model.name),
    [models],
  )

  useEffect(() => {
    const load = async () => {
      try {
        const [usageResponse, modelResponse] = await Promise.all([
          getUsage(),
          getModels(),
        ])
        setUsage(usageResponse.items)
        setModels(modelResponse.items)
        if (!selectedModel) {
          const hasNano = modelResponse.items.some(
            (model) => model.name === 'gpt-4.1-nano',
          )
          if (hasNano) {
            setSelectedModel('gpt-4.1-nano')
          }
        }
      } catch (loadError) {
        setError((loadError as Error).message)
      }
    }

    void load()
  }, [selectedModel])

  const handleSend = async () => {
    if (!message.trim()) {
      return
    }
    try {
      setError(null)
      setIsLoading(true)
      setStatus('Sending prompt...')
      const result = await sendChat(message, selectedModel || null)
      setChatResult(result)
      const usageResponse = await getUsage()
      setUsage(usageResponse.items)
    } catch (sendError) {
      setError((sendError as Error).message)
    } finally {
      setIsLoading(false)
      setStatus(null)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <p className="eyebrow">LLM Inference Gateway</p>
          <h1>Admin Console</h1>
          <p className="subtitle">
            Internal testing console for model selection and inference tracking.
          </p>
        </div>
        <div className="status">
          {status && <span className="badge">{status}</span>}
          {error && <span className="badge error">{error}</span>}
        </div>
      </header>

      <section className="panel">
        <h2>Prompt Input</h2>
        <div className="form-row">
          <label htmlFor="modelSelect">Model selector</label>
          <select
            id="modelSelect"
            value={selectedModel}
            onChange={(event) => setSelectedModel(event.target.value)}
          >
            <option value="">Use routing policy</option>
            {availableModels.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>
        </div>
        <div className="form-row">
          <label>Sample prompts</label>
          <div className="button-row">
            {samplePrompts.map((sample) => (
              <button
                key={sample.label}
                type="button"
                onClick={() => setMessage(sample.value)}
              >
                {sample.label}
              </button>
            ))}
          </div>
        </div>
        <div className="form-row">
          <label htmlFor="message">User message</label>
          <textarea
            id="message"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            rows={4}
            placeholder="Enter a prompt to test model routing and usage."
          />
        </div>
        <div className="actions">
          <button
            className="primary"
            onClick={handleSend}
            disabled={isLoading}
          >
            {isLoading ? 'Sending...' : 'Submit'}
          </button>
        </div>
        {chatResult && (
          <div className="result">
            <div className="result-header">
              <h3>Response</h3>
              <div className="result-meta">
                <span>Model: {chatResult.model}</span>
                {chatResult.latency_ms !== null &&
                  chatResult.latency_ms !== undefined && (
                    <span>Latency: {chatResult.latency_ms.toFixed(0)} ms</span>
                  )}
                {chatResult.total_tokens !== null &&
                  chatResult.total_tokens !== undefined && (
                    <span>Total tokens: {chatResult.total_tokens}</span>
                  )}
                {chatResult.cost_usd !== null &&
                  chatResult.cost_usd !== undefined && (
                    <span>Cost: ${chatResult.cost_usd}</span>
                  )}
              </div>
            </div>
            <pre>{chatResult.reply}</pre>
          </div>
        )}
      </section>

      <section className="panel">
        <h2>Usage & Cost</h2>
        <div className="table">
          <div className="table-row table-header usage-table">
            <span>Timestamp</span>
            <span>Status</span>
            <span>Model</span>
            <span>Latency</span>
            <span>Tokens</span>
            <span>Cost</span>
          </div>
          {usage.map((record) => (
            <div className="table-row usage-table" key={record.id}>
              <span>{new Date(record.created_at).toLocaleString()}</span>
              <span>{record.success ? 'Success' : 'Failed'}</span>
              <span>{record.model}</span>
              <span>
                {record.latency_ms !== null && record.latency_ms !== undefined
                  ? `${record.latency_ms.toFixed(0)} ms`
                  : '—'}
              </span>
              <span>{record.total_tokens ?? '-'}</span>
              <span>
                {record.cost_usd !== null && record.cost_usd !== undefined
                  ? `$${record.cost_usd}`
                  : '—'}
              </span>
            </div>
          ))}
          {usage.length === 0 && (
            <div className="table-row empty">No usage records yet.</div>
          )}
        </div>
      </section>
    </div>
  )
}

export default App
