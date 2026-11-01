import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/');
});

test.describe('Bootstrap 4', () => {

	test('should style alert messages', async ({ page }) => {
		const alert = page.locator('.alert-primary').first();
		const initialColor = await alert.evaluate((el) => {
			return getComputedStyle(el).backgroundColor;
		});
		await page.waitForResponse(
			'https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css'
		);
		const styledColor = await alert.evaluate((el) => getComputedStyle(el).backgroundColor);
		expect(styledColor !== initialColor);
	});

});
