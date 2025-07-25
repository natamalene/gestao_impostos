from django.db import models
from .models import Property, Neighborhood, AgeFactor, ConstructionPrice
from typing import Dict, Optional

class TaxCalculator:
    def __init__(self):
        pass
    
    def calculate_ipra_tax(self, built_area: float, construction_price: float, 
                          age_factor: float, logradouro_area: float, location_factor: float, 
                          property_type: str = "residential") -> Dict:
        vp = (built_area * construction_price * age_factor + 0.00 * logradouro_area * construction_price) * location_factor
        
        tax_rate = 0.004 if property_type == "residential" else 0.007
        
        vipra = vp * tax_rate
        
        return {
            "patrimonial_value": round(vp, 2),
            "tax_rate": tax_rate,
            "ipra_tax": round(vipra, 2),
            "formula_details": {
                "built_area": built_area,
                "construction_price": construction_price,
                "age_factor": age_factor,
                "logradouro_area": logradouro_area,
                "location_factor": location_factor,
                "calculation": f"({built_area} × {construction_price} × {age_factor} + 0.00 × {logradouro_area} × {construction_price}) × {location_factor} × {tax_rate}"
            }
        }
    
    def calculate_property_tax(self, property_id: int) -> Dict:
        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise ValueError(f"Property with ID {property_id} not found")
        
        built_area = self._safe_float(property_obj.built_area, 100.0)
        logradouro_area = self._safe_float(property_obj.land_area, 0.0)
        construction_price = self.get_construction_price()
        age_factor = self.get_age_factor(property_obj.age_factor_code, property_obj.purpose_id)
        location_factor = self.get_neighborhood_factor(property_obj.neighborhood_id)
        property_type = "commercial" if property_obj.purpose_id == 2 else "residential"
        
        result = self.calculate_ipra_tax(built_area, construction_price, age_factor, 
                                       logradouro_area, location_factor, property_type)
        
        result.update({
            "property_id": property_id,
            "property_name": property_obj.name,
            "property_ncontr": property_obj.ncontr
        })
        
        return result
    
    def get_neighborhood_factor(self, neighborhood_id: int) -> float:
        if not neighborhood_id:
            return 1.0
            
        try:
            neighborhood = Neighborhood.objects.get(cod_b1=neighborhood_id)
            return neighborhood.factor
        except Neighborhood.DoesNotExist:
            return 1.0
    
    def get_age_factor(self, factant_code: str, purpose_id: int) -> float:
        if not factant_code:
            return 1.0
            
        try:
            factor = AgeFactor.objects.get(code=factant_code)
            if purpose_id == 2:
                return factor.commercial_factor
            else:
                return factor.residential_factor
        except AgeFactor.DoesNotExist:
            return 1.0
    
    def get_construction_price(self, year: int = 2025) -> float:
        construction_prices = {
            2025: 9143.73, 2024: 9143.73, 2023: 9143.73, 2022: 9143.73, 2021: 9143.73,
            2020: 9143.73, 2019: 9143.73, 2018: 9143.73, 2017: 9143.73, 2016: 9143.73,
            2015: 9143.73, 2014: 7284.82, 2013: 6898.0, 2012: 6132.0, 2011: 5600.0
        }
        return construction_prices.get(year, 9143.73)
    
    def _safe_float(self, value, default=0.0):
        """Safely convert value to float, handling European decimal format"""
        if value is None or value == '':
            return default
        try:
            if isinstance(value, str):
                value = value.replace(',', '.')
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def calculate_bulk_taxes(self, limit: int = 100) -> list:
        properties = Property.objects.all()[:limit]
        results = []
        
        for prop in properties:
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
        total_properties = Property.objects.count()
        
        sample_taxes = self.calculate_bulk_taxes(1000)
        valid_taxes = [t for t in sample_taxes if "ipra_tax" in t]
        
        if valid_taxes:
            total_tax = sum(t["ipra_tax"] for t in valid_taxes)
            avg_tax = total_tax / len(valid_taxes)
            max_tax = max(t["ipra_tax"] for t in valid_taxes)
            min_tax = min(t["ipra_tax"] for t in valid_taxes)
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
