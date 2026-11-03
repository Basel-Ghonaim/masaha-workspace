import sys
def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
LOST = "query.error?.type === 'network' || query.error?.type === 'timeout'"
# occupancy: usePresentList
edit('features/occupancy/hooks/now/usePresentList.ts', [
("""      : data === undefined
        ? ('failed' as const)
        : people.length === 0""","""      : data === undefined
        ? query.error?.type === 'network' || query.error?.type === 'timeout'
          ? ('offline' as const)
          : ('failed' as const)
        : people.length === 0"""),
("""    empty: { title: words.empty.title, text: words.empty.text },""","""    empty: { title: words.empty.title, text: words.empty.text },
    // No answer at all: the connection's state (P7), not a refusal.
    offline: { title: copy.status.offline.title, text: copy.status.offline.description },"""),
])
edit('features/occupancy/components/PresentList.tsx', [
("""  EmptyState,
} from '@shared/design-system';""","""  EmptyState,
  WifiOffIcon,
} from '@shared/design-system';"""),
("""      {list.state === 'failed' ? (""","""      {list.state === 'offline' ? (
        <EmptyState icon={<WifiOffIcon />} title={list.offline.title} description={list.offline.text}>
          <Button variant="outline" onClick={list.failure.retry}>
            {list.failure.retryLabel}
          </Button>
        </EmptyState>
      ) : list.state === 'failed' ? ("""),
(""" * as their subscription's progress. The list is read""",""" * as their subscription's progress. No answer at all draws the offline state (P7). The list is read"""),
])
# desk: search
edit('features/desk/hooks/search/useDeskSearch.ts', [
("""        : answer === undefined
          ? ('failed' as const)
          : ('ready' as const);""","""        : answer === undefined
          ? query.error?.type === 'network' || query.error?.type === 'timeout'
            ? ('offline' as const)
            : ('failed' as const)
          : ('ready' as const);"""),
("""      busy: query.isPlaceholderData,
      failure: {""","""      busy: query.isPlaceholderData,
      // No answer at all: the connection's state (P7), not a refusal.
      offline: { title: copy.status.offline.title, text: copy.status.offline.description },
      failure: {"""),
])
edit('features/desk/components/search/DeskSearch.tsx', [
("""  Skeleton,
} from '@shared/design-system';""","""  Skeleton,
  WifiOffIcon,
} from '@shared/design-system';"""),
("""        {customers.state === 'failed' && (""","""        {customers.state === 'offline' && (
          <EmptyState
            icon={<WifiOffIcon />}
            title={customers.offline.title}
            description={customers.offline.text}
          >
            <Button variant="outline" onClick={customers.failure.retry}>
              {customers.failure.retryLabel}
            </Button>
          </EmptyState>
        )}
        {customers.state === 'failed' && ("""),
])
# desk: uncollected
edit('features/desk/hooks/uncollected/useUncollectedCard.ts', [
("""    title: words.title({ count: total }),""","""    // With none, the card keeps its name and says so once, in its line (G13.3).
    title: answer !== undefined && total === 0 ? words.heading : words.title({ count: total }),"""),
("""        : answer === undefined
          ? ('failed' as const)
          : total === 0""","""        : answer === undefined
          ? query.error?.type === 'network' || query.error?.type === 'timeout'
            ? ('offline' as const)
            : ('failed' as const)
          : total === 0"""),
("""    empty: words.none,""","""    empty: words.none,
    // No answer at all: the connection's state (P7), not a refusal.
    offline: { title: copy.status.offline.title, text: copy.status.offline.description },"""),
])
edit('features/desk/components/uncollected/UncollectedCard.tsx', [
("""  CardTitle,
  Skeleton,
} from '@shared/design-system';""","""  CardTitle,
  CircleCheckIcon,
  EmptyState,
  Skeleton,
  WifiOffIcon,
} from '@shared/design-system';"""),
("""    <Card id={card.id} role="region" aria-labelledby={headingId}>""","""    // Empty, it is hidden below xl, where it would stand above who is here with nothing (G13.3).
    <Card
      id={card.id}
      role="region"
      aria-labelledby={headingId}
      className={card.state === 'empty' ? 'hidden xl:flex' : undefined}
    >"""),
("""      ) : card.state === 'failed' ? (""","""      ) : card.state === 'offline' ? (
        <CardContent>
          <EmptyState
            icon={<WifiOffIcon />}
            title={card.offline.title}
            titleAs="h3"
            description={card.offline.text}
          >
            <Button variant="outline" onClick={card.failure.retry}>
              {card.failure.retryLabel}
            </Button>
          </EmptyState>
        </CardContent>
      ) : card.state === 'failed' ? ("""),
("""          <p className="text-body-sm text-muted-foreground">{card.empty}</p>""","""          <p className="flex items-center gap-2 text-body-sm text-muted-foreground">
            <CircleCheckIcon aria-hidden className="size-4 text-success" />
            {card.empty}
          </p>"""),
])
# copy
edit('shared/copy/arabic/desk.ts', [("""    none: 'لا توجد مبالغ غير محصّلة.',""","""    heading: 'غير محصّل',
    none: 'لا توجد مبالغ غير محصّلة.',""")])
edit('shared/copy/english/desk.ts', [("""    none: 'Nothing left to collect.',""","""    /** The card's name when it holds none: its line says so (G13.3). */
    heading: 'Not collected',
    none: 'Nothing left to collect.',""")])
# page order
edit('pages/dashboard/space/desk/DeskPage.tsx', [
("""      <div className="flex flex-col gap-6 xl:grid xl:grid-cols-12 xl:items-start">
        <div className="xl:col-span-8">""","""      {/* On a phone the uncollected come before who is here (K1); the grid places them from xl. */}
      <div className="flex flex-col gap-6 xl:grid xl:grid-cols-12 xl:items-start">
        <div className="flex flex-col gap-6 xl:order-last xl:col-span-4">
          <UncollectedCard spaceId={spaceId} abilities={{ writeOff: owner }} />
          <UnpricedCard spaceId={spaceId} mayTypePrice={terms.data?.mayTypePrice ?? false} />
        </div>
        <div className="xl:col-span-8">"""),
("""          </Tabs>
        </div>
        <div className="flex flex-col gap-6 xl:col-span-4">
          <UncollectedCard spaceId={spaceId} abilities={{ writeOff: owner }} />
          <UnpricedCard spaceId={spaceId} mayTypePrice={terms.data?.mayTypePrice ?? false} />
        </div>
      </div>""","""          </Tabs>
        </div>
      </div>"""),
])
