import type { AuditValue, AuditValues } from '../../shared/audit/index.ts';

/** What a card's save changes: only its fields set to a new value, as they were and become. */
export interface SettingsChange {
  before: AuditValues;
  after: AuditValues;
}

/**
 * What a save of a card changes: each field whose value differs from the current one. A save that
 * changes nothing answers `null`, and writes and audits nothing.
 */
export function settingsChange<Card extends Record<string, AuditValue>>(
  current: Card,
  next: Card,
): SettingsChange | null {
  const changed = Object.keys(next).filter((field) => next[field] !== current[field]);
  if (changed.length === 0) return null;
  const pick = (from: Card) => Object.fromEntries(changed.map((field) => [field, from[field]]));
  return { before: pick(current), after: pick(next) };
}
