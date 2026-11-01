import { expect, test } from "@playwright/test";
import { XMLValidator } from 'fast-xml-parser';

test("should open rss feed in new tab", async ({ page, context }) => {
  await page.goto("/");

  const pagePromise = page.context().waitForEvent('page');

  const rss = await page.getByRole("link", { name: "RSS" });
  await rss.click();

  await pagePromise;

  const pages = await context.pages();
  await expect(pages[1]).toHaveURL("/rss.xml");
});
