import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, it } from 'vitest';
import A from './A';

it('should trigger click', async () => {
  let io = 0;
  const onClick = () => {
    io = 1;
    expect(io).toBeTruthy();
  };
  render(
    <A
      data-testid="a.clickme"
      onClick={onClick}
    >
      click
    </A>,
  );
  await userEvent.click(screen.getByTestId('a.clickme'));
});
