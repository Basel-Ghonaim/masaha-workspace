import io

ROOT = 'C:/dev/masaha/app/apps/web/src/features/directory/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


p = 'hooks/list/useDirectoryList.ts'
sub(p, """import { useCopy } from '@shared/copy';
import type { AppError } from '@shared/errors';
import { useRefusalView } from '@shared/forms';
import { paginationView, usePageInRange } from '@shared/lists';""", """import { useCopy } from '@shared/copy';
import { paginationView, usePageInRange } from '@shared/lists';""")
sub(p, """import type { DirectoryListView, ListFailureView } from '../../types/DirectoryListView';""", """import type { DirectoryListView } from '../../types/DirectoryListView';""")
sub(p, """import { useDirectoryQuery } from './useDirectoryQuery';
""", """import { useDirectoryQuery } from './useDirectoryQuery';
import { useFailureView } from './useFailureView';
""")
sub(p, """  const failed = answer === undefined ? query.error : null;
  const load = useRefusalView(failed, words.loadFailed);
  const refresh = useRefusalView(
    answer !== undefined && query.isError ? query.error : null,
    words.refreshFailed,
  );
  const failureOf = (
    view: typeof load,
    error: AppError | null,
    title: string,
  ): ListFailureView | null =>
    error === null
      ? null
      : {
          title,
          // Too many requests' view is gone once its count ends; the failure stays, with its retry.
          line: view.view?.message ?? copy.errors.rate_limit,
          reference: view.view?.kind === 'refused' ? (view.view.reference ?? null) : null,
          retry: {
            label: copy.status.retry,
            blocked: view.blocked,
            run: () => {
              void query.refetch();
            },
          },
        };
""", """  const retry = () => {
    void query.refetch();
  };
  const failure = useFailureView(
    answer === undefined ? query.error : null,
    words.loadFailed,
    retry,
  );
  const refreshFailure = useFailureView(
    answer !== undefined && query.isError ? query.error : null,
    words.refreshFailed,
    retry,
  );
""")
sub(p, """      failure: failureOf(load, failed, words.loadFailed),
      refreshFailure: failureOf(
        refresh,
        answer !== undefined && query.isError ? query.error : null,
        words.refreshFailed,
      ),""", """      failure,
      refreshFailure,""")
print('ok')
