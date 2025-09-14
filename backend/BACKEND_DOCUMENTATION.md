# Strava Stats Backend Documentation

## Overview

The Strava Stats backend is a FastAPI-based application that provides AI-powered analysis of Strava running data. It features a sophisticated chat workflow system that can process natural language queries about running statistics and generate both textual responses and visual charts.

## Architecture

The backend follows a modular service-oriented architecture with the following key components:

- **FastAPI Application** (`main.py`): Main application entry point with API endpoints
- **Routes** (`routes/`): API route definitions and handlers
- **Services** (`services/`): Business logic and data processing services
- **AI Workflow** (`chat_workflow.py`): LangGraph-based AI workflow for query processing

## API Endpoints

### Core Application Endpoints

#### Health Check Endpoints

**GET `/`**
- **Description**: Root health check endpoint
- **Response**: Basic application status and version information
- **Example Response**:
```json
{
  "message": "Strava Stats API is running",
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "version": "1.0.0"
}
```

**GET `/health`**
- **Description**: Detailed health check with system status
- **Response**: Comprehensive health information including data file status and workflow initialization
- **Example Response**:
```json
{
  "status": "healthy",
  "data_file_exists": true,
  "workflow_initialized": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Authentication Endpoints

**POST `/auth/token`**
- **Description**: Exchange Strava authorization code for access token
- **Request Body**:
```json
{
  "code": "strava_authorization_code"
}
```
- **Response**: Access token and metadata
- **Example Response**:
```json
{
  "access_token": "access_token_here",
  "token_type": "Bearer",
  "expires_at": null,
  "refresh_token": null,
  "scope": "activity:read_all"
}
```

### Data Management Endpoints

**POST `/data/refresh`**
- **Description**: Fetch fresh Strava data and update the workflow dataset
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Data refresh status and statistics
- **Example Response**:
```json
{
  "message": "Data refreshed successfully",
  "activities_count": 150,
  "file_path": "fixed_formatted_run_data.csv",
  "timestamp": "2024-01-15T10:30:00"
}
```

**GET `/data/status`**
- **Description**: Get current status of user's data
- **Response**: Data file status and activity counts
- **Example Response**:
```json
{
  "data_processed": true,
  "formatted_data_exists": true,
  "activities_count": 150,
  "latest_activity": "2024-01-14T18:30:00",
  "workflow_ready": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

### User Profile Endpoints

**GET `/user/profile`**
- **Description**: Get user profile information from Strava
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Complete user profile data
- **Example Response**:
```json
{
  "id": 12345678,
  "firstname": "John",
  "lastname": "Doe",
  "username": "johndoe",
  "city": "Boston",
  "state": "MA",
  "country": "United States",
  "weight": 70.5,
  "profile": "https://dgalywyr863g5.cloudfront.net/pictures/athletes/...",
  "profile_medium": "https://dgalywyr863g5.cloudfront.net/pictures/athletes/...",
  "follower_count": 25,
  "friend_count": 50,
  "date_preference": "%m/%d/%Y",
  "measurement_preference": "feet"
}
```

**GET `/user/stats`**
- **Description**: Get comprehensive user statistics and analytics
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Detailed running statistics
- **Example Response**:
```json
{
  "summary": {
    "total_runs": 150,
    "total_miles": 1200.5,
    "total_time_minutes": 12000.0,
    "total_elevation": 50000.0,
    "this_year_miles": 300.2
  },
  "averages": {
    "avg_pace": 8.5,
    "avg_distance": 8.0,
    "avg_time": 80.0,
    "avg_heartrate": 155.0
  },
  "bests": {
    "fastest_pace": 6.2,
    "longest_run": 26.2,
    "longest_time": 240.0
  },
  "weekly_stats": [...],
  "monthly_stats": [...],
  "day_of_week_stats": [...]
}
```

**GET `/user/recent-activities`**
- **Description**: Get recent running activities
- **Headers**: `Authorization: Bearer <access_token>`
- **Query Parameters**: `limit` (default: 10)
- **Response**: List of recent activities
- **Example Response**:
```json
{
  "activities": [
    {
      "id": 123456789,
      "name": "Morning Run",
      "date": "2024-01-14T06:30:00",
      "distance": 5.2,
      "time": 42.5,
      "pace": 8.2,
      "elevation": 150.0,
      "heartrate": 155.0
    }
  ]
}
```

### Analysis Endpoints

**POST `/query`**
- **Description**: Process a user query using the AI-powered chat workflow
- **Request Body**:
```json
{
  "query": "What is my average running pace?",
  "include_chart": true
}
```
- **Response**: Analysis results with optional chart generation
- **Example Response**:
```json
{
  "query": "What is my average running pace?",
  "response": "Your average running pace is **8.5 minutes per mile** based on 150 runs.",
  "chart_generated": false,
  "chart_url": null,
  "execution_time": 2.3,
  "timestamp": "2024-01-15T10:30:00",
  "status": "success"
}
```

**GET `/chart`**
- **Description**: Get the most recently generated chart
- **Response**: PNG image file or 404 if no chart available
- **Content-Type**: `image/png`

**GET `/data/overview`**
- **Description**: Get an overview of the available data
- **Response**: Basic statistics and information about the dataset
- **Example Response**:
```json
{
  "total_activities": 150,
  "date_range": {
    "start": "2023-01-01",
    "end": "2024-01-14"
  },
  "activity_types": {
    "Run": 150
  },
  "columns": ["id", "start_date", "name", "distance", ...],
  "sample_data": [...],
  "data_loaded_at": "2024-01-15T10:30:00"
}
```

**GET `/examples`**
- **Description**: Get example queries that users can try
- **Response**: Categorized example queries
- **Example Response**:
```json
{
  "examples": [
    {
      "category": "Basic Statistics",
      "queries": [
        "What is my average running pace?",
        "How many miles have I run this year?",
        "What is my fastest run?",
        "Show me my total elevation gain"
      ]
    },
    {
      "category": "Trends and Analysis",
      "queries": [
        "How has my pace improved over time?",
        "What days of the week do I run most?",
        "Show me my weekly mileage trends",
        "What is my average heart rate during runs?"
      ]
    },
    {
      "category": "Charts and Visualizations",
      "queries": [
        "Create a chart showing my distance over time",
        "Show me a histogram of my running paces",
        "Generate a scatter plot of pace vs heart rate",
        "Create a bar chart of my monthly mileage"
      ]
    }
  ]
}
```

## Services

### 1. StravaWorkflow (`chat_workflow.py`)

The core AI-powered workflow service that processes natural language queries about running data.

**Key Features**:
- LangGraph-based state machine workflow
- OpenAI GPT-4 integration for query analysis and code generation
- Automatic chart generation using seaborn and matplotlib
- Data analysis using pandas
- Query enhancement and verification

**Workflow States**:
- `analyze_query`: Initial query analysis
- `enhance_query`: Query enhancement for better code generation
- `prepare_graphs`: Chart code generation (if chart requested)
- `prepare_data`: Data analysis code generation
- `verify_graphs`: Chart code validation
- `verify_code`: Data analysis code validation
- `graph_data`: Chart execution
- `analyze_data`: Data analysis execution
- `final_response`: Response generation

**Main Methods**:
- `run_workflow(messages, df)`: Execute the complete workflow
- `_build_workflow()`: Construct the LangGraph workflow

### 2. UserAnalyticsService (`user_analytics_service.py`)

Comprehensive analytics service for user running data.

**Key Features**:
- User profile data retrieval from Strava API
- Comprehensive statistics calculation
- Time-based analysis (weekly, monthly, yearly)
- Day-of-week analysis
- Recent activities retrieval

**Main Methods**:
- `get_user_profile_data(access_token)`: Fetch user profile from Strava
- `get_user_stats(data_file_path)`: Calculate comprehensive statistics
- `get_recent_activities(data_file_path, limit)`: Get recent activities

**Statistics Provided**:
- Summary stats (total runs, miles, time, elevation)
- Average metrics (pace, distance, time, heart rate)
- Best performances (fastest pace, longest run, longest time)
- Weekly and monthly trends
- Day-of-week analysis

### 3. StravaDataService (`strava_data_service.py`)

Service for interacting with the Strava API to fetch user data.

**Key Features**:
- Activity data retrieval with pagination
- User profile fetching
- Error handling and logging

**Main Methods**:
- `get_activities(token, max_pages)`: Fetch user activities with pagination
- `get_user_profile(token)`: Fetch user profile information

**Configuration**:
- Uses environment variables for API credentials
- Supports pagination up to 20 pages (2000 activities)
- Handles API rate limiting and errors

### 4. FormatDataService (`format_data_service.py`)

Data processing and formatting service for Strava activity data.

**Key Features**:
- Activity data formatting and normalization
- Unit conversions (meters to miles, seconds to minutes)
- Speed conversion (m/s to minutes per mile)
- Data cleaning and validation
- CSV file processing

**Main Methods**:
- `format_activity(activity)`: Format individual activity data
- `format_data(data)`: Format list of activities into DataFrame
- `fix_data(file_name)`: Process and clean data file
- `load_data(file_name)`: Load processed data

**Data Transformations**:
- Distance: meters → miles
- Time: seconds → minutes
- Speed: m/s → minutes per mile
- Date parsing and timezone handling
- Missing value handling

### 5. GraphService (`graph_service.py`)

Comprehensive visualization service for running data analysis.

**Key Features**:
- Multiple chart types (line, bar, scatter, histogram)
- Professional styling with seaborn
- Statistical analysis integration
- Individual and combined graph generation
- High-quality image output

**Chart Types**:
- Distance over time with trend lines
- Pace distribution histograms
- Heart rate trends
- Weekly mileage analysis
- Speed vs distance scatter plots
- Suffer score analysis
- Monthly summaries
- Cadence analysis

**Main Methods**:
- `graph_data(df)`: Generate comprehensive multi-chart analysis
- `create_individual_graphs(df)`: Create separate charts
- `create_weekly_mileage_line_graph(df)`: Specialized weekly trend chart
- `save_graph(fig, filename)`: Save charts to files

### 6. StravaAuthService (`strava_auth_service.py`)

Authentication service for Strava OAuth integration.

**Key Features**:
- OAuth 2.0 authorization flow
- Access token management
- Token refresh handling
- Environment-based configuration

**Main Methods**:
- `get_auth_url()`: Generate Strava authorization URL
- `get_access_token()`: Exchange code for access token
- `refresh_access_token()`: Refresh expired tokens
- `get_access()`: Complete authorization flow

**Configuration**:
- Uses environment variables for client credentials
- Supports `activity:read_all` scope
- Handles OAuth callback processing

## Data Flow

### 1. Data Ingestion
1. User authorizes application via Strava OAuth
2. Access token obtained and stored
3. Strava API called to fetch activities
4. Raw data formatted and processed
5. Processed data saved to CSV files

### 2. Query Processing
1. User submits natural language query
2. Query analyzed and enhanced by AI
3. Code generated for data analysis or chart creation
4. Code executed with user's data
5. Results formatted and returned

### 3. Chart Generation
1. Query determined to require visualization
2. Seaborn/matplotlib code generated
3. Code executed to create chart
4. Chart saved as PNG file
5. Chart URL returned to user

## Error Handling

The application implements comprehensive error handling:

- **HTTP Exceptions**: Proper HTTP status codes and error messages
- **Data Validation**: Pydantic models for request/response validation
- **Service Errors**: Graceful degradation when services fail
- **File System**: Checks for required data files
- **API Errors**: Strava API error handling and logging

## Configuration

### Environment Variables
- `CLIENT_ID`: Strava application client ID
- `CLIENT_SECRET`: Strava application client secret
- `REDIRECT_URI`: OAuth callback URL
- `OPENAI_API_KEY`: OpenAI API key for AI workflow

### File Dependencies
- `fixed_formatted_run_data.csv`: Processed running data
- `data/formatted_data.csv`: Raw formatted data
- `chart.png`: Generated chart output

## Security Considerations

- **Token Management**: Access tokens handled securely
- **CORS Configuration**: Configurable CORS settings
- **Input Validation**: Pydantic model validation
- **Error Information**: Limited error detail exposure
- **File Access**: Controlled file system access

## Performance Considerations

- **Async Operations**: FastAPI async endpoints
- **Data Caching**: Processed data cached in CSV files
- **Pagination**: Strava API pagination support
- **Background Tasks**: Non-blocking data processing
- **Resource Management**: Proper cleanup of resources

## Development and Testing

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export CLIENT_ID="your_client_id"
export CLIENT_SECRET="your_client_secret"
export REDIRECT_URI="your_redirect_uri"
export OPENAI_API_KEY="your_openai_key"

# Run the application
python main.py
```

### API Documentation
- Interactive docs available at `/docs`
- ReDoc documentation at `/redoc`
- OpenAPI schema at `/openapi.json`

### Testing Endpoints
- Health check: `GET /health`
- Data status: `GET /data/status`
- Example queries: `GET /examples`

## Future Enhancements

### Potential Improvements
- **Database Integration**: Replace CSV files with proper database
- **Caching Layer**: Redis for improved performance
- **User Management**: Multi-user support with proper authentication
- **Advanced Analytics**: Machine learning insights
- **Real-time Updates**: WebSocket support for live data
- **Export Features**: Data export in multiple formats
- **Custom Dashboards**: User-configurable analytics views

### Scalability Considerations
- **Microservices**: Split into smaller, focused services
- **Load Balancing**: Multiple application instances
- **Database Scaling**: Proper database architecture
- **CDN Integration**: Static asset delivery
- **Monitoring**: Application performance monitoring

## Conclusion

The Strava Stats backend provides a robust, AI-powered platform for analyzing running data. Its modular architecture, comprehensive error handling, and extensive API make it suitable for both individual use and potential scaling to serve multiple users. The integration of modern AI capabilities with traditional data analysis creates a powerful tool for runners to gain insights into their training and performance.