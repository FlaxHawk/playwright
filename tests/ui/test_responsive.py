import pytest
from pages.example_page import ExamplePage

@pytest.mark.ui
@pytest.mark.responsive
class TestResponsive:
    def test_responsive_elements_visibility(self, responsive_page):
        """Test that elements are visible across different viewport sizes."""
        example_page = ExamplePage(responsive_page)
        example_page.navigate_to_home()
        
        # Verify elements are visible in current viewport
        responsive_check = example_page.verify_responsive_elements()
        
        assert responsive_check['heading_visible'], f"Heading not visible at viewport size {responsive_check['viewport']}"
        assert responsive_check['paragraph_visible'], f"Paragraph not visible at viewport size {responsive_check['viewport']}"
        assert responsive_check['link_visible'], f"Link not visible at viewport size {responsive_check['viewport']}"

    def test_content_readability(self, responsive_page):
        """Test that content remains readable across different viewport sizes."""
        example_page = ExamplePage(responsive_page)
        example_page.navigate_to_home()
        
        # Get the main heading and paragraph
        heading = example_page.get_main_heading()
        paragraph = example_page.get_main_paragraph()
        
        # Verify content is not truncated
        assert len(heading) > 0, "Heading is empty or truncated"
        assert len(paragraph) > 0, "Paragraph is empty or truncated"
        
        # Verify content matches expected text
        assert "Example Domain" in heading, "Heading content is incorrect"
        assert "illustrative examples" in paragraph, "Paragraph content is incorrect"

    @pytest.mark.parametrize("element_selector", [
        ExamplePage.HEADING,
        ExamplePage.PARAGRAPH,
        ExamplePage.MORE_INFO_LINK
    ])
    def test_element_positioning(self, responsive_page, element_selector):
        """Test that elements maintain proper positioning across viewport sizes."""
        example_page = ExamplePage(responsive_page)
        example_page.navigate_to_home()
        
        # Verify element is visible
        assert example_page.is_element_visible(element_selector), f"Element {element_selector} not visible"
        
        # Get element position
        element = responsive_page.query_selector(element_selector)
        bbox = element.bounding_box()
        
        # Verify element is within viewport
        viewport = example_page.get_viewport_size()
        assert bbox['x'] >= 0, f"Element {element_selector} positioned outside left viewport"
        assert bbox['y'] >= 0, f"Element {element_selector} positioned outside top viewport"
        assert bbox['x'] + bbox['width'] <= viewport['width'], f"Element {element_selector} positioned outside right viewport"
        assert bbox['y'] + bbox['height'] <= viewport['height'], f"Element {element_selector} positioned outside bottom viewport" 