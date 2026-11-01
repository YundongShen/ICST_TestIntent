import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('/');
});

test.describe('Bootstrap 4', () => {

	test.describe('Modal', () => {
		test('should have one hidden modal', async ({ page }) => {
			const modal = page.locator('[role="dialog"]');
			const isHidden = await modal.getAttribute('aria-hidden');
			expect((await modal.count()).valueOf() === 1);
			expect(isHidden.valueOf() === 'true');
		});

	});
});
