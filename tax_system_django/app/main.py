from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio

app = FastAPI(title="Tax System API Wrapper")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DJANGO_BASE_URL = "https://user:123377f234c92f847f900a2c9233f99a@imposto-sistema-app-tunnel-v5us3yx4.devinapps.com"

@app.get("/")
async def root():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_BASE_URL}/")
        return response.json()

@app.get("/api/statistics/")
async def get_statistics():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_BASE_URL}/api/statistics/")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/api/neighborhoods/")
async def get_neighborhoods():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_BASE_URL}/api/neighborhoods/")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/api/properties/")
async def get_properties():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_BASE_URL}/api/properties/")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/api/properties/{property_id}/")
async def get_property_details(property_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_BASE_URL}/api/properties/{property_id}/")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/api/owner-types/")
async def get_owner_types():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_BASE_URL}/api/owner-types/")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/api/purposes/")
async def get_purposes():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_BASE_URL}/api/purposes/")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/api/age-factors/")
async def get_age_factors():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_BASE_URL}/api/age-factors/")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/api/addresses/")
async def get_addresses():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_BASE_URL}/api/addresses/")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/api/calculate-tax/")
async def calculate_tax(request_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{DJANGO_BASE_URL}/api/calculate-tax/", json=request_data)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/api/simulate-tax/")
async def simulate_tax(request_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{DJANGO_BASE_URL}/api/simulate-tax/", json=request_data)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/api/properties/{property_id}/tax/")
async def get_property_tax(property_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_BASE_URL}/api/properties/{property_id}/tax/")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
