# Unit Testing Guide - Smartgement

Comprehensive unit tests for the Smartgement application covering both Go backend and Python AI services.

## Test Structure

```
unit-tes/
├── backend/           # Go tests
│   ├── controllers/   # Controller tests
│   └── test_utils.go  # Test utilities
├── aiservices/        # Python tests
│   ├── conftest.py    # Pytest fixtures
│   └── test_*.py      # Test modules
└── README.md          # This file
```

## Running Tests

### Backend Tests (Go)

Navigate to the backend test directory and run:

```bash
cd c:\Users\ihsan\VScodeProject\smartgement\unit-tes\backend
go test -v ./...
```

**Run specific test:**
```bash
go test -v -run TestRegister ./controllers
```

### AI Services Tests (Python)

First, install testing dependencies:

```bash
cd c:\Users\ihsan\VScodeProject\smartgement\unit-tes\aiservices
pip install -r requirements-test.txt
```

Run all tests:
```bash
pytest -v
```

**Run specific test file:**
```bash
pytest -v test_chatbot_service.py
```

**Run with coverage:**
```bash
pytest --cov=../../aiservices/app --cov-report=html
```

Coverage report will be in `htmlcov/index.html`

## Test Coverage

### Backend (Go)

- **Auth Controller**: Registration, login, user retrieval
- **Product Controller**: CRUD operations, authorization
- **Transaction Controller**: Create/list transactions
- **Middlewares**: JWT authentication

### AI Services (Python)

- **Chatbot Service**: Intent classification, CRUD via chat, query handling
- **Automation Service**: Bulk operations, preview, undo functionality
- **Product Service**: Database operations

## Mocking Strategy

### Backend
- Database operations use in-memory SQLite for speed
- reCAPTCHA verification is mocked
- JWT generation uses test secrets

### AI Services
- LLM calls (Gemini API) are mocked to avoid API costs
- Database uses SQLite in-memory or temporary files
- External service calls are mocked

## Best Practices

1. **Isolation**: Each test should be independent
2. **Clean State**: Use setup/teardown to ensure clean state
3. **Descriptive Names**: Test names should describe what they test
4. **Fast Execution**: Mock external dependencies
5. **Coverage**: Aim for >80% code coverage on critical paths

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

**GitHub Actions example:**
```yaml
- name: Run Go Tests
  run: cd unit-tes/backend && go test ./...

- name: Run Python Tests
  run: cd unit-tes/aiservices && pytest
```

## Troubleshooting

**Go tests fail with import errors:**
- Ensure you're in the correct directory
- Run `go mod tidy` in the backend folder

**Python tests fail with module not found:**
- Activate virtual environment
- Install `requirements-test.txt`
- Ensure PYTHONPATH includes the aiservices directory

**Database connection errors:**
- Tests should use in-memory databases
- Check conftest.py fixture configuration

## Contributing

When adding new features:
1. Write tests first (TDD approach recommended)
2. Ensure all existing tests still pass
3. Aim for comprehensive coverage of new code
4. Update this README if adding new test categories
