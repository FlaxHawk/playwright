import pytest
import allure
from pages.herokuapp_page import HerokuappPage
import os
from typing import Generator

@pytest.fixture
def herokuapp(page) -> Generator[HerokuappPage, None, None]:
    """Fixture to create HerokuappPage instance."""
    page_instance = HerokuappPage(page)
    page_instance.navigate_to_home()
    yield page_instance

@allure.epic("Herokuapp Test Suite")
@pytest.mark.auth
class TestAuthentication:
    @allure.title("Test successful login with valid credentials")
    def test_successful_login(self, herokuapp):
        """
        Test Steps:
        1. Navigate to login page
        2. Enter valid username and password
        3. Click login button
        4. Verify successful login
        """
        with allure.step("Login with valid credentials (tomsmith/SuperSecretPassword!)"):
            herokuapp.login("tomsmith", "SuperSecretPassword!")
        
        with allure.step("Verify user is on secure page"):
            assert herokuapp.verify_secure_page()
        
        with allure.step("Verify success message is displayed"):
            assert "You logged into a secure area!" in herokuapp.get_flash_message()

    @allure.title("Test login failure with invalid credentials")
    def test_failed_login(self, herokuapp):
        """
        Test Steps:
        1. Navigate to login page
        2. Enter invalid credentials
        3. Verify error message
        """
        with allure.step("Attempt login with invalid credentials"):
            herokuapp.login("invalid", "invalid")
        
        with allure.step("Verify error message is displayed"):
            assert "Your username is invalid!" in herokuapp.get_flash_message()

@allure.epic("Herokuapp Test Suite")
@pytest.mark.dynamic
class TestDynamicLoading:
    @allure.title("Test waiting for dynamically loaded element")
    def test_wait_for_element(self, herokuapp):
        """
        Test Steps:
        1. Navigate to Dynamic Loading page
        2. Click start button
        3. Wait for loading to complete
        4. Verify loaded text
        """
        with allure.step("Wait for dynamically loaded text"):
            text = herokuapp.wait_for_dynamic_text()
        
        with allure.step("Verify loaded text matches expected"):
            assert text == "Hello World!"

@allure.epic("Herokuapp Test Suite")
@pytest.mark.checkboxes
class TestCheckboxes:
    @allure.title("Test checkbox interactions")
    def test_toggle_checkboxes(self, herokuapp):
        """
        Test Steps:
        1. Navigate to Checkboxes page
        2. Toggle first checkbox and verify state
        3. Verify second checkbox default state
        4. Toggle second checkbox and verify state
        """
        with allure.step("Toggle first checkbox"):
            herokuapp.toggle_checkbox(0)
            assert herokuapp.is_checkbox_checked(0)
        
        with allure.step("Verify second checkbox is checked by default"):
            assert herokuapp.is_checkbox_checked(1)
        
        with allure.step("Toggle second checkbox"):
            herokuapp.toggle_checkbox(1)
            assert not herokuapp.is_checkbox_checked(1)

@allure.epic("Herokuapp Test Suite")
@pytest.mark.dragdrop
class TestDragAndDrop:
    @allure.title("Test drag and drop functionality")
    def test_drag_and_drop(self, herokuapp):
        """
        Test Steps:
        1. Navigate to Drag and Drop page
        2. Perform drag and drop operation
        """
        with allure.step("Perform drag and drop operation"):
            herokuapp.perform_drag_and_drop()

@allure.epic("Herokuapp Test Suite")
@pytest.mark.upload
class TestFileUpload:
    @allure.title("Test file upload functionality")
    def test_file_upload(self, herokuapp, tmp_path):
        """
        Test Steps:
        1. Navigate to File Upload page
        2. Create test file
        3. Upload file
        4. Verify upload success
        """
        with allure.step("Create temporary test file"):
            test_file = tmp_path / "test.txt"
            test_file.write_text("Hello, World!")
        
        with allure.step("Upload file"):
            herokuapp.upload_file(str(test_file))
        
        with allure.step("Verify file upload success message"):
            assert "File Uploaded!" in herokuapp.get_text("h3")

@allure.epic("Herokuapp Test Suite")
@pytest.mark.frames
class TestFrames:
    @allure.title("Test iframe text editor interaction")
    def test_iframe_interaction(self, herokuapp):
        """
        Test Steps:
        1. Navigate to Frames page
        2. Switch to iframe
        3. Type text in editor
        """
        test_text = "Hello from Playwright!"
        with allure.step(f"Type text in iframe editor: {test_text}"):
            herokuapp.switch_to_frame_and_type(test_text)

@allure.epic("Herokuapp Test Suite")
@pytest.mark.alerts
class TestJavaScriptAlerts:
    @allure.title("Test simple JavaScript alert")
    def test_simple_alert(self, herokuapp):
        """
        Test Steps:
        1. Navigate to JavaScript Alerts page
        2. Trigger simple alert
        3. Accept alert
        4. Verify result
        """
        with allure.step("Handle simple alert"):
            result = herokuapp.handle_javascript_alert("alert")
        
        with allure.step("Verify alert handling result"):
            assert "You successfully clicked an alert" in result

    @allure.title("Test JavaScript confirm dialog")
    def test_confirm_alert(self, herokuapp):
        """
        Test Steps:
        1. Navigate to JavaScript Alerts page
        2. Trigger confirm dialog
        3. Accept dialog
        4. Verify result
        """
        with allure.step("Handle confirm dialog"):
            result = herokuapp.handle_javascript_alert("confirm")
        
        with allure.step("Verify confirm dialog handling result"):
            assert "You clicked: Ok" in result

    @allure.title("Test JavaScript prompt dialog")
    def test_prompt_alert(self, herokuapp):
        """
        Test Steps:
        1. Navigate to JavaScript Alerts page
        2. Trigger prompt dialog
        3. Enter text and accept
        4. Verify result
        """
        test_text = "Playwright Test"
        with allure.step(f"Handle prompt dialog with input: {test_text}"):
            result = herokuapp.handle_javascript_alert("prompt", test_text)
        
        with allure.step("Verify prompt dialog handling result"):
            assert f"You entered: {test_text}" in result

@allure.epic("Herokuapp Test Suite")
@pytest.mark.navigation
class TestNavigation:
    @allure.title("Test homepage loads successfully")
    def test_homepage_loads(self, herokuapp):
        """
        Test Steps:
        1. Navigate to homepage
        2. Verify page loaded successfully
        """
        with allure.step("Navigate to homepage"):
            herokuapp.navigate_to_home()
        
        with allure.step("Verify page loaded successfully"):
            assert herokuapp.verify_page_loaded()

    @allure.title("Test available examples are displayed")
    def test_available_examples(self, herokuapp):
        """
        Test Steps:
        1. Navigate to homepage
        2. Get list of available examples
        3. Verify examples list
        """
        with allure.step("Navigate to homepage"):
            herokuapp.navigate_to_home()
        
        with allure.step("Get list of available examples"):
            examples = herokuapp.get_available_examples()
        
        with allure.step("Verify examples list"):
            assert len(examples) > 0
            assert "Form Authentication" in examples 