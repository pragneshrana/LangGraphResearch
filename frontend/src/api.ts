const baseUrl = () =>
  import.meta.env.VITE_API_URL?.replace(/\/$/, "") ?? "http://127.0.0.1:8000"

export type ReportRequestBody = {
  query: string
  thread_id?: string | null
  reset_pipeline?: boolean
}

export type ReportResponseBody = {
  report: string
  success: boolean
}

export async function fetchReport(
  body: ReportRequestBody,
  signal?: AbortSignal,
): Promise<ReportResponseBody> {
  const res = await fetch(`${baseUrl()}/report`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: body.query,
      thread_id: body.thread_id || null,
      reset_pipeline: body.reset_pipeline ?? true,
    }),
    signal,
  })

  if (!res.ok) {
    let detail: string
    try {
      const errJson = (await res.json()) as { detail?: unknown }
      detail =
        typeof errJson.detail === "string"
          ? errJson.detail
          : JSON.stringify(errJson.detail ?? errJson)
    } catch {
      detail = await res.text()
    }
    throw new Error(detail || `HTTP ${res.status}`)
  }

  return res.json() as Promise<ReportResponseBody>
}

export async function fetchHealth(): Promise<{ status: string }> {
  const res = await fetch(`${baseUrl()}/health`)
  if (!res.ok) throw new Error(`Health check failed: ${res.status}`)
  return res.json() as Promise<{ status: string }>
}
