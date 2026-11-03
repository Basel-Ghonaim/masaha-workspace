W = 'apps/web/src/'
PLAIN = [
    W + 'shared/copy/english/packages.ts',
    W + 'shared/copy/arabic/packages.ts',
    W + 'features/packages/components/list/PackageRow.tsx',
    W + 'features/packages/hooks/list/usePackagesSection.component.test.tsx',
    W + 'pages/dashboard/space/PackagesPage.tsx',
    W + 'pages/dashboard/space/PackagesPage.component.test.tsx',
    'docs/features/packages.md',
]


def no_live_test(text):
    a = text.index("  it('announces the terms and the price as they change, never the name typed'")
    b = text.rindex('});')
    return text[:a] + text[b:]


VARIANTS = {W + 'features/packages/components/PackagesSection.component.test.tsx': no_live_test}
