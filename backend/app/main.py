from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from .database import get_db, create_tables
from .models import Propriedade, Bairro, TipoProprietario, Finalidade, Endereco
from .tax_calculator import TaxCalculator
from .data_importer import DataImporter

app = FastAPI(
    title="Sistema de Imposto Predial",
    description="Sistema de cálculo de impostos prediais para Maputo",
    version="1.0.0"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {
        "message": "Sistema de Imposto Predial - API",
        "version": "1.0.0",
        "endpoints": {
            "properties": "/api/properties",
            "neighborhoods": "/api/neighborhoods",
            "tax_calculation": "/api/properties/{id}/tax",
            "import_data": "/api/import-data",
            "statistics": "/api/statistics"
        }
    }

@app.post("/api/import-data")
def import_data():
    """Import data from Excel files"""
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data")
        importer = DataImporter(data_path)
        importer.import_all_data()
        return {"message": "Data imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing data: {str(e)}")

@app.get("/api/properties")
def get_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of properties with pagination and search"""
    query = db.query(Propriedade).join(Endereco, Propriedade.endereco_cod == Endereco.cod_r, isouter=True)
    
    if search:
        query = query.filter(
            Propriedade.nome.contains(search) |
            Propriedade.matriz.contains(search) |
            Propriedade.nuit.contains(search)
        )
    
    total = query.count()
    properties = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "properties": [
            {
                "id": prop.id,
                "ncontr": prop.ncontr,
                "nome": prop.nome,
                "matriz": prop.matriz,
                "valpatr": prop.valpatr,
                "cod_bairro": prop.cod_bairro,
                "proprietar": prop.proprietar,
                "nuit": prop.nuit,
                "localizacao": prop.endereco.morada if prop.endereco else prop.cod_localizaca
            }
            for prop in properties
        ]
    }

@app.get("/api/properties/{property_id}")
def get_property(property_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific property"""
    property = db.query(Propriedade).join(Endereco, Propriedade.endereco_cod == Endereco.cod_r, isouter=True).filter(Propriedade.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return {
        "id": property.id,
        "ncontr": property.ncontr,
        "nome": property.nome,
        "matriz": property.matriz,
        "valpatr": property.valpatr,
        "cod_bairro": property.cod_bairro,
        "proprietar": property.proprietar,
        "nuit": property.nuit,
        "cod_localizaca": property.cod_localizaca,
        "localizacao": property.endereco.morada if property.endereco else property.cod_localizaca,
        "nu_entrada": property.nu_entrada,
        "andar_n": property.andar_n,
        "flat": property.flat,
        "are_tereno": property.are_tereno,
        "are_constr": property.are_constr,
        "factant": property.factant,
        "finalidade_id": property.finalidade_id,
        "data_cria": property.data_cria
    }

@app.get("/api/properties/{property_id}/tax")
def calculate_property_tax(property_id: int, db: Session = Depends(get_db)):
    """Calculate tax for a specific property"""
    try:
        calculator = TaxCalculator(db)
        result = calculator.calculate_property_tax(property_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating tax: {str(e)}")

@app.get("/api/neighborhoods")
def get_neighborhoods(db: Session = Depends(get_db)):
    """Get list of neighborhoods with tax factors"""
    neighborhoods = db.query(Bairro).all()
    return [
        {
            "id": bairro.id,
            "cod_b": bairro.cod_b,
            "descricao": bairro.descricao,
            "fact": bairro.fact,
            "cod_dist_urb": bairro.cod_dist_urb
        }
        for bairro in neighborhoods
    ]

@app.get("/api/owner-types")
def get_owner_types(db: Session = Depends(get_db)):
    """Get list of owner types"""
    types = db.query(TipoProprietario).all()
    return [
        {
            "codigo": tipo.codigo,
            "descricao": tipo.descricao
        }
        for tipo in types
    ]

@app.get("/api/purposes")
def get_purposes(db: Session = Depends(get_db)):
    """Get list of property purposes"""
    purposes = db.query(Finalidade).all()
    return [
        {
            "codigo": finalidade.codigo,
            "descricao": finalidade.descricao
        }
        for finalidade in purposes
    ]

@app.get("/api/statistics")
def get_statistics(db: Session = Depends(get_db)):
    """Get tax collection statistics"""
    try:
        calculator = TaxCalculator(db)
        stats = calculator.get_tax_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

@app.post("/api/calculate-tax")
def calculate_custom_tax(
    base_value: float,
    neighborhood_code: int,
    age_factor_code: str,
    property_type: int = 1,
    db: Session = Depends(get_db)
):
    """Calculate tax with custom parameters"""
    try:
        calculator = TaxCalculator(db)
        
        neighborhood_factor = calculator.get_neighborhood_factor(neighborhood_code)
        age_factor = calculator.get_age_factor(age_factor_code, property_type)
        
        tax_amount = base_value * neighborhood_factor * age_factor
        
        return {
            "base_value": base_value,
            "neighborhood_factor": neighborhood_factor,
            "age_factor": age_factor,
            "tax_amount": round(tax_amount, 2),
            "calculation": f"{base_value} × {neighborhood_factor} × {age_factor} = {round(tax_amount, 2)}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating tax: {str(e)}")
