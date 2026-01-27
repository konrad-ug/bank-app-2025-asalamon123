import { test, expect } from '@playwright/test';
import { UniPage } from './pages/UniPage';

test('has title', async ({ page }) => {

  await page.goto('https://mfi.ug.edu.pl/');

  const uniPage = new UniPage(page)

  await uniPage.searchHeader.click()

  await uniPage.searchStaff.click()

  await uniPage.searchName.fill("sołtys")

  await uniPage.searchButton.click()

  await uniPage.linkName.click()

  await expect(uniPage.searchRoom).toBeVisible()
});
