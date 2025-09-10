# Use Node.js 16 as base image
FROM node:16

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Install serve to serve the static files
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Serve the application
CMD ["serve", "-s", "dist", "-l", "3000"]