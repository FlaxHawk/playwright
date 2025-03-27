import os
import pytest
from typing import Dict, Generator
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DEFAULT_TIMEOUT = int(os.getenv('TIMEOUT', 30000))
BROWSER_NAME = os.getenv('BROWSER', 'chromium')
HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
SLOW_MO = int(os.getenv('SLOW_MO', 0))
BASE_URL = os.getenv('BASE_URL', 'https://example.com')

# Device configurations for responsive testing
DEVICES = {
    'mobile': {'viewport': {'width': 375, 'height': 667}},
    'tablet': {'viewport': {'width': 768, 'height': 1024}},
    'desktop': {'viewport': {'width': 1920, 'height': 1080}},
}

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict) -> Dict:
    """Fixture to set default browser context arguments."""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "record_video_dir": "reports/videos" if os.getenv('VIDEO_ON_FAILURE', 'true').lower() == 'true' else None,
    }

@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "args": ["--start-maximized"],
        "headless": False,
    }

@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Generator[Browser, None, None]:
    """Fixture to launch browser."""
    browser = getattr(playwright, BROWSER_NAME).launch(
        headless=HEADLESS,
        slow_mo=SLOW_MO,
    )
    yield browser
    browser.close()

@pytest.fixture
def context(browser: Browser, browser_context_args: Dict) -> Generator[BrowserContext, None, None]:
    """Fixture to create new browser context."""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()

@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Fixture to create new page."""
    page = context.new_page()
    page.set_default_timeout(DEFAULT_TIMEOUT)
    yield page

@pytest.fixture(params=DEVICES.keys())
def responsive_page(browser: Browser, request) -> Generator[Page, None, None]:
    """Fixture for responsive testing across different device sizes."""
    device_config = DEVICES[request.param]
    context = browser.new_context(**device_config)
    page = context.new_page()
    page.set_default_timeout(DEFAULT_TIMEOUT)
    yield page
    context.close()

@pytest.fixture(scope="session")
def base_url() -> str:
    """Fixture to get base URL from environment variables."""
    return BASE_URL 