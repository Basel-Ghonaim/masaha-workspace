import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { axe } from 'vitest-axe';
import { Refreshing } from '.';

function Cards({ refreshing }: { refreshing: boolean }) {
  return (
    <Refreshing refreshing={refreshing}>
      <ul aria-label="Spaces">
        <li>Focus Hub</li>
        <li>Palm Hub</li>
      </ul>
    </Refreshing>
  );
}

describe('Refreshing', () => {
  it('marks its list busy and dimmed while it refreshes', () => {
    const { container } = render(<Cards refreshing />);

    const wrapper = container.querySelector('[data-slot="refreshing"]');
    expect(wrapper).toHaveAttribute('aria-busy', 'true');
    expect(wrapper).toHaveAttribute('data-refreshing');
    expect(wrapper).toHaveClass('data-refreshing:opacity-(--refreshing)');
    expect(screen.getByRole('listitem', { name: '' , hidden: false })).toBeDefined();
  });
});
