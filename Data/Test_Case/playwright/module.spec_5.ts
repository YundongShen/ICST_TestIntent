import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/');
});

test.describe('Bootstrap 4', () => {

	test.describe('Modal', () => {

		test('should have button to launch modal', async ({ page }) => {
			const button = page.locator('text=Launch demo modal');
			expect(button).toBeDefined();
		});

	});
});
