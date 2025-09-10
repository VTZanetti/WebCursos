# Development Guidelines

This document provides guidelines and best practices for developing the WebCurso application.

## Project Structure

```
WebCurso/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── database.py         # Database management
│   ├── config.py           # Configuration settings
│   ├── init_db.py          # Database initialization
│   ├── requirements.txt    # Python dependencies
│   └── instance/
│       └── database.sqlite # SQLite database file
├── frontend/
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Vue views
│   │   ├── services/       # API services
│   │   └── assets/         # Static assets
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── docs/                   # Documentation files
└── README.md              # Project README
```

## Backend Development

### Python Standards

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

### Flask Application Structure

The backend follows a RESTful API design pattern with the following structure:

1. **Helper Functions**: Utility functions for common operations
2. **API Endpoints**: RESTful routes for CRUD operations
3. **Error Handling**: Consistent error response format
4. **Database Management**: SQLite database operations

### Database Design

The application uses SQLite with two main tables:

1. **cursos**: Stores course information
   - id (INTEGER, PRIMARY KEY)
   - titulo (TEXT)
   - link (TEXT)
   - total_aulas (INTEGER)
   - anotacoes (TEXT)
   - created_at (TEXT)
   - updated_at (TEXT)

2. **aulas_concluidas**: Tracks completed lessons
   - id (INTEGER, PRIMARY KEY)
   - curso_id (INTEGER, FOREIGN KEY to cursos.id)
   - numero_aula (INTEGER)

### Adding New Features

1. Create new endpoints in `app.py`
2. Add corresponding helper functions if needed
3. Update database schema in `init_db.py` if necessary
4. Add error handling and validation
5. Document the new endpoints in `API.md`

## Frontend Development

### Vue.js Standards

- Follow Vue.js style guide
- Use Composition API or Options API consistently
- Organize components logically
- Use meaningful component names
- Keep components small and focused

### Component Structure

1. **Template**: HTML structure
2. **Script**: JavaScript logic
3. **Style**: Scoped CSS styles

### API Integration

All API calls should go through the service layer in `src/services/api.js`:

1. Add new methods to the `apiService` object
2. Handle errors appropriately
3. Return consistent data structures
4. Update documentation in `API.md`

### Adding New Features

1. Create new Vue components in `src/components/`
2. Add new views in `src/views/` if needed
3. Update routing in `src/router/index.js`
4. Add API methods in `src/services/api.js`
5. Update styling as needed

## Git Workflow

### Branching Strategy

- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: Feature branches
- `hotfix/*`: Hotfix branches

### Commit Messages

Follow conventional commit format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Pull Requests

1. Create PRs from feature branches to `develop`
2. Include description of changes
3. Link to related issues
4. Request code review
5. Ensure CI checks pass

## Testing

See [TESTING.md](TESTING.md) for detailed testing guidelines.

## Code Quality

### Backend

- Use pylint or flake8 for code linting
- Maintain test coverage above 80%
- Document all public APIs
- Handle errors gracefully

### Frontend

- Use ESLint and Prettier for code formatting
- Follow Vue.js style guide
- Write unit tests for components
- Use TypeScript for type safety (if applicable)

## Performance Considerations

### Backend

- Use database indexes for frequently queried fields
- Implement pagination for large datasets
- Cache expensive operations when appropriate
- Optimize database queries

### Frontend

- Lazy load components when possible
- Optimize images and assets
- Minimize bundle size
- Use efficient rendering techniques

## Security

### Backend

- Validate all input data
- Use parameterized queries to prevent SQL injection
- Implement proper error handling without exposing sensitive information
- Keep dependencies up to date

### Frontend

- Sanitize user input
- Validate data before sending to backend
- Implement proper error handling
- Keep dependencies up to date

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guidelines.