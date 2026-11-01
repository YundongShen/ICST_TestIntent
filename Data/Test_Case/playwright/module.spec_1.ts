import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/');
});

test.describe('Bootstrap 4', () => {
	test('should initially hide page content', async ({ page }) => {
		await expect(page.locator('body')).toBeHidden();
	});

});
