import { test, expect } from "@playwright/test";

test("users can see the list of all posts", async ({ page }) => {
  await page.goto("http://localhost:3000/");

  await expect(page).toHaveTitle("simple-remix-blog");

  await page.getByRole("link", { name: "Blog" }).click();
  await expect(page).toHaveURL("http://localhost:3000/blog");
  await expect(page.getByText("All posts")).toBeVisible();
  expect(await page.getByText("Read more").count()).toBe(4);
});
