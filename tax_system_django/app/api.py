from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from properties.models import Property, Neighborhood, Address
from properties.services import TaxCalculator

def add_cors_headers(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response["Access-Control-Allow-Credentials"] = "true"
    return response

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def root(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(response)
    response = JsonResponse({"message": "Django Tax System API"})
    return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def get_statistics(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(response)
    try:
        calculator = TaxCalculator()
        stats = calculator.get_tax_statistics()
        response = JsonResponse(stats)
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({"error": str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def get_neighborhoods(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(response)
    try:
        neighborhoods = list(Neighborhood.objects.all()[:20])
        result = []
        for neighborhood in neighborhoods:
            result.append({
                "id": neighborhood.id,
                "cod_b": neighborhood.cod_b,
                "descricao": neighborhood.description,
                "fact": float(neighborhood.factor)
            })
        response = JsonResponse(result, safe=False)
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({"error": str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def get_properties(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(response)
    try:
        properties = list(Property.objects.select_related('neighborhood').all()[:100])
        result = []
        for prop in properties:
            result.append({
                "id": prop.id,
                "ncontr": prop.ncontr,
                "nome": prop.name or "",
                "bairro": prop.neighborhood.description if prop.neighborhood else "",
                "endereco": prop.address.street_name if prop.address else "",
                "valor_patrimonial": float(prop.patrimonial_value or 0)
            })
        response = JsonResponse({"properties": result, "total": len(result)})
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({"error": str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def get_property_details(request, property_id):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(response)
    try:
        prop = Property.objects.select_related('neighborhood').get(id=property_id)
        result = {
            "id": prop.id,
            "ncontr": prop.ncontr,
            "nome": prop.name or "",
            "bairro": prop.neighborhood.description if prop.neighborhood else "",
            "endereco": prop.address.street_name if prop.address else "",
            "valor_patrimonial": float(prop.patrimonial_value or 0),
            "area_construida": float(prop.built_area or 0),
            "area_terreno": float(prop.land_area or 0)
        }
        response = JsonResponse(result)
        return add_cors_headers(response)
    except Property.DoesNotExist:
        response = JsonResponse({"error": "Property not found"}, status=404)
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({"error": str(e)}, status=500)
        return add_cors_headers(response)
