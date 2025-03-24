from .base_page import BasePage
from playwright.sync_api import Page

class ExamplePage(BasePage):
    # Selectors
    HEADING = "h1"
    PARAGRAPH = "p"
    MORE_INFO_LINK = "a"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://example.com"

    def navigate_to_home(self) -> None:
        """Navigate to the example.com homepage."""
        self.navigate(self.url)

    def get_main_heading(self) -> str:
        """Get the main heading text."""
        return self.get_text(self.HEADING)

    def get_main_paragraph(self) -> str:
        """Get the main paragraph text."""
        return self.get_text(self.PARAGRAPH)

    def click_more_info(self) -> None:
        """Click the 'More information' link."""
        self.click(self.MORE_INFO_LINK)

    def verify_page_loaded(self) -> bool:
        """Verify that the page has loaded successfully."""
        return (
            self.is_element_visible(self.HEADING) and
            self.is_element_visible(self.PARAGRAPH) and
            self.is_element_visible(self.MORE_INFO_LINK)
        )

    def verify_responsive_elements(self) -> dict:
        """Verify responsive elements are displayed correctly."""
        viewport = self.get_viewport_size()
        return {
            'viewport': viewport,
            'heading_visible': self.is_element_visible(self.HEADING),
            'paragraph_visible': self.is_element_visible(self.PARAGRAPH),
            'link_visible': self.is_element_visible(self.MORE_INFO_LINK)
        } 