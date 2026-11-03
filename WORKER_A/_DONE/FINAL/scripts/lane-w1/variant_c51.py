W = 'apps/web/src/'
O = W + 'features/overview/'
PLAIN = [
    O + 'repository/overviewRepository.ts',
    O + 'repository/overviewRepository.unit.test.ts',
    O + 'hooks/queryKeys.ts',
    O + 'hooks/useLoadFailure.ts',
    O + 'hooks/useLoadFailure.component.test.tsx',
    O + 'hooks/owner/useOwnerOverviewQuery.ts',
    O + 'hooks/owner/useOwnerOverview.ts',
    O + 'services/attentionRows.ts',
    O + 'services/endsText.ts',
    O + 'types/OwnerOverviewLinks.ts',
    O + 'types/AttentionRowView.ts',
    O + 'components/LoadFailure.tsx',
    O + 'components/owner/OwnerOverview.tsx',
    O + 'components/owner/OwnerOverview.component.test.tsx',
    O + 'components/owner/AttentionCard.tsx',
    O + 'components/owner/PresentCard.tsx',
    O + 'components/owner/EndingCard.tsx',
    W + 'pages/dashboard/space/overview/OverviewPage.tsx',
    W + 'pages/dashboard/space/overview/OverviewPage.component.test.tsx',
    'docs/features/overview.md',
]


def no_admin_index(text):
    return ''.join(
        line for line in text.splitlines(keepends=True) if 'Admin' not in line
    )


def no_admin_copy(text):
    start = text.index("  /** The admin's overview") if "  /** The admin's overview" in text else text.index('  admin: {')
    end = text.rindex('} ')
    return text[:start] + text[end:]


def no_admin_routes(text):
    a = text.index("/** The admin's overview of a quiet platform")
    b = text.index('/**\n * Signs in a user (id 1)')
    text = text[:a] + text[b:]
    line = "    if (request.url?.endsWith('/admin/overview') === true) return ok(QUIET_ADMIN_OVERVIEW);\n"
    assert text.count(line) == 1
    return text.replace(line, '')


VARIANTS = {
    O + 'index.ts': no_admin_index,
    W + 'shared/copy/english/overview.ts': no_admin_copy,
    W + 'shared/copy/arabic/overview.ts': no_admin_copy,
    W + 'pages/dashboard/routes.component.test.tsx': no_admin_routes,
}
