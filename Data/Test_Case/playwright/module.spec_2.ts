import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/');
});

test.describe('Bootstrap 4', () => {

	test('should eventually display page content', async ({ page }) => {
		await expect(page.locator('body')).toBeVisible();
	});

});
