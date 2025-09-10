# Testing Guide

This document provides guidelines for testing the WebCurso application.

## Testing Strategy

WebCurso uses a combination of unit tests, integration tests, and end-to-end tests to ensure quality and reliability.

## Backend Testing

### Unit Tests

Unit tests for the backend focus on testing individual functions and components in isolation.

#### Test Structure

Tests are organized by module:
- `test_database.py`: Database operations
- `test_api.py`: API endpoints
- `test_helpers.py`: Helper functions

#### Running Backend Tests

```bash
cd backend
python -m pytest tests/
```

#### Example Test

```python
def test_create_course():
    # Test course creation functionality
    pass
```

### Integration Tests

Integration tests verify that different components work together correctly.

#### Database Integration Tests

```python
def test_course_creation_persists():
    # Test that created courses are properly stored in the database
    pass
```

### API Tests

API tests verify that endpoints return correct responses.

```python
def test_get_courses():
    # Test GET /api/cursos endpoint
    pass
```

## Frontend Testing

### Unit Tests

Unit tests for the frontend focus on testing individual Vue components and functions.

#### Test Structure

Tests are organized by component:
- `components/`: Component tests
- `views/`: View tests
- `services/`: Service tests

#### Running Frontend Tests

```bash
cd frontend
npm run test
```

#### Example Test

```javascript
import { mount } from '@vue/test-utils'
import CourseCard from '@/components/CourseCard.vue'

describe('CourseCard.vue', () => {
  it('renders course title', () => {
    const wrapper = mount(CourseCard, {
      props: {
        course: {
          titulo: 'Test Course'
        }
      }
    })
    expect(wrapper.text()).toContain('Test Course')
  })
})
```

### Integration Tests

Integration tests verify that components work together correctly.

#### Component Integration Tests

```javascript
describe('CourseDetailView', () => {
  it('loads course data correctly', async () => {
    // Test that course data is loaded and displayed properly
  })
})
```

### End-to-End Tests

End-to-end tests simulate user interactions with the application.

#### Test Structure

E2E tests use Cypress or a similar framework:
- `cypress/e2e/`: Test specifications
- `cypress/fixtures/`: Test data
- `cypress/support/`: Test helpers

#### Running E2E Tests

```bash
cd frontend
npm run test:e2e
```

#### Example E2E Test

```javascript
describe('Course Management', () => {
  it('creates a new course', () => {
    cy.visit('/')
    cy.contains('Novo Curso').click()
    cy.get('[data-cy=course-title]').type('Test Course')
    cy.get('[data-cy=total-lessons]').type('10')
    cy.get('[data-cy=submit]').click()
    cy.contains('Test Course').should('be.visible')
  })
})
```

## Test Data Management

### Backend Test Data

Use fixtures and factories to create consistent test data:

```python
@pytest.fixture
def sample_course():
    return {
        'titulo': 'Test Course',
        'total_aulas': 10
    }
```

### Frontend Test Data

Use mock data and factories for frontend tests:

```javascript
const mockCourse = {
  id: 1,
  titulo: 'Test Course',
  total_aulas: 10
}
```

## Continuous Integration

### GitHub Actions

The project uses GitHub Actions for continuous integration:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          python -m pytest
```

## Test Coverage

### Backend Coverage

Aim for >80% test coverage for backend code:

```bash
cd backend
python -m pytest --cov=.
```

### Frontend Coverage

Aim for >80% test coverage for frontend code:

```bash
cd frontend
npm run test:coverage
```

## Performance Testing

### Load Testing

Use tools like Apache Bench or Locust for load testing:

```bash
ab -n 1000 -c 10 http://localhost:5000/api/cursos
```

### Stress Testing

Test the application under extreme conditions to identify bottlenecks.

## Security Testing

### API Security

- Test for SQL injection vulnerabilities
- Test for XSS vulnerabilities
- Validate input sanitization

### Authentication Testing

- Test authentication mechanisms
- Validate session management
- Test authorization controls

## Manual Testing

### Test Cases

1. **Course Creation**
   - Create a new course with valid data
   - Attempt to create a course with invalid data
   - Verify course appears in course list

2. **Lesson Management**
   - Mark individual lessons as completed
   - Mark all lessons as completed
   - Unmark individual lessons
   - Unmark all lessons
   - Verify progress calculations

3. **Course Editing**
   - Edit course title
   - Edit total number of lessons
   - Edit course notes
   - Verify changes are saved

4. **Course Deletion**
   - Delete a course
   - Verify course is removed from list
   - Verify associated lesson data is removed

### Browser Compatibility

Test the application in the following browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

### Mobile Responsiveness

Test the application on various screen sizes:
- Desktop
- Tablet
- Mobile

## Debugging

### Backend Debugging

Use logging for debugging backend issues:

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Course created successfully")
logger.error("Failed to create course: %s", error_message)
```

### Frontend Debugging

Use browser developer tools for frontend debugging:
- Console logging
- Network tab inspection
- Element inspection

## Test Reporting

### Test Results

Generate test reports for CI/CD pipelines:

```bash
cd backend
python -m pytest --junitxml=report.xml
```

### Code Coverage Reports

Generate code coverage reports:

```bash
cd backend
python -m pytest --cov=. --cov-report=html
```

## Best Practices

### Test Design

1. **Keep tests independent**: Each test should be able to run independently
2. **Use descriptive test names**: Test names should clearly describe what is being tested
3. **Follow the AAA pattern**: Arrange, Act, Assert
4. **Test edge cases**: Include tests for boundary conditions and error cases
5. **Maintain test data**: Keep test data clean and consistent

### Test Maintenance

1. **Regular review**: Review and update tests regularly
2. **Remove obsolete tests**: Delete tests that are no longer relevant
3. **Refactor tests**: Keep tests clean and maintainable
4. **Update documentation**: Keep test documentation up to date

### Test Automation

1. **CI/CD integration**: Integrate tests into the CI/CD pipeline
2. **Automated reporting**: Generate automated test reports
3. **Failure notifications**: Set up notifications for test failures
4. **Performance monitoring**: Monitor test execution times