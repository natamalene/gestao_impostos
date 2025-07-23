from sqlalchemy.orm import Session
from .models import Propriedade, Bairro, FatorAntiguidade, PrecoReferencia
from typing import Dict, Optional
import re

class TaxCalculator:
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_ipra_tax(self, built_area: float, construction_price: float, 
                          age_factor: float, land_area: float, location_factor: float, 
                          property_type: str = "residential") -> Dict:
        """
        Calculate IPRA tax using official formula from Article 4:
        Vipra = Vp × taxa
        Where Vp = (Ae × P × Fa + 0,00 × Al × P) × Fl
        """
        vp = (built_area * construction_price * age_factor + 0.00 * land_area * construction_price) * location_factor
        
        tax_rate = 0.001 if property_type == "residential" else 0.002
        
        vipra = vp * tax_rate
        
        return {
            "patrimonial_value": round(vp, 2),
            "tax_rate": tax_rate,
            "ipra_tax": round(vipra, 2),
            "formula_details": {
                "built_area": built_area,
                "construction_price": construction_price,
                "age_factor": age_factor,
                "land_area": land_area,
                "location_factor": location_factor,
                "calculation": f"({built_area} × {construction_price} × {age_factor} + 0.00 × {land_area} × {construction_price}) × {location_factor} × {tax_rate}"
            }
        }
    
    def calculate_property_tax(self, property_id: int) -> Dict:
        """
        Calculate property tax for a given property using IPRA formula
        """
        propriedade = self.db.query(Propriedade).filter(Propriedade.id == property_id).first()
        if not propriedade:
            raise ValueError(f"Property with ID {property_id} not found")
        
        built_area = float(propriedade.are_constr) if propriedade.are_constr else 100.0
        land_area = float(propriedade.are_tereno) if propriedade.are_tereno else 0.0
        construction_price = self.get_construction_price()
        age_factor = self.get_age_factor(propriedade.factant, propriedade.finalidade_id)
        location_factor = self.get_neighborhood_factor(propriedade.cod_bairro)
        property_type = "commercial" if propriedade.finalidade_id == 2 else "residential"
        
        result = self.calculate_ipra_tax(built_area, construction_price, age_factor, 
                                       land_area, location_factor, property_type)
        
        result.update({
            "property_id": property_id,
            "property_name": propriedade.nome,
            "property_ncontr": propriedade.ncontr
        })
        
        return result
    
    def get_neighborhood_factor(self, cod_bairro: int) -> float:
        """Get neighborhood tax factor (location factor)"""
        if not cod_bairro:
            return 1.0
            
        bairro = self.db.query(Bairro).filter(Bairro.cod_b1 == cod_bairro).first()
        return bairro.fact if bairro else 1.0
    
    def get_age_factor(self, factant_code: str, finalidade_id: int) -> float:
        """Get age factor based on property age and type"""
        if not factant_code:
            return 1.0
            
        fator = self.db.query(FatorAntiguidade).filter(FatorAntiguidade.cod == factant_code).first()
        if not fator:
            return 1.0
        
        if finalidade_id == 2:
            return fator.tipcom
        else:
            return fator.tiphab
    
    def get_construction_price(self) -> float:
        """Get current construction price per square meter"""
        preco = self.db.query(PrecoReferencia).order_by(PrecoReferencia.ano.desc()).first()
        return preco.preco if preco else 15000.0
    
    def calculate_bulk_taxes(self, limit: int = 100) -> list:
        """Calculate taxes for multiple properties"""
        propriedades = self.db.query(Propriedade).limit(limit).all()
        results = []
        
        for prop in propriedades:
            try:
                tax_result = self.calculate_property_tax(prop.id)
                results.append(tax_result)
            except Exception as e:
                results.append({
                    "property_id": prop.id,
                    "error": str(e)
                })
        
        return results
    
    def get_tax_statistics(self) -> Dict:
        """Get tax collection statistics"""
        total_properties = self.db.query(Propriedade).count()
        
        sample_taxes = self.calculate_bulk_taxes(1000)
        valid_taxes = [t for t in sample_taxes if "tax_amount" in t]
        
        if valid_taxes:
            total_tax = sum(t["tax_amount"] for t in valid_taxes)
            avg_tax = total_tax / len(valid_taxes)
            max_tax = max(t["tax_amount"] for t in valid_taxes)
            min_tax = min(t["tax_amount"] for t in valid_taxes)
        else:
            total_tax = avg_tax = max_tax = min_tax = 0
        
        return {
            "total_properties": total_properties,
            "sample_size": len(valid_taxes),
            "total_tax_sample": round(total_tax, 2),
            "average_tax": round(avg_tax, 2),
            "max_tax": round(max_tax, 2),
            "min_tax": round(min_tax, 2)
        }
