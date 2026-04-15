import Markdown from 'react-markdown'
import type { ComponentPropsWithoutRef } from 'react'
import type { ParsedReport } from './parseReport'

type ReportDocumentProps = {
  parsed: ParsedReport
}

const mdComponents = {
  p: ({ children, ...props }: ComponentPropsWithoutRef<'p'>) => (
    <p
      className="text-[15px] leading-[1.7] text-zinc-300 first:mt-0 [&+p]:mt-5"
      {...props}
    >
      {children}
    </p>
  ),
  strong: ({ children, ...props }: ComponentPropsWithoutRef<'strong'>) => (
    <strong
      className="font-semibold text-emerald-100/95"
      {...props}
    >
      {children}
    </strong>
  ),
  ul: ({ children, ...props }: ComponentPropsWithoutRef<'ul'>) => (
    <ul
      className="my-4 list-disc space-y-2 border-l-2 border-emerald-500/30 pl-5 marker:text-emerald-500/70"
      {...props}
    >
      {children}
    </ul>
  ),
  ol: ({ children, ...props }: ComponentPropsWithoutRef<'ol'>) => (
    <ol
      className="my-4 list-decimal space-y-2 pl-6 text-zinc-300 marker:text-emerald-600/90"
      {...props}
    >
      {children}
    </ol>
  ),
  li: ({ children, ...props }: ComponentPropsWithoutRef<'li'>) => (
    <li className="text-[15px] leading-relaxed text-zinc-300" {...props}>
      {children}
    </li>
  ),
  hr: () => (
    <hr className="my-10 border-0 h-px bg-gradient-to-r from-transparent via-zinc-500/35 to-transparent" />
  ),
}

export function ReportDocument({ parsed }: ReportDocumentProps) {
  const { title, generated, topic, bodyMarkdown } = parsed

  return (
    <article className="overflow-hidden rounded-2xl border border-zinc-700/80 bg-zinc-900/40 shadow-2xl shadow-black/40 ring-1 ring-white/[0.04]">
      {/* Hero header */}
      <div className="relative border-b border-zinc-800/90 bg-gradient-to-br from-emerald-950/80 via-zinc-900/90 to-blue-950/40 px-6 py-8 sm:px-10 sm:py-10">
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 opacity-[0.07]"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
          }}
        />
        <div className="pointer-events-none absolute -right-20 -top-20 h-64 w-64 rounded-full bg-emerald-500/15 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-16 -left-12 h-48 w-48 rounded-full bg-blue-600/10 blur-3xl" />

        <p className="relative text-[11px] font-semibold uppercase tracking-[0.35em] text-emerald-400/90">
          Stock intelligence
        </p>
        <h2 className="relative mt-2 max-w-3xl font-serif text-2xl font-semibold tracking-tight text-white sm:text-3xl">
          {title}
        </h2>

        <div className="relative mt-6 flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:gap-4">
          {generated ? (
            <div className="inline-flex items-center gap-2.5 rounded-lg border border-white/10 bg-black/25 px-3 py-2 text-sm text-zinc-300 backdrop-blur-sm">
              <span
                aria-hidden
                className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-emerald-500/20 text-base"
              >
                &#128197;
              </span>
              <span>
                <span className="block text-[10px] font-medium uppercase tracking-wider text-zinc-500">
                  Generated
                </span>
                <span className="font-medium text-zinc-100">{generated}</span>
              </span>
            </div>
          ) : null}
          {topic ? (
            <div className="min-w-0 flex-1 rounded-lg border border-white/10 bg-black/25 px-3 py-2 backdrop-blur-sm sm:max-w-xl">
              <span
                className="block text-[10px] font-medium uppercase tracking-wider text-zinc-500"
              >
                Topic
              </span>
              <p className="mt-0.5 text-sm leading-snug text-zinc-200">{topic}</p>
            </div>
          ) : null}
        </div>
      </div>

      {/* Body */}
      <div className="relative px-6 py-8 sm:px-10 sm:py-10">
        <div className="max-w-none selection:bg-emerald-500/25 selection:text-emerald-50">
          <Markdown components={mdComponents}>{bodyMarkdown}</Markdown>
        </div>

        <div
          className="mt-12 flex items-center justify-center gap-3 border-t border-dashed border-zinc-700/70 pt-8"
          aria-hidden
        >
          <span className="h-px w-12 bg-gradient-to-r from-transparent to-zinc-600" />
          <span className="text-[10px] font-semibold uppercase tracking-[0.35em] text-zinc-600">
            Report complete
          </span>
          <span className="h-px w-12 bg-gradient-to-l from-transparent to-zinc-600" />
        </div>
      </div>
    </article>
  )
}
