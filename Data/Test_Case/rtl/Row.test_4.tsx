import { render, screen, cleanup } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, afterEach } from 'bun:test';

import Row from './Row';

describe('Row', () => {
  afterEach(cleanup);

  it('applies the scale prop correctly', async () => {
    render(<Row scale={2} />);
    const input = screen.getByRole('spinbutton');
    await userEvent.type(input, '1');

    // The result should be 232.0 g (1 * 116.0 * 2)
    expect(await screen.findByText(/232.0 g/i)).not.toBeNull();
  });
});
