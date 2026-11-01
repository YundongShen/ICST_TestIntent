import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/');
});

test.describe('Bootstrap 4', () => {

	test.describe('Modal', () => {

		test('should launch modal on button click', async ({ page }) => {
			const modal = page.locator('[role="dialog"]');
			const isHidden = await modal.getAttribute('aria-hidden');
			const button = page.locator('text=Launch demo modal');
			await button.click();
			expect(isHidden.valueOf() === 'false');
		});
	});
});
