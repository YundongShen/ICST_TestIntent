import { expect, test } from '@playwright/test'
import compareVersions from 'semver/functions/compare'
import { electronTest } from './helpers'

declare const window: { api: typeof import('../src/preload/api').default }

electronTest('renders the first page', async (app, page) => {
  await expect(page).toHaveTitle('Heroic Games Launcher')
})
