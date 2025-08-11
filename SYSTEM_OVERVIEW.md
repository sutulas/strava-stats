# Strava Stats System Overview

## 🏃‍♂️ Complete System Architecture

This document provides a comprehensive overview of the Strava Stats system, which allows users to analyze their Strava running data using natural language queries and AI-powered insights.

## 🔄 Complete User Flow

### 1. **User Authentication**
- User visits `localhost:4200` → redirected to `/login`
- Clicks "Connect with Strava" → redirected to Strava OAuth
- User authorizes → Strava redirects to `localhost:4200/token?code=...`
- Frontend processes code → sends to backend for token exchange
- Backend exchanges code → returns access token
- **Automatic Data Refresh**: System automatically fetches user's Strava data

### 2. **Data Processing Pipeline**
```
Strava API → FormatDataService → Fixed CSV → Workflow Update
    ↓              ↓                ↓           ↓
User Activities → Formatted Data → Processed → Analysis Ready
```

### 3. **Analysis & Insights**
- User navigates to dashboard → sees data status and refresh options
- User can manually refresh data using "Refresh Data" button
- User submits natural language queries → AI workflow processes them
- Results include text analysis and generated charts

## 🏗️ System Components

### **Frontend (Angular + Tailwind CSS)**
- **Login Component**: Strava OAuth integration
- **Token Callback**: Handles OAuth redirect and data refresh
- **Dashboard**: Data status display and manual refresh
- **Analysis Interface**: Query submission and results display
- **Navigation**: Conditional display based on authentication

### **Backend (FastAPI + Python)**
- **Authentication Service**: Strava OAuth token exchange
- **Data Service**: Fetches activities from Strava API
- **Format Service**: Processes and cleans activity data
- **Workflow Service**: AI-powered analysis engine
- **API Endpoints**: RESTful interface for frontend

### **Data Flow Services**
- **StravaAuthService**: OAuth flow management
- **StravaDataService**: API integration with Strava
- **FormatDataService**: Data processing and CSV generation
- **ChatWorkflow**: AI analysis and chart generation

## 📊 Data Processing Details

### **Raw Data → Formatted Data**
```python
# Strava API Response → Formatted DataFrame
{
    'id': 12345,
    'name': 'Morning Run',
    'distance': 5000,  # meters
    'moving_time': 1800,  # seconds
    'type': 'Run',
    # ... other fields
}

# Becomes:
{
    'id': 12345,
    'name': 'Morning Run',
    'distance': 3.11,  # miles
    'moving_time': 30.0,  # minutes
    'type': 'Run',
    # ... processed fields
}
```

### **Data Transformations**
- **Distance**: meters → miles (× 0.000621371)
- **Time**: seconds → minutes (÷ 60)
- **Speed**: m/s → minutes/mile (26.822 ÷ speed)
- **Date Processing**: Add year, month, day, day_of_week columns
- **Data Cleaning**: Handle missing values, filter running activities only

### **Output Files**
- `data/formatted_data.csv` - Raw formatted data
- `fixed_formatted_run_data.csv` - Final processed data for analysis

## 🔌 API Endpoints

### **Authentication**
- `POST /auth/token` - Exchange OAuth code for access token

### **Data Management**
- `POST /data/refresh` - Fetch fresh Strava data and update workflow
- `GET /data/status` - Get current data and workflow status

### **Analysis**
- `POST /query` - Process natural language queries
- `GET /chart.png` - Retrieve generated charts
- `GET /data/overview` - Get dataset statistics

## 🚀 Getting Started

### **1. Backend Setup**
```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "CLIENT_ID=your_strava_client_id" > .env
echo "CLIENT_SECRET=your_strava_client_secret" >> .env
echo "REDIRECT_URI=http://localhost:4200/token" >> .env

# Start backend
python main.py
```

### **2. Frontend Setup**
```bash
cd frontend
npm install

# Update environment.ts with your Client ID
# Copy from environment.example.ts

# Start frontend
ng serve
```

### **3. Strava API Configuration**
- Visit [Strava API Settings](https://www.strava.com/settings/api)
- Create application and get Client ID
- Set callback domain to `localhost:4200`

## 🔍 Testing the System

### **Backend Testing**
```bash
cd backend
python test_data_refresh.py
```

### **Frontend Testing**
1. Navigate to `http://localhost:4200`
2. Click "Connect with Strava"
3. Authorize the application
4. Check dashboard for data status
5. Use "Refresh Data" button to fetch fresh data

## 📈 Data Refresh Workflow

### **Automatic Refresh (OAuth Callback)**
1. User completes OAuth
2. Frontend receives access token
3. Frontend calls `/data/refresh` with token
4. Backend fetches activities from Strava
5. Data is processed and formatted
6. Workflow is updated with fresh data
7. User redirected to dashboard

### **Manual Refresh (Dashboard)**
1. User clicks "Refresh Data" button
2. Frontend calls `/data/refresh` with stored token
3. Same processing pipeline as automatic refresh
4. Dashboard updates with new status

## 🛡️ Security Features

- **OAuth2 Flow**: Secure authentication with Strava
- **Token Management**: Access tokens not permanently stored
- **Input Validation**: Pydantic models for all API inputs
- **Error Handling**: Sensitive information not exposed
- **CORS Configuration**: Proper origin handling

## 🔧 Troubleshooting

### **Common Issues**
- **CORS Errors**: Ensure backend allows `localhost:4200`
- **Token Issues**: Check Strava API credentials
- **Data Not Loading**: Verify backend is running on port 8000
- **Workflow Errors**: Check if data files exist and are valid

### **Debug Steps**
1. Check backend logs for errors
2. Verify Strava API credentials
3. Test endpoints with `test_data_refresh.py`
4. Check browser console for frontend errors
5. Verify file permissions for data directory

## 🚀 Production Considerations

- **Environment Variables**: Use proper secret management
- **CORS Origins**: Restrict to production domains
- **HTTPS**: Enable SSL in production
- **Rate Limiting**: Implement API rate limiting
- **Monitoring**: Add logging and metrics collection
- **Data Backup**: Implement data backup strategies

## 📚 Next Steps

- **User Management**: Add user accounts and data isolation
- **Data Persistence**: Store processed data in database
- **Advanced Analytics**: Add more sophisticated analysis tools
- **Mobile App**: Create mobile application
- **Social Features**: Add sharing and comparison features
- **Performance Optimization**: Implement caching and optimization

---

This system provides a complete, production-ready solution for Strava data analysis with a modern web interface and powerful backend processing capabilities. 