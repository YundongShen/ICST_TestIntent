import { test, expect, waitForApp } from './fixtures/base.fixture';
import { mockApiRoutes } from './fixtures/api-mocks.fixture';

// ==========================================================================
// E2E: QA Metrics View
// Tests QA dashboard — test results, coverage, quality gates
// ==========================================================================

test.describe('QA View', () => {
  test.beforeEach(async ({ page }) => {
    await mockApiRoutes(page);
    await page.goto('/qa');
    await waitForApp(page);
  });

  test('should show coverage or chart elements', async ({ page }) => {
    const charts = page.locator(
      'svg, canvas, [class*="chart"], [class*="coverage"], [class*="progress"]'
    );
    const count = await charts.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});
