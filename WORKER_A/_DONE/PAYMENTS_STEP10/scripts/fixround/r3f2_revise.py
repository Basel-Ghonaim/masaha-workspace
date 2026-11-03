"""R3-F2 revised: the intents keep their bound only; the site's shell lets them go on a guest's landing."""
import io, re

W = 'C:/dev/masaha/app/apps/web/src/'


def rw(path, fn):
    p = W + path
    s = io.open(p, encoding='utf8', newline='').read()
    t = fn(s)
    assert t != s, path
    io.open(p, 'w', encoding='utf8', newline='').write(t)
    print('ok', path)


def fav(s):
    s = s.replace("let held: { favorite: HeldFavorite; from: string } | null = null;", "let held: HeldFavorite | null = null;")
    s = s.replace("// bound to its round trip: let go after `HOLD_MS`, or once the guest lands on another page of the\n// site (`releaseHeldFavorite`), so a later sign-in in the tab, maybe someone else's, saves nothing.",
                  "// bound to its round trip: let go after `HOLD_MS`, or by the site's shell once the guest lands on\n// another page, so a later sign-in in the tab, maybe someone else's, saves nothing.")
    s = s.replace("/** Holds the favourite a guest pressed on the page `from`, until they come back signed in. */\nexport function holdFavorite(favorite: HeldFavorite, from: string): void {\n  forget();\n  held = { favorite, from };",
                  "/** Holds the favourite a guest pressed, until they come back signed in or `HOLD_MS` has passed. */\nexport function holdFavorite(favorite: HeldFavorite): void {\n  forget();\n  held = favorite;")
    s = s.replace("  const taken = held?.favorite ?? null;", "  const taken = held;")
    s = s.replace("/** Lets go of a held favourite: the guest closed the sign-in without going on. */",
                  "/** Lets go of a held favourite: the guest closed the sign-in, or went elsewhere, without going on. */")
    s = re.sub(r"\n/\*\* A guest landed on the page `at`.*?\n}\n", "\n", s, flags=re.S)
    return s.rstrip('\n') + '\n'


rw('features/favorites/hooks/intent/favoriteIntent.ts', fav)


def rep(s):
    s = s.replace("const store = createStore<{ held: string | null; from: string | null }>()(() => ({\n  held: null,\n  from: null,\n}));",
                  "const store = createStore<{ held: string | null }>()(() => ({ held: null }));")
    s = s.replace("// is bound to its round trip: let go after `HOLD_MS`, or once the guest lands on another page of the\n// site (`releaseHeldReport`), so a later visit signed in does not open the dialog by itself.",
                  "// is bound to its round trip: let go after `HOLD_MS`, or by the site's shell once the guest lands on\n// another page, so a later visit signed in does not open the dialog by itself.")
    s = s.replace("  store.setState({ held: null, from: null });", "  store.setState({ held: null });")
    s = s.replace("/** Holds the report a guest pressed on the space `slug`'s page `from`, until they come back signed in. */\nexport function holdReport(slug: string, from: string): void {\n  forget();\n  store.setState({ held: slug, from });",
                  "/** Holds the report a guest pressed on the space `slug`, until they come back signed in. */\nexport function holdReport(slug: string): void {\n  forget();\n  store.setState({ held: slug });")
    s = s.replace("/** Lets go of a held report: the guest closed the sign-in without going on. */",
                  "/** Lets go of a held report: the guest closed the sign-in, or went elsewhere, without going on. */")
    s = re.sub(r"\n/\*\* A guest landed on the page `at`.*?\n}\n", "\n", s, flags=re.S)
    return s


rw('features/data-reports/hooks/intent/reportIntent.ts', rep)


def favtest(s):
    s = s.replace("  HOLD_MS,\n  holdFavorite,\n  releaseHeldFavorite,\n  takeFavorite,", "  HOLD_MS,\n  holdFavorite,\n  takeFavorite,")
    s = s.replace(", '/spaces/masaha-hub');", ");").replace(", '/spaces/old-hub');", ");")
    s = re.sub(r"\n  it\('lets go of it when the guest lands on another page.*?\n  \}\);\n", "\n", s, flags=re.S)
    return s


rw('features/favorites/hooks/intent/favoriteIntent.unit.test.ts', favtest)


def reptest(s):
    s = s.replace("import { dropReport, HOLD_MS, holdReport, releaseHeldReport, takeReport } from './reportIntent';",
                  "import { dropReport, HOLD_MS, holdReport, takeReport } from './reportIntent';")
    s = s.replace("holdReport('masaha-hub', '/spaces/masaha-hub');", "holdReport('masaha-hub');")
    s = re.sub(r"\n  it\('lets go of it when the guest lands on another page.*?\n  \}\);\n", "\n", s, flags=re.S)
    return s


rw('features/data-reports/hooks/intent/reportIntent.unit.test.ts', reptest)
