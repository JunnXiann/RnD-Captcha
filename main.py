"""
FastAPI backend for Tencent CAPTCHA verification with mock mode support.
"""
import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Tencent CAPTCHA Mock API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
TENCENT_CAPTCHA_APP_ID = os.getenv("TENCENT_CAPTCHA_APP_ID", "")
TENCENT_CAPTCHA_SECRET = os.getenv("TENCENT_CAPTCHA_SECRET", "")
MOCK_CAPTCHA = os.getenv("MOCK_CAPTCHA", "false").lower() == "true"

# Tencent CAPTCHA API endpoint
TENCENT_API_URL = "https://ssl.captcha.qq.com/ticket/verify"


class CaptchaRequest(BaseModel):
    """Request model for CAPTCHA verification."""
    ticket: str
    randstr: str


class CaptchaResponse(BaseModel):
    """Response model for CAPTCHA verification."""
    success: bool
    message: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Tencent CAPTCHA Mock API",
        "mock_mode": MOCK_CAPTCHA,
        "status": "running"
    }


@app.post("/verify-captcha", response_model=CaptchaResponse)
async def verify_captcha(request: CaptchaRequest):
    """
    Verify CAPTCHA ticket and randstr.
    
    If MOCK_CAPTCHA=true, returns success immediately.
    Otherwise, calls Tencent CAPTCHA API for verification.
    """
    logger.info(f"Received CAPTCHA verification request. Mock mode: {MOCK_CAPTCHA}")
    
    # Mock mode: always return success
    if MOCK_CAPTCHA:
        logger.info("Mock mode enabled - returning success")
        return CaptchaResponse(
            success=True,
            message="Mock verification successful"
        )
    
    # Real verification mode
    if not TENCENT_CAPTCHA_APP_ID or not TENCENT_CAPTCHA_SECRET:
        logger.error("Tencent CAPTCHA credentials not configured")
        raise HTTPException(
            status_code=500,
            detail="Tencent CAPTCHA credentials not configured"
        )
    
    try:
        # Prepare request parameters
        params = {
            "aid": TENCENT_CAPTCHA_APP_ID,
            "AppSecretKey": TENCENT_CAPTCHA_SECRET,
            "Ticket": request.ticket,
            "Randstr": request.randstr,
            "UserIP": "127.0.0.1"  # In production, use actual client IP
        }
        
        logger.info("Calling Tencent CAPTCHA API for verification")
        
        # Call Tencent CAPTCHA API
        async with httpx.AsyncClient() as client:
            response = await client.get(TENCENT_API_URL, params=params, timeout=10.0)
            response.raise_for_status()
            result = response.json()
        
        logger.info(f"Tencent API response: {result}")
        
        # Check if verification was successful
        # Tencent returns {"response": "1", "evil_level": "0", "err_msg": "OK"}
        # CaptchaCode or response == "1" indicates success
        captcha_code = result.get("response")
        
        if captcha_code == "1" or captcha_code == 1:
            return CaptchaResponse(
                success=True,
                message="CAPTCHA verification successful"
            )
        else:
            return CaptchaResponse(
                success=False,
                message=result.get("err_msg", "CAPTCHA verification failed")
            )
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP error calling Tencent API: {e}")
        raise HTTPException(
            status_code=502,
            detail=f"Error calling Tencent CAPTCHA API: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during verification: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during verification: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
