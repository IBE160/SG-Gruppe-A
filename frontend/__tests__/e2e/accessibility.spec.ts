import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Scans', () => {
  test('Landing Page should not have any automatically detectable accessibility issues', async ({ page }) => {
    await page.goto('/');
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('Login Page should not have any automatically detectable accessibility issues', async ({ page }) => {
    await page.goto('/login');
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('Authenticated pages (Dashboard, Analysis) should not have accessibility issues', async ({ page }) => {
    // 1. Login with test credentials
    // Note: This user MUST exist and be verified in the Supabase project.
    // Use 'test@example.com' / 'Password123!' or update these credentials.
    const email = 'test@example.com';
    const password = 'Password123!';

    await page.goto('/login');
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);
    await page.click('button[type="submit"]');

    // 2. Assert Login Success
    // We expect to be redirected to /dashboard (or at least NOT stay on /login).
    // Using a longer timeout to allow for network latency.
    try {
      await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 });
    } catch (error) {
      throw new Error(`Login failed for ${email}. Please ensure this user exists and is verified in your Supabase project.`);
    }
    
    // 3. Scan Dashboard
    const dashboardResults = await new AxeBuilder({ page }).analyze();
    expect(dashboardResults.violations).toEqual([]);

    // 4. Scan Analysis Page
    await page.goto('/analysis');
    // Ensure we are still authenticated
    await expect(page).toHaveURL(/\/analysis/);
    const analysisResults = await new AxeBuilder({ page }).analyze();
    expect(analysisResults.violations).toEqual([]);
  });
});
