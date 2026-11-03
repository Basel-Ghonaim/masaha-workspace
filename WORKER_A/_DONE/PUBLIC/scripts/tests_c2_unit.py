import io

ROOT = 'C:/dev/masaha/app/apps/web/src/features/directory/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


def write(path, text):
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(text)


write('services/pinMark.unit.test.ts', """import { describe, expect, it } from 'vitest';
import { pinMark } from './pinMark';

describe('pinMark', () => {
  it('each live state is a shape as well as a colour', () => {
    expect(pinMark('AVAILABLE')).toEqual({ shape: 'filled', tone: 'success' });
    expect(pinMark('FULL')).toEqual({ shape: 'bar', tone: 'warning' });
    expect(pinMark('CLOSED')).toEqual({ shape: 'hollow', tone: 'neutral' });
    expect(pinMark(null)).toEqual({ shape: 'dashed', tone: 'muted' });
    const shapes = [pinMark('AVAILABLE'), pinMark('FULL'), pinMark('CLOSED'), pinMark(null)].map(
      (mark) => mark.shape,
    );
    expect(new Set(shapes).size).toBe(4);
  });
});
""")

write('services/boundsText.unit.test.ts', """import { describe, expect, it } from 'vitest';
import { boundsText } from './boundsText';

describe('boundsText', () => {
  it('writes south,west,north,east', () => {
    expect(boundsText({ south: 31.4, west: 34.3, north: 31.55, east: 34.5 })).toBe(
      '31.4,34.3,31.55,34.5',
    );
  });
});
""")

p = 'services/filtersOf.unit.test.ts'
sub(p, """  sort: undefined,
  page: 1,
};""", """  sort: undefined,
  page: 1,
  view: 'list',
};""")
sub(p, """      sort: 'name',
      page: 2,
    });""", """      sort: 'name',
      page: 2,
      view: 'list',
    });""")
sub(p, """    expect(read('page=2.5').page).toBe(1);
  });""", """    expect(read('page=2.5').page).toBe(1);
    expect(read('view=grid').view).toBe('list');
  });

  it('reads and writes view=map, the list unwritten', () => {
    expect(read('view=map&verified=1')).toMatchObject({ view: 'map', verified: true });
    expect(paramsOf({ ...DEFAULTS, view: 'map', verified: true }).toString()).toBe(
      'verified=1&view=map',
    );
    expect(paramsOf({ ...DEFAULTS, view: 'list' }).toString()).toBe('');
  });""")

p = 'repository/directoryRepository.unit.test.ts'
sub(p, """import type { DirectorySpace } from '@masaha/shared/directory';""", """import type { DirectorySpace, MapPin } from '@masaha/shared/directory';""")
sub(p, """    expect(JSON.stringify(requests[0]?.params)).not.toContain('31.521');
  });
});""", """    expect(JSON.stringify(requests[0]?.params)).not.toContain('31.521');
  });

  it('asks for the map’s pins with the filters and the box in view', async () => {
    const repository = createDirectoryRepository();
    const pin: MapPin = {
      id: 7,
      slug: 'focus-hub',
      nameEn: 'Focus Hub',
      nameAr: null,
      areaId: 2,
      location: { lat: 31.52, lng: 34.45 },
      isVerified: true,
      days: null,
      cover: null,
      liveStatus: 'AVAILABLE',
    };
    const requests = serve({
      status: 200,
      data: { success: true, data: { pins: [pin], truncated: false } },
    });

    await expect(
      repository.pins({ verified: true, bounds: '31.4,34.3,31.55,34.5' }),
    ).resolves.toEqual({ pins: [pin], truncated: false });
    expect(requests[0]).toMatchObject({
      method: 'get',
      url: '/map/spaces',
      params: { verified: true, bounds: '31.4,34.3,31.55,34.5' },
    });
    expect(requests[0]?.headers['Masaha-Near']).toBeUndefined();
  });
});""")
print('ok')
