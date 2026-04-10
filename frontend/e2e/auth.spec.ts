import { test, expect } from '@playwright/test';

test.describe('英语学习工具 - 认证流程', () => {
  test('应该能够注册新用户', async ({ page }) => {
    // 访问注册页面
    await page.goto('/login');

    // 点击注册链接
    await page.click('text=注册账户');

    // 填写注册表单
    const uniqueId = Date.now();
    await page.fill('input[name="username"]', `testuser${uniqueId}`);
    await page.fill('input[name="password"]', 'Test1234');
    await page.fill('input[name="studentName"]', '测试用户');
    await page.selectOption('select[name="gradeLevel"]', '7');

    // 提交注册
    await page.click('button[type="submit"]');

    // 等待成功提示
    await expect(page.locator('.uni-toast')).toContainText('注册成功', { timeout: 5000 });
  });

  test('应该能够登录', async ({ page }) => {
    // 访问登录页面
    await page.goto('/login');

    // 填写登录表单
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'Test1234');

    // 提交登录
    await page.click('button[type="submit"]');

    // 等待跳转到首页
    await expect(page).toHaveURL('/', { timeout: 5000 });
  });

  test('应该显示错误信息当密码错误时', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'WrongPassword');

    await page.click('button[type="submit"]');

    // 等待错误提示
    await expect(page.locator('.uni-toast')).toContainText('密码', { timeout: 5000 });
  });
});
