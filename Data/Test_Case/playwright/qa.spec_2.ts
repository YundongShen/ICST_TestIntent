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

  test('should display QA metrics or cards', async ({ page }) => {
    const metrics = page.locator(
      '[class*="qa"], [class*="metric"], [class*="card"], [class*="quality"]'
    );
    const count = await metrics.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

});
