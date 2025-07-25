import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ArrowLeft, Calculator, Building, User, MapPin } from 'lucide-react'

interface Property {
  id: number
  codigo: number
  nome: string
  matriz: string
  valpatr: number
  cod_bairro: number
  bairro: string
  proprietar: number
  nuit: string
  cod_localizaca: string
  localizacao: string
  nu_entrada: string
  andar_n: string
  flat: string
  are_tereno: string
  are_constr: string
  factant: string
  finalidade_id: number
  data_cria: string
}

interface TaxResult {
  property_id: number
  property_name: string
  base_value: number
  neighborhood_factor: number
  age_factor: number
  tax_amount: number
  calculation_details: {
    formula: string
    calculation: string
  }
}

export function PropertyDetails() {
  const { id } = useParams<{ id: string }>()
  const [property, setProperty] = useState<Property | null>(null)
  const [taxResult, setTaxResult] = useState<TaxResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [calculatingTax, setCalculatingTax] = useState(false)

  useEffect(() => {
    const fetchProperty = async () => {
      if (!id) return

      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/properties/${id}`)
        const data = await response.json()
        setProperty(data)
      } catch (error) {
        console.error('Error fetching property:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchProperty()
  }, [id])

  const calculateTax = async () => {
    if (!id) return

    try {
      setCalculatingTax(true)
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/properties/${id}/tax`)
      const data = await response.json()
      setTaxResult(data)
    } catch (error) {
      console.error('Error calculating tax:', error)
    } finally {
      setCalculatingTax(false)
    }
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-MZ', {
      style: 'currency',
      currency: 'MZN'
    }).format(value)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Carregando detalhes da propriedade...</div>
      </div>
    )
  }

  if (!property) {
    return (
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900">Propriedade não encontrada</h2>
        <Link to="/properties">
          <Button className="mt-4">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Voltar às Propriedades
          </Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Link to="/properties">
            <Button variant="outline">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar
            </Button>
          </Link>
        </div>
        <Button onClick={calculateTax} disabled={calculatingTax}>
          <Calculator className="h-4 w-4 mr-2" />
          {calculatingTax ? 'Calculando...' : 'Calcular Imposto'}
        </Button>
      </div>

      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          {property.nome || `Propriedade ${property.codigo}`}
        </h1>
        <p className="text-gray-600">Detalhes da propriedade e cálculo de imposto</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Building className="h-5 w-5 mr-2" />
              Informações da Propriedade
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">CÓDIGO</label>
                <p className="text-lg">{property.codigo}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Matriz</label>
                <p className="text-lg">{property.matriz || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Valor Patrimonial</label>
                <p className="text-lg font-semibold text-green-600">
                  {property.valpatr ? formatCurrency(property.valpatr) : 'N/A'}
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Bairro</label>
                <p className="text-lg">{property.bairro || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Área de Logradouro</label>
                <p className="text-lg">{property.are_tereno || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Área de Construção</label>
                <p className="text-lg">{property.are_constr || 'N/A'}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <MapPin className="h-5 w-5 mr-2" />
              Localização
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Localização</label>
                <p className="text-lg">{property.localizacao || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Número de Entrada</label>
                <p className="text-lg">{property.nu_entrada || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Andar</label>
                <p className="text-lg">{property.andar_n || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Apartamento</label>
                <p className="text-lg">{property.flat || 'N/A'}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <User className="h-5 w-5 mr-2" />
              Proprietário
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Nome</label>
                <p className="text-lg">{property.nome || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">NUIT</label>
                <p className="text-lg">{property.nuit || 'N/A'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Tipo de Proprietário</label>
                <p className="text-lg">{property.proprietar || 'N/A'}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {taxResult && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Calculator className="h-5 w-5 mr-2" />
                Cálculo do Imposto
              </CardTitle>
              <CardDescription>
                {taxResult.calculation_details.formula}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Valor Base</label>
                  <p className="text-lg">{formatCurrency(taxResult.base_value)}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Fator do Bairro</label>
                  <p className="text-lg">{taxResult.neighborhood_factor}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Fator de Antiguidade</label>
                  <p className="text-lg">{taxResult.age_factor}</p>
                </div>
                <div className="border-t pt-4">
                  <label className="text-sm font-medium text-gray-500">Imposto Total</label>
                  <p className="text-2xl font-bold text-blue-600">
                    {formatCurrency(taxResult.tax_amount)}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                    {taxResult.calculation_details.calculation}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
