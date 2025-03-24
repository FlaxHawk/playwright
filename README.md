# Playwright Automated Testing Framework

This project demonstrates a comprehensive automated testing framework using Playwright and pytest, incorporating CI/CD pipelines and best practices for web testing.

## 🚀 Features

- Cross-browser testing support (Chrome, Firefox, Safari)
- Parallel test execution
- Comprehensive reporting
- CI/CD integration with Jenkins
- Environment-based configuration
- Error handling and retry mechanisms
- Device responsiveness testing

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Jenkins (for CI/CD)

## 🛠️ Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd playwright-testing-framework
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   playwright install
   ```

5. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 🧪 Running Tests

### Run all tests:
```bash
pytest
```

### Run tests in parallel:
```bash
pytest -n auto
```

### Run tests with specific browser:
```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Generate HTML report:
```bash
pytest --html=report.html
```

## 📁 Project Structure

```
.
├── tests/
│   ├── conftest.py           # Pytest configurations and fixtures
│   ├── ui/                   # UI test cases
│   │   ├── test_navigation.py
│   │   ├── test_forms.py
│   │   └── test_responsive.py
│   └── utils/               # Test utilities and helpers
├── pages/                   # Page Object Models
├── config/                  # Configuration files
├── reports/                 # Test reports directory
├── Jenkinsfile             # CI/CD pipeline definition
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## 🔄 CI/CD Pipeline

The project includes a Jenkins pipeline that:
1. Runs tests on every push and pull request
2. Generates test reports
3. Deploys code on successful test execution

## 📊 Test Reports

- HTML reports are generated in the `reports` directory
- Allure reports provide detailed test execution insights
- Screenshots and videos are captured for failed tests

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
