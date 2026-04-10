import { defineConfig, devices } from '@playwright/test';

/**
 * 阅读 Playwright 测试配置文档：
 * https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './e2e',
  /* 超时设置 */
  timeout: 30 * 1000,
  expect: {
    /**
     * toEqual 等断言的超时时间
     */
    timeout: 5000
  },
  /* 并行运行测试 */
  fullyParallel: true,
  /* 每个测试文件的重试次数 */
  retries: process.env.CI ? 2 : 0,
  /* 同时运行的 worker 数量 */
  workers: process.env.CI ? 1 : undefined,
  /* 报告器 */
  reporter: 'html',
  /* 失败时跟踪录制 */
  use: {
    /* 基本 URL 用于所有测试 */
    baseURL: 'http://localhost:5173',

    /* 收集跟踪信息 */
    trace: 'on-first-retry',

    /* 失败时录制视频 */
    video: 'on-first-retry',

    /* 失败时截图 */
    screenshot: 'only-on-failure'
  },

  /* 配置项目用于不同浏览器 */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },

    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },

    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },

    /* 移动设备测试 */
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] }
    }
  ],

  /* 运行开发服务器 */
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000
  }
});
