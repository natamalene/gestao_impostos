from sqlalchemy.orm import Session
from .models import Propriedade, Bairro, FatorAntiguidade, PrecoReferencia
from typing import Dict, Optional
import re

class TaxCalculator:
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_property_tax(self, property_id: int) -> Dict:
        """
        Calculate property tax for a given property
        Formula: base_value × neighborhood_factor × age_factor
        """
        propriedade = self.db.query(Propriedade).filter(Propriedade.id == property_id).first()
        if not propriedade:
            raise ValueError(f"Property with ID {property_id} not found")
        
        base_value = propriedade.valpatr or 0
        
        neighborhood_factor = self.get_neighborhood_factor(propriedade.cod_bairro)
        
        age_factor = self.get_age_factor(propriedade.factant, propriedade.finalidade_id)
        
        tax_amount = base_value * neighborhood_factor * age_factor
        
        return {
            "property_id": property_id,
            "property_name": propriedade.nome,
            "base_value": base_value,
            "neighborhood_factor": neighborhood_factor,
            "age_factor": age_factor,
            "tax_amount": round(tax_amount, 2),
            "calculation_details": {
                "formula": "base_value × neighborhood_factor × age_factor",
                "calculation": f"{base_value} × {neighborhood_factor} × {age_factor} = {round(tax_amount, 2)}"
            }
        }
    
    def get_neighborhood_factor(self, cod_bairro: int) -> float:
        """Get neighborhood tax factor"""
        if not cod_bairro:
            return 1.0
            
        bairro = self.db.query(Bairro).filter(Bairro.cod_b == cod_bairro).first()
        return bairro.fact if bairro else 1.0
    
    def get_age_factor(self, factant_code: str, finalidade_id: int) -> float:
        """Get age factor based on property age and type"""
        if not factant_code:
            return 1.0
            
        fator = self.db.query(FatorAntiguidade).filter(FatorAntiguidade.cod == factant_code).first()
        if not fator:
            return 1.0
        
        if finalidade_id == 2:  # Commercial
            return fator.tipcom
        else:  # Residential or other
            return fator.tiphab
    
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
