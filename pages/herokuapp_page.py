from .base_page import BasePage
from playwright.sync_api import Page, expect
import re
from typing import List, Dict

class HerokuappPage(BasePage):
    """Page object for The Internet Herokuapp test site."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "http://the-internet.herokuapp.com"
        
        # Main page elements
        self.heading = "h1"
        self.subheading = "h2"
        self.footer = "#page-footer"
        
        # Navigation and links
        self.available_examples = "ul li a"
        
        # Form Authentication
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_button = "button[type='submit']"
        self.flash_message = "#flash"
        
        # Dynamic Loading
        self.start_button = "#start button"
        self.finish_text = "#finish h4"
        self.loading_indicator = "#loading"
        
        # Checkboxes
        self.checkboxes = "input[type='checkbox']"
        
        # Drag and Drop
        self.draggable = "#column-a"
        self.droppable = "#column-b"
        
        # File Upload
        self.file_upload_input = "#file-upload"
        self.upload_button = "#file-submit"
        
        # Frames
        self.iframe_link = "text=iFrame"
        self.iframe = "#mce_0_ifr"
        self.frame_content = "body#tinymce"
        
        # Alerts
        self.js_alert_button = "button[onclick='jsAlert()']"
        self.js_confirm_button = "button[onclick='jsConfirm()']"
        self.js_prompt_button = "button[onclick='jsPrompt()']"
        self.result = "#result"

        # Key Presses
        self.key_press_input = "#target"
        self.key_press_result = "#result"

        # Horizontal Slider
        self.slider = "input[type='range']"
        self.slider_value = "span#range"

        # Tables
        self.table = "#table1"
        self.table_headers = "#table1 th"
        self.table_rows = "#table1 tbody tr"
        self.table_cells = "td"

        # Status Codes
        self.status_codes = {
            200: "200",
            301: "301",
            404: "404",
            500: "500"
        }

    def navigate_to_home(self) -> None:
        """Navigate to the homepage."""
        self.navigate(self.url)
        
    def get_available_examples(self) -> List[str]:
        """Get list of available example pages."""
        elements = self.page.query_selector_all(self.available_examples)
        return [element.text_content().strip() for element in elements]
        
    def navigate_to_example(self, example_name: str) -> None:
        """Navigate to a specific example page."""
        # First try exact match
        link = self.page.get_by_text(example_name, exact=True)
        if link.count() > 0:
            link.click()
            return
            
        # Then try case-insensitive partial match with common variations
        variations = [
            example_name,
            example_name.lower(),
            example_name.title(),
            example_name.replace(" ", ""),
            "Sortable Tables" if example_name == "Sortable Data Tables" else example_name,
            "Data Tables" if example_name == "Tables" else example_name,
            "Status Codes" if example_name == "Status Code" else example_name
        ]
        
        elements = self.page.query_selector_all(self.available_examples)
        for element in elements:
            element_text = element.text_content().strip()
            if any(var.lower() in element_text.lower() for var in variations):
                element.click()
                return
                
        # Try to find by URL pattern
        if example_name == "Data Tables":
            self.page.goto(f"{self.url}/tables")
            return
        elif example_name == "Status Codes":
            self.page.goto(f"{self.url}/status_codes")
            return
                
        raise ValueError(f"Example '{example_name}' not found")

    def login(self, username: str, password: str) -> None:
        """Perform login with given credentials."""
        self.navigate_to_example("Form Authentication")
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)
        
    def get_flash_message(self) -> str:
        """Get the flash message text."""
        return self.get_text(self.flash_message)
        
    def wait_for_dynamic_text(self) -> str:
        """Wait for dynamically loaded text."""
        self.navigate_to_example("Dynamic Loading")
        self.click("text=Example 1")
        self.click(self.start_button)
        self.page.wait_for_selector(self.loading_indicator, state="hidden")
        return self.get_text(self.finish_text).strip()
        
    def toggle_checkbox(self, index: int) -> None:
        """Toggle checkbox at given index."""
        self.navigate_to_example("Checkboxes")
        checkboxes = self.page.query_selector_all(self.checkboxes)
        checkboxes[index].click()
        
    def is_checkbox_checked(self, index: int) -> bool:
        """Check if checkbox at given index is checked."""
        checkboxes = self.page.query_selector_all(self.checkboxes)
        return checkboxes[index].is_checked()
        
    def perform_drag_and_drop(self) -> None:
        """Perform drag and drop operation."""
        self.navigate_to_example("Drag and Drop")
        source = self.page.locator(self.draggable)
        target = self.page.locator(self.droppable)
        source.drag_to(target)
        
    def upload_file(self, file_path: str) -> None:
        """Upload a file."""
        self.navigate_to_example("File Upload")
        self.page.set_input_files(self.file_upload_input, file_path)
        self.click(self.upload_button)
        
    def switch_to_frame_and_type(self, text: str) -> None:
        """Switch to iframe and type text."""
        self.navigate_to_example("Frames")
        self.click(self.iframe_link)
        
        # Wait for iframe to load
        self.page.wait_for_selector(self.iframe)
        frame = self.page.frame_locator(self.iframe)
        
        # Wait for editor to be ready
        frame.locator(self.frame_content).wait_for(state="visible")
        
        # Type into the editor using keyboard press
        frame.locator(self.frame_content).press("Control+A")  # Select all
        frame.locator(self.frame_content).press("Delete")     # Clear content
        frame.locator(self.frame_content).type(text)         # Type new text
        
    def handle_javascript_alert(self, alert_type: str, input_text: str = None) -> str:
        """Handle different types of JavaScript alerts."""
        self.navigate_to_example("JavaScript Alerts")
        
        # Set up alert handling before triggering the alert
        dialog_handler = lambda dialog: dialog.accept(input_text) if alert_type == "prompt" else dialog.accept()
        self.page.once("dialog", dialog_handler)
        
        if alert_type == "confirm":
            self.click(self.js_confirm_button)
        elif alert_type == "prompt":
            self.click(self.js_prompt_button)
        else:  # simple alert
            self.click(self.js_alert_button)
            
        # Wait for the result text to appear
        self.page.wait_for_selector(self.result)
        return self.get_text(self.result)
        
    def verify_secure_page(self) -> bool:
        """Verify that we're on the secure page."""
        return "secure" in self.page.url and "Secure Area" in self.get_text(self.subheading)
        
    def verify_page_loaded(self) -> bool:
        """Verify that the page has loaded successfully."""
        return (
            self.is_element_visible(self.heading) and
            "Welcome to the-internet" in self.get_text(self.heading)
        )

    def press_key(self, key: str) -> str:
        """Press a key and get the result."""
        self.navigate_to_example("Key Presses")
        input_field = self.page.locator(self.key_press_input)
        input_field.press(key)
        return self.get_text(self.key_press_result)

    def set_slider_value(self, value: float) -> None:
        """Set horizontal slider to a specific value."""
        self.navigate_to_example("Horizontal Slider")
        slider = self.page.locator(self.slider)
        
        # Calculate the position based on the slider's range
        min_value = float(slider.get_attribute("min") or "0")
        max_value = float(slider.get_attribute("max") or "5")
        steps = float(slider.get_attribute("step") or "0.5")
        
        # Ensure value is within bounds and matches step increments
        value = max(min_value, min(max_value, value))
        value = round(value / steps) * steps
        
        # Set the value using JavaScript and trigger input event
        slider.evaluate(f"""(node) => {{
            node.value = {value};
            node.dispatchEvent(new Event('input', {{ bubbles: true }}));
            node.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}""")
        self.page.wait_for_timeout(500)  # Wait for the value to update

    def get_slider_value(self) -> float:
        """Get the current slider value."""
        value_element = self.page.locator(self.slider_value)
        return float(value_element.text_content() or "0")

    def get_table_data(self) -> List[Dict[str, str]]:
        """Get table data as a list of dictionaries."""
        self.navigate_to_example("Data Tables")
        
        # Wait for the table to be visible
        self.page.wait_for_selector(self.table)
        
        # Get headers
        headers = [header.text_content().strip() 
                  for header in self.page.query_selector_all(self.table_headers)]
        
        # Get rows
        rows = self.page.query_selector_all(self.table_rows)
        table_data = []
        
        for row in rows:
            cells = row.query_selector_all(self.table_cells)
            row_data = {}
            for header, cell in zip(headers, cells):
                row_data[header] = cell.text_content().strip()
            table_data.append(row_data)
            
        return table_data

    def sort_table_by_column(self, column_name: str) -> None:
        """Sort table by clicking on a column header."""
        self.navigate_to_example("Data Tables")
        
        # Wait for the table to be visible
        self.page.wait_for_selector(self.table)
        
        headers = self.page.query_selector_all(self.table_headers)
        for header in headers:
            if header.text_content().strip() == column_name:
                header.click()
                break

    def check_status_code(self, code: int) -> bool:
        """Check a specific status code page."""
        try:
            # Navigate directly to the status code page
            self.page.goto(f"{self.url}/status_codes/{code}")
            # Wait for the page to load
            self.page.wait_for_load_state("networkidle")
            # Verify we're on the correct page
            current_url = self.page.url
            return str(code) in current_url and "status_codes" in current_url
        except Exception as e:
            print(f"Error accessing status code {code}: {str(e)}")
            return False

    def verify_status_code_message(self, code: int) -> str:
        """Get the message from a status code page."""
        try:
            self.check_status_code(code)
            message = self.page.locator("p").text_content()
            return message.strip()
        except Exception:
            return "" 