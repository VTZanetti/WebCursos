# Changelog

All notable changes to the WebCurso project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Batch lesson processing endpoint for improved performance
- Comprehensive documentation structure
- API documentation for batch endpoint
- Feature documentation for batch processing

### Changed
- Improved "Marcar todas" and "Desmarcar todas" functionality
- Fixed database helper functions to properly handle connections/cursors
- Enhanced error handling in API endpoints
- Updated frontend to use batch processing with fallback

### Fixed
- Performance issues with individual lesson processing
- Database connection handling in update functions
- Repeated API calls for the same lessons

## [1.0.0] - 2023-01-01

### Added
- Initial release of WebCurso application
- Course management functionality
- Lesson progress tracking
- Basic CRUD operations for courses
- Vue.js frontend with Flask backend
- SQLite database integration

### Changed
- N/A (Initial release)

### Deprecated
- N/A (Initial release)

### Removed
- N/A (Initial release)

### Fixed
- N/A (Initial release)

### Security
- N/A (Initial release)