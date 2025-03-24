import os
import json
from typing import Dict, Any
from datetime import datetime

def save_test_artifact(artifact_type: str, data: Any, test_name: str) -> str:
    """
    Save test artifacts (screenshots, videos, logs) with proper naming and organization.
    
    Args:
        artifact_type: Type of artifact (screenshot, video, log)
        data: The artifact data to save
        test_name: Name of the test that generated the artifact
    
    Returns:
        str: Path to the saved artifact
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifacts_dir = os.path.join("reports", "artifacts", artifact_type)
    os.makedirs(artifacts_dir, exist_ok=True)
    
    filename = f"{test_name}_{timestamp}.{artifact_type}"
    filepath = os.path.join(artifacts_dir, filename)
    
    if artifact_type == "json":
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    elif artifact_type in ["png", "jpg"]:
        # Assuming data is a bytes object for images
        with open(filepath, "wb") as f:
            f.write(data)
    else:
        # For other types, assume string data
        with open(filepath, "w") as f:
            f.write(str(data))
    
    return filepath

def get_test_data(test_name: str) -> Dict:
    """
    Load test data from JSON files.
    
    Args:
        test_name: Name of the test to load data for
    
    Returns:
        dict: Test data
    """
    data_file = os.path.join("tests", "data", f"{test_name}.json")
    if not os.path.exists(data_file):
        return {}
    
    with open(data_file, "r") as f:
        return json.load(f)

def retry_on_failure(func, max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function on failure.
    
    Args:
        func: Function to retry
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds
    
    Returns:
        Any: Result of the function call
    """
    from functools import wraps
    import time
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        attempts = 0
        last_exception = None
        
        while attempts < max_attempts:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                attempts += 1
                last_exception = e
                if attempts < max_attempts:
                    time.sleep(delay)
        
        raise last_exception
    
    return wrapper

def generate_test_report(results: Dict) -> str:
    """
    Generate a detailed test report in markdown format.
    
    Args:
        results: Dictionary containing test results
    
    Returns:
        str: Markdown formatted report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = [
        "# Test Execution Report",
        f"\nGenerated: {timestamp}\n",
        "## Summary",
        f"- Total Tests: {results.get('total', 0)}",
        f"- Passed: {results.get('passed', 0)}",
        f"- Failed: {results.get('failed', 0)}",
        f"- Skipped: {results.get('skipped', 0)}",
        "\n## Test Details\n"
    ]
    
    for test in results.get('tests', []):
        report.extend([
            f"### {test['name']}",
            f"- Status: {test['status']}",
            f"- Duration: {test['duration']}s",
            f"- Error: {test.get('error', 'None')}\n"
        ])
    
    return "\n".join(report)

def setup_test_environment() -> Dict[str, Any]:
    """
    Set up test environment with necessary configurations.
    
    Returns:
        dict: Environment configuration
    """
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create necessary directories
    dirs = ["reports", "reports/artifacts", "reports/videos", "reports/screenshots"]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # Return configuration
    return {
        "browser": os.getenv("BROWSER", "chromium"),
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
        "viewport": {
            "width": int(os.getenv("VIEWPORT_WIDTH", "1920")),
            "height": int(os.getenv("VIEWPORT_HEIGHT", "1080"))
        },
        "timeout": int(os.getenv("TIMEOUT", "30000")),
        "screenshot_on_failure": os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true",
        "video_on_failure": os.getenv("VIDEO_ON_FAILURE", "true").lower() == "true"
    } 