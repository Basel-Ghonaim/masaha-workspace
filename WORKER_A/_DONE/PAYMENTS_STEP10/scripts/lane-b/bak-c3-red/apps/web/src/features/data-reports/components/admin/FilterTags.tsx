import { Button, FilterTag } from '@shared/design-system';
import type { AdminReportsView } from '../../hooks/admin/useAdminReports';

/**
 * The filters in force, at every width (DI-40, finding 8): the space and the field as removable tags,
 * and «مسح الفلاتر» beside them. Nothing while none applies.
 */
export function FilterTags({
  tags,
  clear,
}: {
  tags: AdminReportsView['tags'];
  clear: AdminReportsView['clear'];
}) {
  if (tags.length === 0) return null;
  return (
    <div className="flex flex-wrap items-center gap-2">
      {tags.map((tag) => (
        <FilterTag key={tag.key} removeLabel={tag.removeLabel} onRemove={tag.remove}>
          {tag.label}
        </FilterTag>
      ))}
      {clear !== null && (
        <Button variant="link" size="sm" onClick={clear.run}>
          {clear.label}
        </Button>
      )}
    </div>
  );
}
