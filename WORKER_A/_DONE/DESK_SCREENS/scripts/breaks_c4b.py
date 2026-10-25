"""Commit 4's check-out breaks again, on the hook as it is after the lint fixes."""
import sys
import breaks

H = 'features/desk/hooks/check-out/useCheckOutDialog.ts'
T = 'src/features/desk/hooks/check-out'
breaks.BREAKS.update({
    '23b': (H, '{ amountAgorot: money.recorded, method:', '{ amountAgorot: Number(money.amount), method:', T, 'component'),
    '24b': (H, 'if (needsDebt && !debtShown) setDebtShown(true);', 'if (needsDebt !== debtShown) setDebtShown(needsDebt);', T, 'component'),
    '25b': (H, 'if (quote !== null && quoteIsStale(quote.at, new Date())) {', 'if (quote !== null && quoteIsStale(quote.at, new Date()) && Date.now() < 0) {', T, 'component'),
    '26b': (H, '...(values.typing', '...(values.typing && Date.now() < 0', T, 'component'),
})
for name in sys.argv[1:]:
    breaks.run(name)
