# Running Stats Backend

A FastAPI backend service for analyzing Strava running data using AI-powered chat workflow.

## Features

- **Strava OAuth Integration**: Secure authentication with Strava API
- **Data Processing**: Automatic fetching and formatting of user activities
- **AI Analysis**: Natural language query processing with chat workflow
- **Chart Generation**: Dynamic chart creation from user data
- **RESTful API**: Clean, documented API endpoints

## API Endpoints

### Authentication
- `POST /auth/token` - Exchange Strava authorization code for access token

### Data Management
- `POST /data/refresh` - Fetch fresh Strava data and update workflow dataset
- `GET /data/status` - Get current status of user's data and workflow

### Analysis
- `POST /query` - Process natural language analysis queries
- `GET /data/overview` - Get dataset overview and statistics
- `GET /examples` - Get example queries
- `GET /chart.png` - Get generated chart image

### Health & Status
- `GET /` - Root endpoint with basic status
- `GET /health` - Detailed health check
- `GET /docs` - Interactive API documentation (Swagger UI)

## Data Flow

1. **User Authentication**: User authorizes via Strava OAuth
2. **Token Exchange**: Backend exchanges auth code for access token
3. **Data Fetching**: Backend fetches user activities from Strava API
4. **Data Processing**: Activities are formatted and processed using `FormatDataService`
5. **Workflow Update**: Analysis workflow is updated with fresh data
6. **Query Processing**: Users can analyze data using natural language queries

## Setup

### Prerequisites

- Python 3.8+
- Strava API credentials (Client ID, Client Secret)
- Required Python packages (see requirements.txt)

### Installation

1. Clone the repository and navigate to backend directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file with your Strava credentials:
   ```env
   CLIENT_ID=your_strava_client_id
   CLIENT_SECRET=your_strava_client_secret
   REDIRECT_URI=http://localhost:4200/token
   ```

4. Start the server:
   ```bash
   python main.py
   ```

The server will run on `http://localhost:8000`

## Data Processing

### FormatDataService

The `FormatDataService` handles:
- Converting Strava API responses to structured format
- Filtering for running activities only
- Data cleaning and normalization
- Unit conversions (meters to miles, seconds to minutes)
- Speed calculations (m/s to minutes/mile)

### Output Files

- `data/formatted_data.csv` - Raw formatted data from Strava
- `fixed_formatted_run_data.csv` - Processed and cleaned data for analysis

## Testing

Run the test script to verify endpoints:
```bash
python test_data_refresh.py
```

## Development

### Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── services/               # Business logic services
│   ├── strava_auth_service.py    # Strava OAuth handling
│   ├── strava_data_service.py    # Strava API integration
│   ├── format_data_service.py    # Data processing
│   └── chat_workflow.py          # AI analysis workflow
├── routes/                 # API route handlers
│   └── analysis.py         # Analysis endpoints
├── data/                   # Data storage directory
└── requirements.txt        # Python dependencies
```

### Adding New Endpoints

1. Define Pydantic models for request/response
2. Add endpoint function to main.py or appropriate router
3. Include proper error handling and logging
4. Update API documentation

## Security Considerations

- **Token Storage**: Access tokens are not permanently stored
- **CORS**: Configured for development (allow_origins=["*"])
- **Input Validation**: All inputs validated using Pydantic models
- **Error Handling**: Sensitive information not exposed in error messages

## Production Deployment

- Set `allow_origins` to specific frontend domains
- Use environment variables for all sensitive configuration
- Implement proper logging and monitoring
- Consider rate limiting for API endpoints
- Use HTTPS in production
