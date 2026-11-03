"""R3-F2's unit tests: the held intents' bound and their release on another page."""
import io

W = 'C:/dev/masaha/app/apps/web/src/'


def write_tail(path, old_imports, new_imports, tail):
    p = W + path
    s = io.open(p, encoding='utf8', newline='').read()
    assert s.count(old_imports) == 1, path
    s = s.replace(old_imports, new_imports)
    s = s.rstrip('\n')
    assert s.endswith('});')
    s = s[:-3] + tail
    io.open(p, 'w', encoding='utf8', newline='').write(s)
    print('ok', path)


write_tail(
    'features/favorites/hooks/intent/favoriteIntent.unit.test.ts',
    "import { afterEach, describe, expect, it } from 'vitest';\nimport { dropFavorite, holdFavorite, takeFavorite } from './favoriteIntent';",
    "import { afterEach, describe, expect, it, vi } from 'vitest';\nimport {\n  dropFavorite,\n  HOLD_MS,\n  holdFavorite,\n  releaseHeldFavorite,\n  takeFavorite,\n} from './favoriteIntent';",
    """
  it('lets go of it once its round trip is over: 15 minutes after it was held', () => {
    vi.useFakeTimers();
    try {
      expect(HOLD_MS).toBe(15 * 60 * 1000);
      holdFavorite({ spaceId: 7, name: { text: 'Masaha Hub' } }, '/spaces/masaha-hub');
      vi.advanceTimersByTime(HOLD_MS - 1);
      holdFavorite({ spaceId: 8, name: { text: 'Old Hub' } }, '/spaces/old-hub');
      vi.advanceTimersByTime(HOLD_MS - 1);
      expect(takeFavorite()).toEqual({ spaceId: 8, name: { text: 'Old Hub' } });

      holdFavorite({ spaceId: 7, name: { text: 'Masaha Hub' } }, '/spaces/masaha-hub');
      vi.advanceTimersByTime(HOLD_MS);
      expect(takeFavorite()).toBeNull();
    } finally {
      vi.useRealTimers();
    }
  });

  it('lets go of it when the guest lands on another page, and keeps it on the page that held it', () => {
    holdFavorite({ spaceId: 7, name: { text: 'Masaha Hub' } }, '/spaces/masaha-hub');
    releaseHeldFavorite('/spaces/masaha-hub');
    expect(takeFavorite()).toEqual({ spaceId: 7, name: { text: 'Masaha Hub' } });

    holdFavorite({ spaceId: 7, name: { text: 'Masaha Hub' } }, '/spaces/masaha-hub');
    releaseHeldFavorite('/');
    expect(takeFavorite()).toBeNull();
  });
});
""")

write_tail(
    'features/data-reports/hooks/intent/reportIntent.unit.test.ts',
    "import { afterEach, describe, expect, it } from 'vitest';\nimport { dropReport, holdReport, takeReport } from './reportIntent';",
    "import { afterEach, describe, expect, it, vi } from 'vitest';\nimport { dropReport, HOLD_MS, holdReport, releaseHeldReport, takeReport } from './reportIntent';",
    """
  it('lets go of it once its round trip is over: 15 minutes after it was held', () => {
    vi.useFakeTimers();
    try {
      expect(HOLD_MS).toBe(15 * 60 * 1000);
      holdReport('masaha-hub', '/spaces/masaha-hub');
      vi.advanceTimersByTime(HOLD_MS - 1);
      expect(takeReport('masaha-hub')).toBe(true);

      holdReport('masaha-hub', '/spaces/masaha-hub');
      vi.advanceTimersByTime(HOLD_MS);
      expect(takeReport('masaha-hub')).toBe(false);
    } finally {
      vi.useRealTimers();
    }
  });

  it('lets go of it when the guest lands on another page, and keeps it on the page that held it', () => {
    holdReport('masaha-hub', '/spaces/masaha-hub');
    releaseHeldReport('/spaces/masaha-hub');
    expect(takeReport('masaha-hub')).toBe(true);

    holdReport('masaha-hub', '/spaces/masaha-hub');
    releaseHeldReport('/spaces');
    expect(takeReport('masaha-hub')).toBe(false);
  });
});
""")
