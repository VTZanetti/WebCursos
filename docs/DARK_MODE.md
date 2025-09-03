# Dark Mode Implementation

WebCurso includes a comprehensive dark mode feature that provides a comfortable viewing experience in low-light environments. This document explains how the dark mode is implemented and how to use it.

## Features

- Automatic detection of system preference
- Manual toggle switch
- Persistent theme preference using localStorage
- Smooth transitions between themes
- Full support across all components

## Implementation Details

### CSS Variables

The dark mode is implemented using CSS variables that change based on the theme. The root variables are defined in `App.vue`:

```css
:root {
  /* Light mode variables */
  --primary-color: #3b82f6;
  --text-primary: #1f2937;
  --bg-primary: #ffffff;
  --border-color: #e5e7eb;
  /* ... other variables */
}

.dark-mode {
  /* Dark mode overrides */
  --text-primary: #f9fafb;
  --bg-primary: #111827;
  --border-color: #4b5563;
  /* ... other variables */
}
```

### Theme Toggle

The theme can be toggled using the button in the navigation bar. The toggle button shows:
- 🌙 (moon icon) for light mode
- ☀️ (sun icon) for dark mode

### Persistence

The theme preference is saved to localStorage with the key `webcurso-theme`. The value can be either `dark` or `light`.

### System Preference Detection

If no saved preference exists, the application will default to the user's system preference using the `prefers-color-scheme` media query.

## Components with Dark Mode Support

All Vue components in the application have been updated with dark mode styles:

1. **App.vue** - Main application wrapper
2. **DashboardView.vue** - Dashboard page
3. **CourseDetailView.vue** - Course detail page
4. **CourseCard.vue** - Course card component
5. **ProgressBar.vue** - Progress bar component
6. **CourseModal.vue** - Course creation/editing modal
7. **ConfirmationModal.vue** - Confirmation dialog

## Usage

### Manual Toggle

Click the theme toggle button (🌙/☀️) in the top navigation bar to switch between light and dark modes.

### Automatic Detection

The application automatically detects your system's color scheme preference and applies the appropriate theme on first load.

### Persistence

Your theme preference is saved and will be applied automatically on subsequent visits.

## Development

When adding new components or modifying existing ones, ensure dark mode support by:

1. Adding dark mode specific styles using the `.dark-mode` class prefix
2. Using CSS variables for consistent theming
3. Testing both light and dark modes
4. Ensuring proper contrast ratios for accessibility

### Example

```vue
<template>
  <div class="my-component">
    <h2 class="component-title">My Component</h2>
    <p class="component-text">This text adapts to the theme</p>
  </div>
</template>

<style scoped>
.my-component {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  padding: 20px;
}

.component-title {
  color: var(--text-primary);
}

/* Dark mode overrides */
.dark-mode .my-component {
  background: var(--bg-primary);
  border-color: var(--border-color);
}

.dark-mode .component-title {
  color: var(--text-primary);
}
</style>
```

## Testing

To test the dark mode implementation:

1. Open the application in a browser
2. Click the theme toggle button to switch between modes
3. Verify that all components render correctly in both modes
4. Refresh the page to ensure the preference is persisted
5. Check that the system preference is respected when no saved preference exists

## Accessibility

The dark mode implementation ensures:
- Proper contrast ratios for readability
- Consistent color scheme across all components
- Smooth transitions between themes
- Support for users with visual impairments