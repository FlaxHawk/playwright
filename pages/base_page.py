from playwright.sync_api import Page
from typing import Optional, List

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to the specified URL."""
        self.page.goto(url)

    def get_title(self) -> str:
        """Get the page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Get the current URL."""
        return self.page.url

    def is_element_visible(self, selector: str, timeout: Optional[float] = None) -> bool:
        """Check if an element is visible."""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except:
            return False

    def click(self, selector: str) -> None:
        """Click an element."""
        self.page.click(selector)

    def fill(self, selector: str, value: str) -> None:
        """Fill a form field."""
        self.page.fill(selector, value)

    def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        return self.page.text_content(selector)

    def get_elements(self, selector: str) -> List:
        """Get all elements matching the selector."""
        return self.page.query_selector_all(selector)

    def wait_for_navigation(self) -> None:
        """Wait for navigation to complete."""
        self.page.wait_for_load_state("networkidle")

    def screenshot(self, path: str) -> None:
        """Take a screenshot."""
        self.page.screenshot(path=path)

    def get_viewport_size(self) -> dict:
        """Get the current viewport size."""
        return self.page.viewport_size 