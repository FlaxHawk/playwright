import pytest
from pages.herokuapp_page import HerokuappPage
import os
from typing import Generator

@pytest.fixture
def herokuapp(page) -> Generator[HerokuappPage, None, None]:
    """Fixture to create HerokuappPage instance."""
    page_instance = HerokuappPage(page)
    page_instance.navigate_to_home()
    yield page_instance

@pytest.mark.auth
class TestAuthentication:
    def test_successful_login(self, herokuapp):
        herokuapp.login("tomsmith", "SuperSecretPassword!")
        assert herokuapp.verify_secure_page()
        assert "You logged into a secure area!" in herokuapp.get_flash_message()

    def test_failed_login(self, herokuapp):
        herokuapp.login("invalid", "invalid")
        assert "Your username is invalid!" in herokuapp.get_flash_message()

@pytest.mark.dynamic
class TestDynamicLoading:
    def test_wait_for_element(self, herokuapp):
        text = herokuapp.wait_for_dynamic_text()
        assert text == "Hello World!"

@pytest.mark.checkboxes
class TestCheckboxes:
    def test_toggle_checkboxes(self, herokuapp):
        herokuapp.toggle_checkbox(0)
        assert herokuapp.is_checkbox_checked(0)
        
        # Second checkbox is checked by default
        assert herokuapp.is_checkbox_checked(1)
        herokuapp.toggle_checkbox(1)
        assert not herokuapp.is_checkbox_checked(1)

@pytest.mark.dragdrop
class TestDragAndDrop:
    def test_drag_and_drop(self, herokuapp):
        herokuapp.perform_drag_and_drop()
        # Visual verification would be needed for complete validation

@pytest.mark.upload
class TestFileUpload:
    def test_file_upload(self, herokuapp, tmp_path):
        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")
        
        herokuapp.upload_file(str(test_file))
        assert "File Uploaded!" in herokuapp.get_text("h3")

@pytest.mark.frames
class TestFrames:
    def test_iframe_interaction(self, herokuapp):
        test_text = "Hello from Playwright!"
        herokuapp.switch_to_frame_and_type(test_text)
        # The text should now be in the iframe editor

@pytest.mark.alerts
class TestJavaScriptAlerts:
    def test_simple_alert(self, herokuapp):
        result = herokuapp.handle_javascript_alert("alert")
        assert "You successfully clicked an alert" in result

    def test_confirm_alert(self, herokuapp):
        result = herokuapp.handle_javascript_alert("confirm")
        assert "You clicked: Ok" in result

    def test_prompt_alert(self, herokuapp):
        test_text = "Playwright Test"
        result = herokuapp.handle_javascript_alert("prompt", test_text)
        assert f"You entered: {test_text}" in result

@pytest.mark.navigation
class TestNavigation:
    def test_homepage_loads(self, herokuapp):
        herokuapp.navigate_to_home()
        assert herokuapp.verify_page_loaded()

    def test_available_examples(self, herokuapp):
        herokuapp.navigate_to_home()
        examples = herokuapp.get_available_examples()
        assert len(examples) > 0
        assert "Form Authentication" in examples 