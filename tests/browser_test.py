"""Browser regressions; run against a local server or PREVIEW_URL."""
import os
import unittest
from playwright.sync_api import sync_playwright


class BrowserTests(unittest.TestCase):
    def setUp(self):
        self.pw = sync_playwright().start()
        options = {"headless": True}
        if os.environ.get("CHROME_PATH"):
            options["executable_path"] = os.environ["CHROME_PATH"]
        self.browser = self.pw.chromium.launch(**options)
        self.page = self.browser.new_page(viewport={"width": 1440, "height": 900})
        self.page.goto(os.environ.get("PREVIEW_URL", "http://127.0.0.1:8765/"))
        self.page.wait_for_function("Boolean(window.gsap && window.ScrollTrigger)")

    def tearDown(self):
        self.browser.close()
        self.pw.stop()

    def test_active_stage_link_is_clickable_and_hidden_stages_are_inert(self):
        self.page.evaluate("window.scrollTo(0, document.querySelector('.story').offsetTop + 4 * innerHeight + 10)")
        self.page.wait_for_timeout(900)
        link = self.page.locator('.stage.active .cta')
        self.assertEqual(link.count(), 1)
        self.assertEqual(link.evaluate("e => getComputedStyle(e).pointerEvents"), 'auto')
        self.assertTrue(self.page.locator('.stage:not(.active)').evaluate_all('els => els.every(e => e.inert)'))
        link.click()
        self.assertTrue(self.page.url.endswith('#kontakt'))

    def test_model_cards_fit_phone_tablet_and_desktop(self):
        for width in (390, 768, 1024, 1440):
            with self.subTest(width=width):
                self.page.set_viewport_size({"width": width, "height": 900})
                self.assertTrue(self.page.locator('.timeline-card, .platform-buttons a').evaluate_all(
                    'els => els.every(e => {const r=e.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth + 1;})'
                ))

    def test_form_controls_have_readable_font(self):
        for width in (390, 768, 1024, 1440):
            with self.subTest(width=width):
                self.page.set_viewport_size({"width": width, "height": 900})
                self.assertTrue(self.page.locator('#projectForm input, #projectForm textarea').evaluate_all(
                    'els => els.every(e => parseFloat(getComputedStyle(e).fontSize) >= 16)'
                ))

    def test_mobile_menu_contains_focus_and_restores_it(self):
        self.page.set_viewport_size({"width": 390, "height": 900})
        toggle = self.page.locator('.menu-toggle')
        toggle.click()
        toggle.focus()
        for _ in range(18):
            self.page.keyboard.press('Tab')
            self.assertTrue(self.page.evaluate("document.activeElement.matches('.menu-toggle, #mainNav a')"))
        for _ in range(10):
            self.page.keyboard.press('Shift+Tab')
            self.assertTrue(self.page.evaluate("document.activeElement.matches('.menu-toggle, #mainNav a')"))
        self.assertTrue(self.page.locator('main').evaluate('e => e.inert'))
        self.page.keyboard.press('Escape')
        self.assertEqual(toggle.get_attribute('aria-expanded'), 'false')
        self.assertTrue(toggle.evaluate('e => e === document.activeElement'))
        self.assertFalse(self.page.locator('main').evaluate('e => e.inert'))
        toggle.click()
        self.page.locator('#mainNav a[href="#kontakt"]').click()
        self.assertEqual(toggle.get_attribute('aria-expanded'), 'false')
        self.assertFalse(self.page.locator('main').evaluate('e => e.inert'))
        toggle.click()
        self.page.set_viewport_size({"width": 1440, "height": 900})
        self.page.wait_for_timeout(100)
        self.assertEqual(toggle.get_attribute('aria-expanded'), 'false')
        self.assertFalse(self.page.locator('main').evaluate('e => e.inert'))

    def test_reduced_motion_keeps_all_stages_accessible(self):
        self.page.emulate_media(reduced_motion='reduce')
        self.page.reload()
        self.assertTrue(self.page.locator('.stage').evaluate_all(
            "els => els.every(e => !e.inert && getComputedStyle(e).opacity === '1')"
        ))
        self.page.locator('.stage .cta').click()
        self.assertTrue(self.page.url.endswith('#kontakt'))


if __name__ == '__main__':
    unittest.main()
