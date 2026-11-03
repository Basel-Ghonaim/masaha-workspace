import pathlib, sys
root = pathlib.Path(r"C:\dev\masaha\app-b")
def sub(rel, old, new):
    p = root / rel
    t = p.read_bytes().decode("utf-8")
    if t.count(old) != 1:
        sys.exit(f"{rel}: {t.count(old)} matches of {old[:40]!r}")
    p.write_bytes(t.replace(old, new).encode("utf-8"))
terms_doc = """    /**
     * The desk's terms for the caller: the rounding and the cap in force, whether they may type a
     * price, and the rates a visit would copy now with no shift and in each shift; the student
     * rates only where the space allows them and they change one (DI-41).
     */
"""
v = "apps/api/src/modules/visits/visits.service.ts"
sub(v, terms_doc + "    /**\n     * A page of the space's visits", "    /**\n     * A page of the space's visits")
sub(v, "      return { rows: rows.map(toDeskVisit), total };\n    },\n\n    async terms(",
       "      return { rows: rows.map(toDeskVisit), total };\n    },\n\n" + terms_doc + "    async terms(")
sub("apps/api/.env.example",
    "# later in the platform settings. WhatsApp in E.164, for example +970599000000.",
    "# later in the platform settings. WhatsApp: a Palestinian or Israeli number, typed in any form the\n# phone rule reads (059…, 00970…), stored in its one E.164 form, for example +970599000000.")
