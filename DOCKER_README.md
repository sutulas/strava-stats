# Docker Setup for Strava Stats

This project includes Docker configuration for both the frontend and backend services.

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode:**
   ```bash
   docker-compose up -d --build
   ```

3. **Stop all services:**
   ```bash
   docker-compose down
   ```

### Individual Service Commands

#### Backend Only
```bash
# Build the backend image
docker build -t strava-stats-backend ./backend

# Run the backend container
docker run -p 8000:8000 strava-stats-backend
```

#### Frontend Only
```bash
# Build the frontend image
docker build -t strava-stats-frontend ./frontend

# Run the frontend container
docker run -p 3000:80 strava-stats-frontend
```

## Services

- **Backend**: FastAPI application running on port 8000
- **Frontend**: React application served by nginx on port 3000

## Environment Variables

Make sure to set up your environment variables before running the containers. Create a `.env` file in the backend directory with your Strava API credentials and other configuration.

## Health Checks

Both services include health checks:
- Backend: `http://localhost:8000/health`
- Frontend: `http://localhost:3000/`

## Data Persistence

The backend data directory is mounted as a volume to persist data between container restarts.

## Development

For development, you may want to mount your source code as volumes:

```yaml
# Add to docker-compose.yml for development
volumes:
  - ./backend:/app
  - ./frontend:/app
```

## Troubleshooting

1. **Port conflicts**: Make sure ports 8000 and 3000 are not in use
2. **Build failures**: Check that all dependencies are properly specified
3. **Health check failures**: Ensure the applications are starting correctly

## Production Considerations

- Use specific image tags instead of `latest`
- Set up proper secrets management
- Configure reverse proxy (nginx/traefik) for production
- Use multi-stage builds to reduce image size
- Set up proper logging and monitoring