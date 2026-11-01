import { test, expect } from '@playwright/test';

test.describe('Content Security Policy', () => {

  test('no inline styles in served HTML', async ({ request }) => {
    const res = await request.get('/');
    const html = await res.text();
    // Only check body content, not SVG attributes
    const bodyMatch = html.match(/<body[\s\S]*<\/body>/);
    const body = bodyMatch?.[0] || '';
    // Should not have style= attributes (except in SVG which use presentation attributes)
    const inlineStyles = body.match(/ style="/g);
    expect(inlineStyles).toBeNull();
  });
});
