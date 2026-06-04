export interface SessionStatusMeta {
  label: string
  badgeClass: string
  dotClass: string
}

const SESSION_STATUS_META: Record<string, SessionStatusMeta> = {
  running: {
    label: 'Running',
    badgeClass: 'border-cyan-300/25 bg-cyan-300/10 text-cyan-100',
    dotClass: 'bg-cyan-300 shadow-[0_0_18px_rgba(103,232,249,0.75)]',
  },
  waiting: {
    label: 'Waiting for approval',
    badgeClass: 'border-amber-300/25 bg-amber-300/10 text-amber-100',
    dotClass: 'bg-amber-300 shadow-[0_0_18px_rgba(252,211,77,0.75)]',
  },
  failed: {
    label: 'Failed',
    badgeClass: 'border-rose-300/25 bg-rose-300/10 text-rose-100',
    dotClass: 'bg-rose-300 shadow-[0_0_18px_rgba(253,164,175,0.75)]',
  },
  idle: {
    label: 'Idle',
    badgeClass: 'border-emerald-300/20 bg-emerald-300/10 text-emerald-100',
    dotClass: 'bg-emerald-300',
  },
}

export const getSessionStatusMeta = (status: string | null | undefined): SessionStatusMeta => SESSION_STATUS_META[status || 'idle'] || SESSION_STATUS_META.idle
