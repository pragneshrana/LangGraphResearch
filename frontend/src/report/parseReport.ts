const SEP_LINE = /^={20,}$/

export type ParsedReport = {
  /** Banner title from the report header, or a default */
  title: string
  generated?: string
  topic?: string
  /** Remaining text after header blocks; suitable for markdown */
  bodyMarkdown: string
}

/**
 * Best-effort parse of the pipeline's ASCII header (title, Generated:, Topic:)
 * and optional footer ("End of report"). If the shape doesn't match, the full
 * string is returned as `bodyMarkdown`.
 */
export function parseReport(raw: string): ParsedReport {
  const trimmedEnd = raw
    .trimEnd()
    .replace(/\n={20,}\s*\n\s*End of report\s*$/i, '')
    .trimEnd()

  const lines = trimmedEnd.split('\n')
  let i = 0

  while (i < lines.length && !lines[i].trim()) i++
  if (i >= lines.length) {
    return {
      title: 'Intelligence report',
      bodyMarkdown: trimmedEnd,
    }
  }

  const firstSep = lines.findIndex((l, j) => j >= i && SEP_LINE.test(l.trim()))
  if (firstSep < 0) {
    return {
      title: 'Intelligence report',
      bodyMarkdown: trimmedEnd,
    }
  }

  const titleBlock = lines.slice(i, firstSep).join('\n').trim()
  const title =
    titleBlock.split('\n')[0]?.trim() || 'Intelligence report'

  let j = firstSep + 1
  const meta: { generated?: string; topic?: string } = {}
  while (j < lines.length && lines[j].trim() && !SEP_LINE.test(lines[j].trim())) {
    const line = lines[j].trim()
    const gen = /^Generated:\s*(.+)$/i.exec(line)
    const topic = /^Topic:\s*(.+)$/i.exec(line)
    if (gen) meta.generated = gen[1]
    else if (topic) meta.topic = topic[1]
    j++
  }

  if (j < lines.length && SEP_LINE.test(lines[j].trim())) j++
  while (j < lines.length && !lines[j].trim()) j++

  const bodyMarkdown = lines.slice(j).join('\n').trim()

  return {
    title,
    generated: meta.generated,
    topic: meta.topic,
    bodyMarkdown: bodyMarkdown || trimmedEnd,
  }
}
