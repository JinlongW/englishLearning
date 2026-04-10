import { test, expect } from '@playwright/test';

test.describe('英语学习工具 - 首页功能', () => {
  test.beforeEach(async ({ page }) => {
    // 访问首页
    await page.goto('/');
  });

  test('应该显示首页主要内容', async ({ page }) => {
    // 检查今日打卡区域
    await expect(page.locator('.checkin-section')).toBeVisible();

    // 检查学习统计卡片
    await expect(page.locator('.stats-section')).toBeVisible();

    // 检查快捷入口
    await expect(page.locator('.quick-actions')).toBeVisible();
  });

  test('应该能够点击学单词', async ({ page }) => {
    await page.click('text=学单词');
    await expect(page).toHaveURL('/words', { timeout: 5000 });
  });

  test('应该能够点击学语法', async ({ page }) => {
    await page.click('text=学语法');
    await expect(page).toHaveURL('/grammar', { timeout: 5000 });
  });

  test('应该能够点击每日挑战', async ({ page }) => {
    await page.click('text=每日挑战');
    await expect(page).toHaveURL('/challenge', { timeout: 5000 });
  });

  test('应该能够点击错题本', async ({ page }) => {
    await page.click('text=错题本');
    await expect(page).toHaveURL('/wrong-questions', { timeout: 5000 });
  });
});
