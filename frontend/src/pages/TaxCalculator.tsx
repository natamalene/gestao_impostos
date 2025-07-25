import React, { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Calculator, Info } from 'lucide-react'

interface Neighborhood {
  id: number
  cod_b: number
  descricao: string
  fact: number
}

interface TaxResult {
  base_value: number
  neighborhood_factor: number
  age_factor: number
  tax_amount: number
  calculation: string
}

export function TaxCalculator() {
  const [neighborhoods, setNeighborhoods] = useState<Neighborhood[]>([])
  const [baseValue, setBaseValue] = useState('')
  const [selectedNeighborhood, setSelectedNeighborhood] = useState('')
  const [ageFactor, setAgeFactor] = useState('')
  const [propertyType, setPropertyType] = useState('1')
  const [result, setResult] = useState<TaxResult | null>(null)
  const [calculating, setCalculating] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchNeighborhoods = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/neighborhoods`)
        const data = await response.json()
        setNeighborhoods(data)
      } catch (error) {
        console.error('Error fetching neighborhoods:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchNeighborhoods()
  }, [])

  const calculateTax = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!baseValue || !selectedNeighborhood || !ageFactor) {
      alert('Por favor, preencha todos os campos obrigatórios')
      return
    }

    try {
      setCalculating(true)
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/calculate-tax`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          base_value: baseValue,
          neighborhood_code: selectedNeighborhood,
          age_factor_code: ageFactor,
          property_type: propertyType
        })
      })

      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error('Error calculating tax:', error)
      alert('Erro ao calcular imposto. Tente novamente.')
    } finally {
      setCalculating(false)
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
        <div className="text-lg">Carregando dados...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Calculadora de Imposto Predial (IPRA)</h1>
        <p className="text-gray-600">Calcule o IPRA usando a fórmula oficial: Vipra = Vp × taxa</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Parâmetros de Cálculo</CardTitle>
            <CardDescription>
              Insira os valores para calcular o IPRA usando a fórmula oficial
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={calculateTax} className="space-y-4">
              <div>
                <Label htmlFor="baseValue">Valor Base da Propriedade (MZN) *</Label>
                <Input
                  id="baseValue"
                  type="number"
                  step="0.01"
                  placeholder="Ex: 1000000"
                  value={baseValue}
                  onChange={(e) => setBaseValue(e.target.value)}
                  required
                />
              </div>

              <div>
                <Label htmlFor="neighborhood">Bairro *</Label>
                <Select value={selectedNeighborhood} onValueChange={setSelectedNeighborhood}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione um bairro" />
                  </SelectTrigger>
                  <SelectContent>
                    {neighborhoods.map((neighborhood) => (
                      <SelectItem key={neighborhood.id} value={neighborhood.cod_b.toString()}>
                        {neighborhood.descricao} (Fator: {neighborhood.fact})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="ageFactor">Código do Fator de Antiguidade *</Label>
                <Input
                  id="ageFactor"
                  type="text"
                  placeholder="Ex: A1, B2, C3"
                  value={ageFactor}
                  onChange={(e) => setAgeFactor(e.target.value)}
                  required
                />
                <p className="text-sm text-gray-500 mt-1">
                  Consulte a tabela de fatores de antiguidade
                </p>
              </div>

              <div>
                <Label htmlFor="propertyType">Tipo de Propriedade</Label>
                <Select value={propertyType} onValueChange={setPropertyType}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">Residencial</SelectItem>
                    <SelectItem value="2">Comercial</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button type="submit" className="w-full" disabled={calculating}>
                <Calculator className="h-4 w-4 mr-2" />
                {calculating ? 'Calculando...' : 'Calcular Imposto'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {result && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Info className="h-5 w-5 mr-2" />
                Resultado do Cálculo
              </CardTitle>
              <CardDescription>
                Fórmula IPRA: Vipra = Vp × taxa, onde Vp = (Ae × P × Fa + 0,00 × Al × P) × Fl
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 gap-4">
                <div>
                  <Label className="text-sm font-medium text-gray-500">Valor Base</Label>
                  <p className="text-lg">{formatCurrency(result.base_value)}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium text-gray-500">Fator do Bairro</Label>
                  <p className="text-lg">{result.neighborhood_factor}</p>
                </div>
                <div>
                  <Label className="text-sm font-medium text-gray-500">Fator de Antiguidade</Label>
                  <p className="text-lg">{result.age_factor}</p>
                </div>
                <div className="border-t pt-4">
                  <Label className="text-sm font-medium text-gray-500">Imposto Total</Label>
                  <p className="text-3xl font-bold text-blue-600">
                    {formatCurrency(result.tax_amount)}
                  </p>
                  <p className="text-sm text-gray-500 mt-2">
                    Cálculo: {result.calculation}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle>Informações sobre Fatores</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-medium">Fatores de Bairro</h4>
              <p className="text-sm text-gray-600">
                Cada bairro tem um fator específico que multiplica o valor base da propriedade.
                Bairros mais centrais geralmente têm fatores mais altos.
              </p>
            </div>
            <div>
              <h4 className="font-medium">Fatores de Antiguidade</h4>
              <p className="text-sm text-gray-600">
                O fator de antiguidade varia conforme a idade e tipo da propriedade.
                Propriedades mais antigas podem ter fatores diferentes.
              </p>
            </div>
            <div>
              <h4 className="font-medium">Taxas de Imposto</h4>
              <p className="text-sm text-gray-600">
                <strong>Residencial:</strong> 0,4% do valor patrimonial<br/>
                <strong>Comercial/Industrial:</strong> 0,7% do valor patrimonial
              </p>
            </div>
            <div>
              <h4 className="font-medium">Fórmula IPRA</h4>
              <p className="text-sm text-gray-600">
                <strong>Vipra = Vp × taxa</strong><br/>
                Onde <strong>Vp = (Ae × P × Fa + 0,00 × Al × P) × Fl</strong>
              </p>
            </div>
            <div>
              <h4 className="font-medium">Variáveis</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li><strong>Ae:</strong> Área edificada do prédio urbano</li>
                <li><strong>P:</strong> Preço médio de construção por m²</li>
                <li><strong>Fa:</strong> Fator de antiguidade do prédio</li>
                <li><strong>Al:</strong> Área do terreno (coeficiente 0,00)</li>
                <li><strong>Fl:</strong> Fator de localização do prédio</li>
              </ul>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
