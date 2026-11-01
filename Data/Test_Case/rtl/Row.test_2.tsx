import { render, screen, cleanup } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, afterEach } from 'bun:test';

import Row from './Row';

describe('Row', () => {
  afterEach(cleanup);

  it('re-calculates when the unit is changed', async () => {
    render(<Row scale={1} />);
    const input = screen.getByRole('spinbutton');
    await userEvent.type(input, '1');

    // The initial result should be 116.0 g (1 * 116.0)
    expect(await screen.findByText(/116.0 g/i)).not.toBeNull();

    // Change the unit to Ounce (value: 8)
    const unitSelect = screen.getAllByRole('combobox')[0];
    await userEvent.click(unitSelect);
    await userEvent.click(await screen.findByText('Ounce'));

    // The new result should be 14.5 g (116.0 / 8)
    expect(await screen.findByText(/14.5 g/i)).not.toBeNull();
  });

});
