import { test, expect } from "@playwright/test";

test.describe("/", () => {
	test("navigation", async ({ page }) => {
		await page.goto("/");

		await expect(page.getByRole("navigation")).toContainText("SPARQList");
		await expect(page.getByRole("link", { name: "Login" })).toBeVisible();
	});

});
