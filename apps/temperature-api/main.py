from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from datetime import datetime, timezone
import uvicorn
import random
from typing import Optional
from pydantic import BaseModel

# Pydantic models matching the Go TemperatureResponse struct
class TemperatureResponse(BaseModel):
    value: float
    unit: str
    timestamp: datetime
    location: str
    status: str
    sensor_id: str
    sensor_type: str
    description: str

class TemperatureByLocationResponse(BaseModel):
    value: float
    unit: str
    timestamp: datetime
    location: str
    status: str = "active"
    sensor_id: str = "location_sensor"
    sensor_type: str = "temperature"
    description: str = "Temperature reading by location"

class TemperatureBySensorResponse(BaseModel):
    value: float
    unit: str
    timestamp: datetime
    location: str = "unknown"
    status: str = "active"
    sensor_id: str
    sensor_type: str = "temperature"
    description: str = "Temperature reading by sensor ID"

app = FastAPI(
    title="Temperature API",
    description="Simple temperature monitoring API for WarmHome Smart Home",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint - returns API status and basic information"""
    return JSONResponse(
        content={
            "message": "Temperature API is running",
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc),
            "version": "1.0.0",
            "service": "temperature-api"
        }
    )

@app.get("/temperature", response_model=TemperatureByLocationResponse)
async def get_temperature_by_location(location: Optional[str] = Query(None, description="Location to get temperature for")):
    """Get temperature reading by location"""
    # Generate random temperature between 15-30°C
    temperature = round(random.uniform(15.0, 30.0), 1)
    
    response_data = TemperatureByLocationResponse(
        value=temperature,
        unit="°C",
        timestamp=datetime.now(timezone.utc),
        location=location or "unknown"
    )
    
    return response_data

@app.get("/temperature/{sensor_id}", response_model=TemperatureBySensorResponse)
async def get_temperature_by_sensor(sensor_id: str):
    """Get temperature reading by sensor ID"""
    # Generate random temperature between 15-30°C
    temperature = round(random.uniform(15.0, 30.0), 1)
    
    response_data = TemperatureBySensorResponse(
        value=temperature,
        unit="°C",
        timestamp=datetime.now(timezone.utc),
        sensor_id=sensor_id
    )
    
    return response_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
