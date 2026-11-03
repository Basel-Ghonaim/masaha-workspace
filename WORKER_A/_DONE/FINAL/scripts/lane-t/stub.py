p = r'C:\dev\masaha\app-lane-t\apps\web\scripts\checkBuild.ts'
s = open(p, encoding='utf8').read()
s = s.replace("""  isEntry?: boolean;
  imports?: string[];
""", """  isEntry?: boolean;
  isDynamicEntry?: boolean;
  imports?: string[];
  dynamicImports?: string[];
""", 1)
s = s.replace("""/** The forbidden strings that a build file contains. */""", """export function sitePageProblems(
  _manifest: Record<string, ManifestChunk>,
  _names: readonly string[],
): string[] {
  return [];
}

/** The forbidden strings that a build file contains. */""", 1)
open(p, 'w', encoding='utf8', newline='').write(s)
