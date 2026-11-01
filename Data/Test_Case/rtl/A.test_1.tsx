import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, it } from 'vitest';
import A from './A';

it('should render a link', () => {
  render(<A data-testid="a.link">Link</A>);
  expect(screen.getByTestId('a.link')).toContainHTML('Link');
});
