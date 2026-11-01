import { render, screen, cleanup } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, afterEach } from 'bun:test';

import Row from './Row';

describe('Row', () => {
  afterEach(cleanup);
  it('calculates the conversion correctly on input change', async () => {
    render(<Row scale={1} />);
    const input = screen.getByRole('spinbutton');

    await userEvent.type(input, '2');

    const result = await screen.findByText(/232.0 g/i);
    expect(result).not.toBeNull();
  });

});
