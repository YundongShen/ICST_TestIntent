import { test, expect } from "@playwright/test";

test.describe("/", () => {

	test("navigate to login", async ({ page }) => {
		await page.goto("/");
		await page.click("text=Login");

		await expect(page).toHaveURL("/-login");
	});

});
