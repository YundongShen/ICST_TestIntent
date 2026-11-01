import { test, expect } from '@playwright/test';

test('exports as "globus"', async ({ page }) => {
  await page.goto('umd');
  await expect(page).toHaveTitle('@globus/sdk');

  expect(await page.evaluate(() => window.globus.logger)).toBeDefined();
  expect(await page.evaluate(() => window.globus.authorization)).toBeDefined();

  expect(await page.evaluate(() => window.globus)).toBeDefined();
  expect(await page.evaluate(() => window.globus.auth)).toBeDefined();
  expect(await page.evaluate(() => window.globus.transfer)).toBeDefined();
  expect(await page.evaluate(() => window.globus.search)).toBeDefined();
  expect(await page.evaluate(() => window.globus.flows)).toBeDefined();
  expect(await page.evaluate(() => window.globus.gcs)).toBeDefined();
  expect(await page.evaluate(() => window.globus.timers)).toBeDefined();
  expect(await page.evaluate(() => window.globus.compute)).toBeDefined();

  expect(await page.evaluate(() => window.globus.webapp)).toBeDefined();
});

/**
 * Basic E2E test to validate the creation of a AuthorizationManager and
 * its ability to initiate the OAuth flow.
 */
