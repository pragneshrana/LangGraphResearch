import {
  Alert,
  Button,
  Card,
  Checkbox,
  Description,
  Input,
  Label,
  Spinner,
  TextArea,
  TextField,
} from '@heroui/react'
import { useCallback, useMemo, useState } from 'react'
import { fetchReport } from './api'
import { parseReport } from './report/parseReport'
import { ReportDocument } from './report/ReportDocument'

export default function App() {
  const [query, setQuery] = useState('')
  const [threadId, setThreadId] = useState('')
  const [resetPipeline, setResetPipeline] = useState(true)
  const [report, setReport] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const apiBase = useMemo(
    () => import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000',
    [],
  )

  const parsedReport = useMemo(
    () => (report ? parseReport(report) : null),
    [report],
  )

  const run = useCallback(async () => {
    const q = query.trim()
    if (!q) {
      setError('Enter a question or topic.')
      return
    }
    setError(null)
    setReport(null)
    setLoading(true)
    const ac = new AbortController()
    try {
      const res = await fetchReport(
        {
          query: q,
          thread_id: threadId.trim() || null,
          reset_pipeline: resetPipeline,
        },
        ac.signal,
      )
      setReport(res.report)
    } catch (e) {
      if ((e as Error).name === 'AbortError') return
      setError((e as Error).message || String(e))
    } finally {
      setLoading(false)
    }
  }, [query, threadId, resetPipeline])

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="mx-auto max-w-4xl px-4 py-10">
        <header className="mb-10 text-center">
          <h1 className="text-3xl font-semibold tracking-tight text-white">
            Stock Market Intelligence
          </h1>
          <p className="mt-2 text-sm text-zinc-400">
          </p>
        </header>

        <Card className="border border-zinc-800 bg-zinc-900/80 p-6 shadow-xl backdrop-blur">
          <div className="flex flex-col gap-6">
            <div className="flex flex-col gap-2">
              <Label id="q-label" className="text-sm font-medium text-zinc-300">
                Query
              </Label>
              <TextArea
                aria-labelledby="q-label"
                placeholder="e.g. Brief on AAPL and large-cap tech risks this week"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                rows={5}
                className="w-full"
                fullWidth
              />
            </div>

            <TextField
              value={threadId}
              onChange={setThreadId}
              fullWidth
            >
              <Label className="text-sm font-medium text-zinc-300">
                Thread ID (optional)
              </Label>
              <Input placeholder="e.g. session-001" />
              <Description className="text-zinc-500">
                Same ID reuses checkpoint memory across runs.
              </Description>
            </TextField>

            <Checkbox
              isSelected={resetPipeline}
              onChange={setResetPipeline}
              className="items-start"
            >
              <span className="text-sm">
                Reset pipeline state for this thread (recommended for a fresh
                report)
              </span>
            </Checkbox>

            {error ? (
              <Alert className="border-red-500/50 bg-red-950/40 text-red-100">
                {error}
              </Alert>
            ) : null}

            <Button
              variant="primary"
              size="lg"
              className="font-medium"
              onPress={() => void run()}
              isDisabled={loading}
            >
              {loading ? (
                <span className="inline-flex items-center gap-2">
                  <Spinner size="sm" color="current" />
                  Generating report…
                </span>
              ) : (
                'Generate report'
              )}
            </Button>
          </div>
        </Card>

        {report && parsedReport ? (
          <div className="mt-10">
            <h2 className="mb-4 text-center text-xs font-semibold uppercase tracking-[0.25em] text-zinc-500">
              Latest output
            </h2>
            <div className="max-h-[calc(100vh-12rem)] overflow-y-auto pb-6 pr-1 [-ms-overflow-style:none] [scrollbar-width:thin] [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-zinc-700">
              <ReportDocument parsed={parsedReport} />
            </div>
          </div>
        ) : null}
      </div>
    </div>
  )
}
