// Test script for dark mode functionality
console.log('Testing dark mode implementation...');

// Test 1: Check if dark mode toggle works
console.log('Test 1: Dark mode toggle functionality');
console.log('Expected: Theme preference should be saved to localStorage');

// Simulate dark mode toggle
const savedTheme = localStorage.getItem('webcurso-theme');
console.log('Current saved theme:', savedTheme);

// Toggle dark mode
const newTheme = savedTheme === 'dark' ? 'light' : 'dark';
localStorage.setItem('webcurso-theme', newTheme);
console.log('New theme set to:', newTheme);

// Test 2: Check if CSS variables are properly defined
console.log('\nTest 2: CSS variables for dark mode');
const rootStyles = getComputedStyle(document.documentElement);
const bgColor = rootStyles.getPropertyValue('--bg-primary').trim();
console.log('Background color:', bgColor);

// Test 3: Check if dark mode class is applied to app
console.log('\nTest 3: Dark mode class application');
const appElement = document.getElementById('app');
if (appElement) {
  const isDarkMode = appElement.classList.contains('dark-mode');
  console.log('Dark mode class applied:', isDarkMode);
} else {
  console.log('App element not found');
}

console.log('\nDark mode test completed.');