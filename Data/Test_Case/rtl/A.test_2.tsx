import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, it } from 'vitest';
import A from './A';

it('should warn upon missing href', async () => {
  const mockedwarn = (o: string) => {
    expect(o).toEqual('missing href');
    return o;
  };
  console.warn = mockedwarn;
  render(<A>click link</A>);
});
