from fastapi import FastAPI, Depends, HTTPException, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import os

from .database import get_db, create_tables
from .models import Propriedade, Bairro, TipoProprietario, Finalidade, FatorAntiguidade, PrecoReferencia, Endereco
from .tax_calculator import TaxCalculator
from .data_importer import DataImporter

app = FastAPI(
    title="Sistema de Imposto Predial",
    description="Sistema de cálculo de impostos prediais para Maputo",
    version="1.0.0"
)

class PropertyCreateRequest(BaseModel):
    nome: str
    matriz: str | None = None
    cod_bairro: int
    proprietar: int | None = None
    nuit: str | None = None
    endereco_cod: str | None = None
    finalidade_id: int | None = None
    are_tereno: str | None = None
    are_constr: str | None = None
    factant: str | None = None

class TaxSimulationRequest(BaseModel):
    built_area: float
    construction_price: float | None = None
    construction_year: int = 2025
    age_factor_code: str | None = None
    logradouro_area: float = 0.0
    neighborhood_code: int
    property_type: str = "residential"

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
    query = db.query(Propriedade).join(Endereco, Propriedade.endereco_cod == Endereco.cod_r, isouter=True).join(Bairro, Propriedade.cod_bairro == Bairro.cod_b1, isouter=True)
    
    if search:
        query = query.filter(
            Propriedade.nome.contains(search) |
            Propriedade.matriz.contains(search) |
            Propriedade.nuit.contains(search)
        )
    
    total = query.count()
    properties = query.offset(skip).limit(limit).all()
    
    calculator = TaxCalculator(db)
    properties_with_ipra = []
    
    for prop in properties:
        property_data = {
            "id": prop.id,
            "codigo": prop.ncontr,
            "nome": prop.nome,
            "matriz": prop.matriz,
            "valpatr": prop.valpatr,
            "cod_bairro": prop.cod_bairro,
            "bairro": prop.bairro.descricao if prop.bairro else f"Bairro {prop.cod_bairro}",
            "proprietar": prop.proprietar,
            "nuit": prop.nuit,
            "localizacao": prop.endereco.morada if prop.endereco else prop.cod_localizaca
        }
        
        try:
            ipra_result = calculator.calculate_property_tax(prop.id)
            property_data["ipra_value"] = ipra_result["ipra_tax"]
        except Exception as e:
            property_data["ipra_value"] = None
            
        properties_with_ipra.append(property_data)
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "properties": properties_with_ipra
    }

