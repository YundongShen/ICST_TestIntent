import { test, expect } from '@playwright/test';

test.describe('Content Security Policy', () => {

  test('page loads without CSP violations', async ({ page }) => {
    const violations: string[] = [];
    page.on('console', msg => {
      if (msg.text().includes('Content-Security-Policy') || msg.text().includes('CSP')) {
        violations.push(msg.text());
      }
    });
    page.on('pageerror', err => {
      violations.push(err.message);
    });

    await page.goto('/');
    await page.waitForSelector('[data-testid="items-container"]');

    // Give time for any async CSP violations
    await page.waitForTimeout(500);
    expect(violations).toHaveLength(0);
  });

});
