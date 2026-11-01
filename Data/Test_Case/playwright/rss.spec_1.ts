import { expect, test } from "@playwright/test";
import { XMLValidator } from 'fast-xml-parser';

test("should have a link to the RSS feed", async ({ page }) => {
  await page.goto("/");

  const rss = await page.getByRole("link", { name: "RSS" });
  expect(rss).toBeTruthy();
});