@app.get("/api/properties/{property_id}")
def get_property(property_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific property"""
    property = db.query(Propriedade).join(Endereco, Propriedade.endereco_cod == Endereco.cod_r, isouter=True).join(Bairro, Propriedade.cod_bairro == Bairro.cod_b1, isouter=True).filter(Propriedade.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return {
        "id": property.id,
        "codigo": property.ncontr,
        "nome": property.nome,
        "matriz": property.matriz,
        "valpatr": property.valpatr,
        "cod_bairro": property.cod_bairro,
        "bairro": property.bairro.descricao if property.bairro else f"Bairro {property.cod_bairro}",
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
            "cod_b": bairro.cod_b1,
            "cod_b1": bairro.cod_b1,
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
    base_value: float = Form(...),
    neighborhood_code: int = Form(...),
    age_factor_code: str = Form(...),
    property_type: str = Form("residential"),
    db: Session = Depends(get_db)
):
    """Calculate tax with custom parameters using IPRA formula"""
    try:
        calculator = TaxCalculator(db)
        
        built_area = base_value / 9143.73 if base_value > 0 else 100.0
        construction_price = calculator.get_construction_price()
        age_factor = calculator.get_age_factor(age_factor_code, 2 if property_type == "commercial" else 1)
        location_factor = calculator.get_neighborhood_factor(neighborhood_code)
        
        result = calculator.calculate_ipra_tax(
            built_area=built_area,
            construction_price=construction_price,
            age_factor=age_factor,
            logradouro_area=0.0,
            location_factor=location_factor,
            property_type=property_type
        )
        
        return {
            "base_value": base_value,
            "neighborhood_factor": location_factor,
            "age_factor": age_factor,
            "tax_amount": result["ipra_tax"],
            "calculation": result["formula_details"]["calculation"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating tax: {str(e)}")

@app.post("/api/properties")
def create_property(property_data: PropertyCreateRequest, db: Session = Depends(get_db)):
    """Create a new property with auto-generated CODIGO and auto-calculated Valor Patrimonial"""
    try:
        max_codigo = db.query(Propriedade).order_by(Propriedade.ncontr.desc()).first()
        new_codigo = (max_codigo.ncontr + 1) if max_codigo else 1000000
        
        bairro = db.query(Bairro).filter(Bairro.cod_b1 == property_data.cod_bairro).first()
        if not bairro:
            raise HTTPException(status_code=400, detail="Invalid neighborhood code")
        
        if property_data.factant:
            age_factor = db.query(FatorAntiguidade).filter(FatorAntiguidade.cod == property_data.factant).first()
            if not age_factor:
                raise HTTPException(status_code=400, detail="Invalid age factor code")
        
        calculator = TaxCalculator(db)
        built_area = float(property_data.are_constr) if property_data.are_constr else 100.0
        logradouro_area = float(property_data.are_tereno) if property_data.are_tereno else 0.0
        construction_price = calculator.get_construction_price(2025)
        age_factor = calculator.get_age_factor(property_data.factant, property_data.finalidade_id) if property_data.factant else 1.0
        location_factor = calculator.get_neighborhood_factor(property_data.cod_bairro)
        property_type = "commercial" if property_data.finalidade_id == 2 else "residential"
        
        ipra_result = calculator.calculate_ipra_tax(
            built_area=built_area,
            construction_price=construction_price,
            age_factor=age_factor,
            logradouro_area=logradouro_area,
            location_factor=location_factor,
            property_type=property_type
        )
        
        calculated_valpatr = ipra_result["patrimonial_value"]
        
        new_property = Propriedade(
            ncontr=new_codigo,
            nome=property_data.nome,
            matriz=property_data.matriz,
            valpatr=calculated_valpatr,
            cod_bairro=property_data.cod_bairro,
            proprietar=property_data.proprietar,
            nuit=property_data.nuit,
            endereco_cod=property_data.endereco_cod,
            finalidade_id=property_data.finalidade_id,
            are_tereno=property_data.are_tereno,
            are_constr=property_data.are_constr,
            factant=property_data.factant,
            data_cria=datetime.now()
        )
        
        db.add(new_property)
        db.commit()
        db.refresh(new_property)
        
        return {
            "message": "Property created successfully", 
            "id": new_property.id, 
            "codigo": new_property.ncontr,
            "valor_patrimonial": calculated_valpatr
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating property: {str(e)}")

@app.post("/api/simulate-tax")
def simulate_tax(simulation_data: TaxSimulationRequest, db: Session = Depends(get_db)):
    """Simulate tax calculation with custom parameters"""
    try:
        calculator = TaxCalculator(db)
        
        construction_price = simulation_data.construction_price or calculator.get_construction_price(simulation_data.construction_year)
        
        age_factor = 1.0
        if simulation_data.age_factor_code:
            finalidade_id = 2 if simulation_data.property_type == "commercial" else 1
            age_factor = calculator.get_age_factor(simulation_data.age_factor_code, finalidade_id)
        
        location_factor = calculator.get_neighborhood_factor(simulation_data.neighborhood_code)
        
        result = calculator.calculate_ipra_tax(
            built_area=simulation_data.built_area,
            construction_price=construction_price,
            age_factor=age_factor,
            logradouro_area=simulation_data.logradouro_area,
            location_factor=location_factor,
            property_type=simulation_data.property_type
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error simulating tax: {str(e)}")

@app.get("/api/age-factors")
def get_age_factors(db: Session = Depends(get_db)):
    """Get all age factors"""
    age_factors = db.query(FatorAntiguidade).all()
    return [
        {
            "id": f.id,
            "cod": f.cod,
            "id_range": f.id_range,
            "tiphab": f.tiphab,
            "tipcom": f.tipcom
        }
        for f in age_factors
    ]

@app.get("/api/addresses")
def get_addresses(db: Session = Depends(get_db)):
    """Get all addresses"""
    addresses = db.query(Endereco).all()
    return [
        {
            "id": e.id,
            "cod_r": e.cod_r,
            "morada": e.morada
        }
        for e in addresses
    ]
