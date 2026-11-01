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

  test('should render QA view', async ({ page }) => {
    await expect(page).toHaveURL('/qa');
    await expect(page.locator('body')).toBeVisible();
  });

});
