# RnD-Captcha

A Tencent CAPTCHA integration demo with mock mode support. This project provides a complete implementation with a FastAPI backend and a simple HTML/JavaScript frontend.

## Features

- ✅ **FastAPI Backend**: High-performance API with async support
- ✅ **CORS Enabled**: Cross-origin requests supported
- ✅ **Mock Mode**: Test without real CAPTCHA verification
- ✅ **Tencent CAPTCHA Integration**: Full integration with Tencent's CAPTCHA service
- ✅ **Simple Frontend**: Plain HTML/JS with TCaptcha.js

## Architecture

### Backend (FastAPI)
- **Framework**: FastAPI + Uvicorn
- **HTTP Client**: httpx for async requests
- **CORS**: Enabled for all origins
- **Endpoint**: `POST /verify-captcha`
  - Accepts: `{ticket, randstr}`
  - Returns: `{success: bool, message: str}`

### Frontend (HTML + JavaScript)
- **CAPTCHA SDK**: Tencent TCaptcha.js (https://ssl.captcha.qq.com/TCaptcha.js)
- **UI**: Simple button to trigger slider CAPTCHA
- **Communication**: Fetch API to send ticket/randstr to backend

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TENCENT_CAPTCHA_APP_ID` | Your Tencent CAPTCHA App ID | Yes (unless MOCK_CAPTCHA=true) |
| `TENCENT_CAPTCHA_SECRET` | Your Tencent CAPTCHA Secret Key | Yes (unless MOCK_CAPTCHA=true) |
| `MOCK_CAPTCHA` | Set to "true" to enable mock mode (bypasses real verification) | No (default: false) |

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/JunnXiann/RnD-Captcha.git
cd RnD-Captcha
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
# Get your credentials from: https://console.cloud.tencent.com/captcha
```

**For Testing (Mock Mode):**
```bash
# Set in .env file
MOCK_CAPTCHA=true
```

**For Production (Real CAPTCHA):**
```bash
# Set in .env file
TENCENT_CAPTCHA_APP_ID=your_app_id_here
TENCENT_CAPTCHA_SECRET=your_secret_key_here
MOCK_CAPTCHA=false
```

### 5. Run the Backend

```bash
# Option 1: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python
python main.py
```

The backend will start at `http://localhost:8000`

### 6. Open the Frontend

Simply open `index.html` in your web browser:

```bash
# On macOS
open index.html

# On Linux
xdg-open index.html

# On Windows
start index.html
```

Or serve it with a simple HTTP server:

```bash
# Python 3
python -m http.server 8080

# Then visit http://localhost:8080/index.html
```

## Usage

### Testing with Mock Mode

1. Set `MOCK_CAPTCHA=true` in your `.env` file
2. Start the backend server
3. Open `index.html` in your browser
4. Click "Verify with CAPTCHA" button
5. Complete the CAPTCHA challenge
6. Backend will automatically return success (bypassing real verification)

### Production with Real CAPTCHA

1. Register at [Tencent Cloud CAPTCHA Console](https://console.cloud.tencent.com/captcha)
2. Get your `App ID` and `Secret Key`
3. Set these values in your `.env` file
4. Set `MOCK_CAPTCHA=false`
5. Update `CAPTCHA_APP_ID` in `index.html` with your App ID
6. Start the backend server
7. Open the frontend and test the verification flow

## API Documentation

### GET /
Returns API status and configuration.

**Response:**
```json
{
  "service": "Tencent CAPTCHA Mock API",
  "mock_mode": true,
  "status": "running"
}
```

### POST /verify-captcha
Verifies CAPTCHA ticket and randstr.

**Request Body:**
```json
{
  "ticket": "string",
  "randstr": "string"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "CAPTCHA verification successful"
}
```

**Response (Failure):**
```json
{
  "success": false,
  "message": "CAPTCHA verification failed"
}
```

## Project Structure

```
RnD-Captcha/
├── main.py              # FastAPI backend application
├── index.html           # Frontend HTML with CAPTCHA integration
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment configuration
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Development

### Running with Auto-reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Checking Logs

The backend logs all CAPTCHA verification attempts. Check the console output for debugging.

### API Documentation

FastAPI provides automatic API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Backend won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is already in use
- Verify your Python version (3.7+ required)

### CAPTCHA not loading
- Check console for JavaScript errors
- Ensure you have internet connection (TCaptcha.js loads from CDN)
- Verify your App ID is correct in `index.html`

### Verification fails in production mode
- Verify your `TENCENT_CAPTCHA_APP_ID` and `TENCENT_CAPTCHA_SECRET` are correct
- Check backend logs for detailed error messages
- Ensure your Tencent CAPTCHA service is active

### CORS errors
- Backend has CORS enabled for all origins by default
- If using a different setup, update CORS configuration in `main.py`

## Security Notes

- Never commit your `.env` file with real credentials
- Use environment variables for sensitive data
- In production, restrict CORS to specific origins
- Consider adding rate limiting for the verification endpoint
- Use HTTPS in production

## License

MIT License - Feel free to use this project for learning and development.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.