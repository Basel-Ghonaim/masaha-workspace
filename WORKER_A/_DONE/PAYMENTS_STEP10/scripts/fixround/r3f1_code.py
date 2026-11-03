"""R3-F1: «إزالة» of a space that left: no «تراجع»; said that it cannot be saved again."""
import io

W = 'C:/dev/masaha/app/apps/web/src/'


def edit(path, pairs):
    p = W + path
    s = io.open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf8', newline='').write(s)
    print('ok', path)


edit('shared/copy/english/favorites.ts', [
    ("  removed: 'Removed from favourites',\n",
     "  removed: 'Removed from favourites',\n"
     "  /** «إزالة» of a space that left the directory: no undo, since it cannot be saved meanwhile. */\n"
     "  removedLeft: ({ name }: { name: string }) =>\n"
     "    `${name} removed from favourites. It can’t be saved again while it’s out of the directory.`,\n"),
])
edit('shared/copy/arabic/favorites.ts', [
    ("  removed: 'أُزيلت من المفضّلة',\n",
     "  removed: 'أُزيلت من المفضّلة',\n"
     "  removedLeft: ({ name }: { name: string }) =>\n"
     "    `أُزيلت ${name} من المفضّلة. لا يمكن حفظها من جديد ما دامت خارج الدليل.`,\n"),
])
edit('features/favorites/components/toast/favoriteToasts.tsx', [
    ("/** Says a guest's favourite was saved once they came back signed in (DI-61). */",
     "/**\n"
     " * Says a space that left the directory was removed from the favourites, with no «تراجع»: the API\n"
     " * saves no space out of the directory, so an undo could never work (DI-58, the owner's word).\n"
     " */\n"
     "export function toastRemovedLeft(name: SpaceNameView) {\n"
     "  toast.success(currentCopy().favorites.removedLeft({ name: isolate(name.text) }));\n"
     "}\n\n"
     "/** Says a guest's favourite was saved once they came back signed in (DI-61). */"),
])
edit('features/favorites/hooks/favoriteWrite.ts', [
    ("  toastFavoriteFailed,\n", "  toastFavoriteFailed,\n  toastRemovedLeft,\n"),
    ("/** How a write is said once it is done: with «تراجع», as a guest's return, or not at all (an undo). */\nexport type FavoriteWriteSay = 'undoable' | 'returned' | 'quiet';",
     "/**\n * How a write is said once it is done: with «تراجع», as a guest's return, as the removal of a space\n * that left the directory (no «تراجع»: it cannot be saved meanwhile), or not at all (an undo).\n */\nexport type FavoriteWriteSay = 'undoable' | 'returned' | 'left' | 'quiet';"),
    ("  } else if (say === 'returned') {\n    toastSavedOnReturn(space.name);\n  }",
     "  } else if (say === 'returned') {\n    toastSavedOnReturn(space.name);\n  } else if (say === 'left') {\n    toastRemovedLeft(space.name);\n  }"),
])
edit('features/favorites/hooks/toggle/useFavoriteToggle.ts', [
    ("import type { FavoriteSignIn, HeartSpace } from '../../types/FavoriteSpace';\nimport { writeFavorite } from '../favoriteWrite';",
     "import type { FavoriteSignIn, HeartSpace } from '../../types/FavoriteSpace';\nimport { writeFavorite, type FavoriteWriteSay } from '../favoriteWrite';"),
    ("  signIn,\n  manage,\n}: {\n  space: HeartSpace;\n  saved: boolean;\n  signIn: FavoriteSignIn;\n  manage: () => void;\n}) {",
     "  signIn,\n  manage,\n  say = 'undoable',\n}: {\n  space: HeartSpace;\n  saved: boolean;\n  signIn: FavoriteSignIn;\n  manage: () => void;\n  /** How the write is said: with «تراجع», or, for a space that left the directory, without. */\n  say?: Extract<FavoriteWriteSay, 'undoable' | 'left'>;\n}) {"),
    ("        say: 'undoable',\n", "        say,\n"),
])
edit('features/favorites/components/RemoveFavorite.tsx', [
    (" * «إزالة» of a saved space that left the directory (C7): named «إزالة {name} من المفضّلة», sent once,\n * said with «تراجع», which saves it again (DI-49); held until the favourites are read again, when its\n * row leaves. `manage` leads to the favourites, from a full list's refusal of the undo.\n",
     " * «إزالة» of a saved space that left the directory (C7): named «إزالة {name} من المفضّلة», sent once,\n * said with no «تراجع» — the API saves no space out of the directory (404), so an undo could never\n * work (DI-58, the owner's word); held until the favourites are read again, when its row leaves.\n"),
    ("  const heart = useFavoriteToggle({ space, saved: true, signIn: NO_SIGN_IN, manage });",
     "  const heart = useFavoriteToggle({ space, saved: true, signIn: NO_SIGN_IN, manage, say: 'left' });"),
])
