p = r'C:\dev\masaha\app-lane-t\apps\web\scripts\checkBuild.ts'
s = open(p, encoding='utf8').read()
old_stub = """export function sitePageProblems(
  _manifest: Record<string, ManifestChunk>,
  _names: readonly string[],
): string[] {
  return [];
}

"""
assert old_stub in s
s = s.replace(old_stub, "", 1)
old_fd = """/** The manifest's keys of the first download's chunks: each entry and its static imports, deeply. */
export function firstDownload(manifest: Record<string, ManifestChunk>): string[] {
  const reached = new Set<string>();
  const pending = Object.keys(manifest).filter((key) => manifest[key]?.isEntry === true);
  for (let key = pending.pop(); key !== undefined; key = pending.pop()) {
    if (!reached.has(key)) {
      reached.add(key);
      pending.push(...(manifest[key]?.imports ?? []));
    }
  }
  return [...reached];
}
"""
new_fd = """/** The manifest's keys of the chunks `starts` load: each of them and its static imports, deeply. */
function staticReach(manifest: Record<string, ManifestChunk>, starts: readonly string[]): string[] {
  const reached = new Set<string>();
  const pending = [...starts];
  for (let key = pending.pop(); key !== undefined; key = pending.pop()) {
    if (!reached.has(key)) {
      reached.add(key);
      pending.push(...(manifest[key]?.imports ?? []));
    }
  }
  return [...reached];
}

/** The manifest's keys of the first download's chunks: each entry and its static imports, deeply. */
export function firstDownload(manifest: Record<string, ManifestChunk>): string[] {
  return staticReach(
    manifest,
    Object.keys(manifest).filter((key) => manifest[key]?.isEntry === true),
  );
}
"""
assert old_fd in s
s = s.replace(old_fd, new_fd, 1)
anchor = """/** The forbidden strings that a build file contains. */"""
s = s.replace(anchor, r"""// A site page: a chunk made from a module of the site's page group, each of its pages, shells and
// layouts loaded lazily by the site's routes.
const SITE_PAGE = /^src\/pages\/site\//;

/**
 * What is wrong with the site pages' place in the build (finding 180): each site page whose chunk,
 * with its static imports, deeply, reaches the chunk of one of `names`. A page draws none of those
 * libraries; what loads one lazily (the map's Leaflet part) is not a static import, so it is not
 * held against the page.
 */
export function sitePageProblems(
  manifest: Record<string, ManifestChunk>,
  names: readonly string[],
): string[] {
  return Object.entries(manifest)
    .filter(([, chunk]) => chunk.src !== undefined && SITE_PAGE.test(chunk.src))
    .flatMap(([page]) =>
      staticReach(manifest, [page]).flatMap((key) => {
        const name = manifest[key]?.name;
        return name !== undefined && names.includes(name)
          ? [`${page} reaches ${name}'s chunk (${key}).`]
          : [];
      }),
    );
}

""" + anchor, 1)

old_main = """  for (const problem of libraryFaults) {
    console.error(problem);
  }
"""
new_main = """  for (const problem of libraryFaults) {
    console.error(problem);
  }
  const pageFaults = manifest ? sitePageProblems(manifest, libraries) : [];
  for (const problem of pageFaults) {
    console.error(problem);
  }
"""
assert old_main in s
s = s.replace(old_main, new_main, 1)
old_end = """  } else if (manifest) {
    console.log(
      `No ${libraries.join(' or ')}, nor Leaflet's stylesheet, in the site's first download.`,
    );
  }
}"""
new_end = """  } else if (manifest) {
    console.log(
      `No ${libraries.join(' or ')}, nor Leaflet's stylesheet, in the site's first download.`,
    );
  }

  if (pageFaults.length > 0) {
    console.error(
      `
A site page draws none of the heavy libraries (${libraries.join(', ')}), so its chunk must not reach theirs through its static imports (finding 180): look for a site page importing a capability's index.ts where the capability has a public.ts entry, or a public entry exporting what the dashboard draws.`,
    );
    process.exitCode = 1;
  } else if (manifest) {
    console.log(`No site page reaches ${libraries.join(' or ')} through its static imports.`);
  }
}"""
assert old_end in s
s = s.replace(old_end, new_end, 1)
open(p, 'w', encoding='utf8', newline='').write(s)
