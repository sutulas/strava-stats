# Running Stats - AI-Powered Fitness Analytics Platform

A comprehensive web application that provides intelligent analysis of Strava running data using natural language queries and AI-powered workflows. Built with modern web technologies and featuring an intuitive chat interface for data exploration.

##  Features

- ** AI-Powered Analysis**: Natural language queries processed through intelligent workflows
- ** Dynamic Chart Generation**: Automated creation of visualizations using seaborn and matplotlib
- ** Secure Strava Integration**: OAuth2 authentication with Strava API
- ** Modern Web Interface**: Responsive Angular frontend with Tailwind CSS
- ** Real-time Data Processing**: Live data fetching and analysis
- ** Comprehensive Analytics**: Detailed insights into running performance and trends

##  Tech Stack

### Backend
- **Python 3.8+** - Core runtime environment
- **FastAPI** - High-performance web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI applications
- **Pandas & NumPy** - Data manipulation and numerical computing
- **Matplotlib & Seaborn** - Data visualization and chart generation
- **OpenAI GPT-4** - AI-powered natural language processing
- **LangGraph** - Workflow orchestration for AI analysis
- **Python-dotenv** - Environment variable management

### Frontend
- **Angular 16** - Modern web application framework
- **TypeScript** - Type-safe JavaScript development
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Interactive charting library
- **RxJS** - Reactive programming for state management

### Development Tools
- **Git** - Version control
- **npm/Node.js** - Package management and runtime
- **Angular CLI** - Angular development tools
- **PostCSS** - CSS processing
- **ESLint/Prettier** - Code quality and formatting

##  Project Structure

```
strava-stats/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # FastAPI application entry point
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── services/              # Business logic services
│   │   ├── chat_workflow.py   # AI analysis workflow
│   │   ├── strava_auth_service.py    # Strava OAuth handling
│   │   ├── strava_data_service.py    # Strava API integration
│   │   ├── format_data_service.py    # Data processing
│   │   ├── graph_service.py          # Chart generation
│   │   └── user_analytics_service.py # User analytics
│   ├── routes/                # API route handlers
│   │   └── analysis.py        # Analysis endpoints
│   ├── data/                  # Data storage directory
│   └── old_services/          # Legacy service implementations
├── frontend/                   # Angular frontend application
│   ├── src/                   # Source code
│   │   ├── app/               # Application components
│   │   │   ├── dashboard/     # Main dashboard component
│   │   │   ├── login/         # Authentication component
│   │   │   ├── query-form/    # Query input component
│   │   │   ├── results/       # Results display component
│   │   │   ├── services/      # API services
│   │   │   └── shared/        # Shared components
│   │   ├── environments/      # Environment configuration
│   │   └── assets/            # Static assets
│   ├── package.json           # Node.js dependencies
│   ├── angular.json           # Angular configuration
│   └── tailwind.config.js     # Tailwind CSS configuration
└── README.md                  # This file
```

##  Quick Start

### Prerequisites

- **Python 3.8+** installed on your system
- **Node.js 16+** and npm installed
- **Git** for version control
- **Strava API credentials** (Client ID and Client Secret)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd strava-stats
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your Strava API credentials
```

**Environment Variables (.env):**
```env
CLIENT_ID=your_strava_client_id
CLIENT_SECRET=your_strava_client_secret
REDIRECT_URI=http://localhost:4200/token
OPENAI_API_KEY=your_openai_api_key
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Configure Strava API credentials
# Edit src/environments/environment.ts with your Client ID
```

**Environment Configuration (src/environments/environment.ts):**
```typescript
export const environment = {
  production: false,
  strava: {
    clientId: 'YOUR_STRAVA_CLIENT_ID',
    redirectUri: 'http://localhost:4200/token'
  }
};
```

### 4. Start Development Servers

```bash
# Terminal 1 - Start Backend (from backend directory)
cd backend
python main.py
# Server runs on http://localhost:8000

# Terminal 2 - Start Frontend (from frontend directory)
cd frontend
npm start
# Application runs on http://localhost:4200
```

### 5. Access the Application

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

##  Development Workflow

### Backend Development

1. **Service Development**: Add new services in `backend/services/`
2. **API Endpoints**: Define routes in `backend/routes/` or `main.py`
3. **Data Models**: Use Pydantic for request/response validation
4. **Testing**: Run tests with `python test_data_refresh.py`

### Frontend Development

1. **Component Creation**: Generate components with `ng generate component component-name`
2. **Service Integration**: Add API services in `src/app/services/`
3. **Styling**: Use Tailwind CSS classes for consistent design
4. **Testing**: Run tests with `npm test`

### AI Workflow Development

The AI analysis workflow is built using LangGraph and can be extended in `backend/services/chat_workflow.py`:

- **Query Analysis**: Understands user intent
- **Code Generation**: Creates Python code for data analysis
- **Chart Generation**: Produces visualizations using seaborn
- **Response Formatting**: Generates markdown responses

##  API Endpoints

### Authentication
- `POST /auth/token` - Exchange Strava authorization code for access token

### Data Management
- `POST /data/refresh` - Fetch fresh Strava data
- `GET /data/status` - Get data status
- `GET /data/overview` - Get dataset overview

### Analysis
- `POST /query` - Process natural language analysis queries
- `GET /examples` - Get example queries
- `GET /chart.png` - Get generated chart image

### Health & Status
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

##  Testing

### Backend Testing
```bash
cd backend
python test_data_refresh.py
```

### Frontend Testing
```bash
cd frontend
npm test
```

##  Deployment

### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Production Build
```bash
cd frontend
npm run build
# Built files are in dist/ directory
```

##  Security Considerations

- **Environment Variables**: Never commit API keys or secrets
- **CORS Configuration**: Configure allowed origins for production
- **Token Management**: Implement proper token refresh mechanisms
- **Input Validation**: All inputs validated using Pydantic models
- **HTTPS**: Use HTTPS in production environments

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the LICENSE file for details.

##  Support

For support and questions:
- Check the existing documentation
- Review the API documentation at `/docs`
- Open an issue in the repository

##  Roadmap

- [ ] Advanced analytics and machine learning insights
- [ ] Mobile application development
- [ ] Social features and leaderboards
- [ ] Integration with additional fitness platforms
- [ ] Real-time notifications and alerts

---
