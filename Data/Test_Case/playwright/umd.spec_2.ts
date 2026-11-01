import { test, expect } from '@playwright/test';

/**
 * Basic E2E test to validate the creation of a AuthorizationManager and
 * its ability to initiate the OAuth flow.
 */
test('authorization', async ({ page }) => {
  await page.goto('umd-authorization');
  await expect(page).toHaveTitle('@globus/sdk');
  await expect(page.getByRole('button')).toHaveText('Sign In');
  await page.getByRole('button').click();

  await page.waitForURL(/https:\/\/auth.globus.org\/p\/login\?.*/);

  const url = await page.url();

  expect(url).toContain('response_type=code');
  expect(url).toContain('client_id=938f3dce-6782-40e7-872d-2ef94c7b24e7');
  expect(url).toContain('scope=openid+profile+email+offline_access');
  expect(url).toContain('%26redirect_uri%3Dexample%253A%252F%252Fredirect%26');
});
