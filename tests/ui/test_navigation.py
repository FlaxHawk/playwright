import pytest
from pages.example_page import ExamplePage
import time

@pytest.mark.ui
@pytest.mark.navigation
class TestNavigation:
    def test_navigate_to_homepage(self, page):
        """Test navigation to the homepage."""
        example_page = ExamplePage(page)
        example_page.navigate_to_home()
        
        assert example_page.verify_page_loaded(), "Homepage failed to load properly"
        assert "Example Domain" in example_page.get_title(), "Page title is incorrect"

    def test_click_more_info(self, page):
        """Test clicking the 'More information' link."""
        example_page = ExamplePage(page)
        example_page.navigate_to_home()
        example_page.click_more_info()
        
        # Wait for navigation to complete
        example_page.wait_for_navigation()
        
        # Verify we've navigated to the IANA page
        assert "iana.org" in example_page.get_url(), "Navigation to IANA page failed"

    @pytest.mark.parametrize("expected_text", [
        "Example Domain",
        "This domain is for use in illustrative examples in documents."
    ])
    def test_verify_page_content(self, page, expected_text):
        """Test that the page contains expected content."""
        example_page = ExamplePage(page)
        example_page.navigate_to_home()
        
        assert expected_text in page.content(), f"Expected text '{expected_text}' not found on page"

    def test_page_load_performance(self, page):
        """Test page load performance."""
        example_page = ExamplePage(page)
        
        # Measure page load time
        start_time = time.time()
        example_page.navigate_to_home()
        example_page.wait_for_navigation()
        load_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Page load should be less than 5 seconds
        assert load_time < 5000, f"Page load took too long: {load_time:.2f}ms" 