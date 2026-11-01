import { test, expect } from '@playwright/test';

test.describe('Content Security Policy', () => {
  test('server returns strict CSP header', async ({ page }) => {
    const response = await page.goto('/');
    expect(response).not.toBeNull();
    const headers = response!.headers();
    const csp = headers['content-security-policy'];
    expect(csp).toBeDefined();
    expect(csp).toContain("default-src 'none'");
    expect(csp).toContain("script-src 'self'");
    expect(csp).toContain("style-src 'self'");
    expect(csp).toContain("img-src 'self' data:");
    expect(csp).toContain("frame-src blob:");
    expect(csp).toContain("object-src blob:");
    expect(csp).toContain("form-action 'none'");
  });

});
