import React, { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select'
import { Calculator, Info, TrendingUp } from 'lucide-react'

interface Neighborhood {
  id: number
  cod_b1: number
  descricao: string
  fact: number
}

interface AgeFactor {
  id: number
  cod: string
  id_range: string
  tiphab: number
  tipcom: number
}

interface SimulationResult {
  patrimonial_value: number
  tax_rate: number
  ipra_tax: number
  formula_details: {
    built_area: number
    construction_price: number
    age_factor: number
    logradouro_area: number
    location_factor: number
    calculation: string
  }
}

export function TaxSimulation() {
  const [neighborhoods, setNeighborhoods] = useState<Neighborhood[]>([])
  const [ageFactors, setAgeFactors] = useState<AgeFactor[]>([])
  const [loading, setLoading] = useState(true)
  const [simulating, setSimulating] = useState(false)
  const [result, setResult] = useState<SimulationResult | null>(null)

  const [formData, setFormData] = useState({
    built_area: '',
    construction_price: '',
    construction_year: '2025',
    age_factor_code: '',
    logradouro_area: '',
    neighborhood_code: '',
    property_type: 'residential'
  })

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [neighborhoodsRes, ageFactorsRes] = await Promise.all([
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/neighborhoods`),
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/age-factors`)
        ])

        const [neighborhoodsData, ageFactorsData] = await Promise.all([
          neighborhoodsRes.json(),
          ageFactorsRes.json()
        ])

        setNeighborhoods(neighborhoodsData)
        setAgeFactors(ageFactorsData)
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.built_area || !formData.neighborhood_code) {
      alert('Por favor, preencha pelo menos a área construída e o bairro')
      return
    }

    try {
      setSimulating(true)
      const response = await fetch(`${(import.meta as any).env.VITE_API_URL}/api/simulate-tax`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          built_area: parseFloat(formData.built_area),
          construction_price: formData.construction_price ? parseFloat(formData.construction_price) : null,
          construction_year: parseInt(formData.construction_year),
          age_factor_code: formData.age_factor_code || null,
          logradouro_area: formData.logradouro_area ? parseFloat(formData.logradouro_area) : 0.0,
          neighborhood_code: parseInt(formData.neighborhood_code),
          property_type: formData.property_type
        })
      })

      if (response.ok) {
        const data = await response.json()
        setResult(data)
      } else {
        const error = await response.json()
        alert(`Erro: ${error.detail}`)
      }
    } catch (error) {
      console.error('Error simulating tax:', error)
      alert('Erro ao simular imposto. Tente novamente.')
    } finally {
      setSimulating(false)
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
        <h1 className="text-3xl font-bold text-gray-900">Simulação de Imposto Predial</h1>
        <p className="text-gray-600">Simule o cálculo do IPRA com parâmetros personalizados</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Parâmetros da Simulação</CardTitle>
            <CardDescription>
              Insira os valores para simular o cálculo do IPRA usando a fórmula oficial
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="built_area">Área Edificada (m²) *</Label>
                <Input
                  id="built_area"
                  type="number"
                  step="0.01"
                  placeholder="Ex: 150"
                  value={formData.built_area}
                  onChange={(e) => handleInputChange('built_area', e.target.value)}
                  required
                />
                <p className="text-sm text-gray-500 mt-1">
                  Área total construída da propriedade
                </p>
              </div>

              <div>
                <Label htmlFor="construction_price">Preço de Construção por m² (MZN)</Label>
                <Input
                  id="construction_price"
                  type="number"
                  step="0.01"
                  placeholder="Ex: 9143.73 (deixe vazio para usar preço do ano)"
                  value={formData.construction_price}
                  onChange={(e) => handleInputChange('construction_price', e.target.value)}
                />
                <p className="text-sm text-gray-500 mt-1">
                  Preço médio de construção por metro quadrado
                </p>
              </div>

              <div>
                <Label htmlFor="construction_year">Ano de Construção</Label>
                <Select value={formData.construction_year} onValueChange={(value) => handleInputChange('construction_year', value)}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="2025">2025 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2024">2024 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2023">2023 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2022">2022 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2021">2021 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2020">2020 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2019">2019 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2018">2018 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2017">2017 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2016">2016 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2015">2015 (9.143,73 MZN/m²)</SelectItem>
                    <SelectItem value="2014">2014 (7.284,82 MZN/m²)</SelectItem>
                    <SelectItem value="2013">2013 (6.898,00 MZN/m²)</SelectItem>
                    <SelectItem value="2012">2012 (6.132,00 MZN/m²)</SelectItem>
                    <SelectItem value="2011">2011 (5.600,00 MZN/m²)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="logradouro_area">Área de Logradouro (m²)</Label>
                <Input
                  id="logradouro_area"
                  type="number"
                  step="0.01"
                  placeholder="Ex: 300"
                  value={formData.logradouro_area}
                  onChange={(e) => handleInputChange('logradouro_area', e.target.value)}
                />
                <p className="text-sm text-gray-500 mt-1">
                  Área do terreno que serve de logradouro ao prédio urbano
                </p>
              </div>

              <div>
                <Label htmlFor="neighborhood_code">Bairro *</Label>
                <Select value={formData.neighborhood_code} onValueChange={(value) => handleInputChange('neighborhood_code', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione um bairro" />
                  </SelectTrigger>
                  <SelectContent>
                    {neighborhoods.map((neighborhood) => (
                      <SelectItem key={neighborhood.id} value={neighborhood.cod_b1.toString()}>
                        {neighborhood.descricao} (Fator: {neighborhood.fact})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="age_factor_code">Fator de Antiguidade</Label>
                <Select value={formData.age_factor_code} onValueChange={(value) => handleInputChange('age_factor_code', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o fator de antiguidade" />
                  </SelectTrigger>
                  <SelectContent>
                    {ageFactors.map((factor) => (
                      <SelectItem key={factor.id} value={factor.cod}>
                        {factor.cod} - {factor.id_range}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="property_type">Tipo de Propriedade</Label>
                <Select value={formData.property_type} onValueChange={(value) => handleInputChange('property_type', value)}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="residential">Residencial (Taxa: 0,4%)</SelectItem>
                    <SelectItem value="commercial">Comercial/Industrial (Taxa: 0,7%)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button type="submit" className="w-full" disabled={simulating}>
                <Calculator className="h-4 w-4 mr-2" />
                {simulating ? 'Simulando...' : 'Simular IPRA'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {result && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="h-5 w-5 mr-2" />
                Resultado da Simulação
              </CardTitle>
              <CardDescription>
                Fórmula IPRA: Vipra = Vp × taxa, onde Vp = (Ae × P × Fa + 0,00 × Al × P) × Fl
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 gap-4">
                <div>
                  <Label className="text-sm font-medium text-gray-500">Valor Patrimonial (Vp)</Label>
                  <p className="text-lg font-semibold">{formatCurrency(result.patrimonial_value)}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Área Edificada</Label>
                    <p className="text-sm">{result.formula_details.built_area} m²</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Preço/m²</Label>
                    <p className="text-sm">{formatCurrency(result.formula_details.construction_price)}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Fator Antiguidade</Label>
                    <p className="text-sm">{result.formula_details.age_factor}</p>
                  </div>
                  <div>
                    <Label className="text-sm font-medium text-gray-500">Fator Localização</Label>
                    <p className="text-sm">{result.formula_details.location_factor}</p>
                  </div>
                </div>

                <div>
                  <Label className="text-sm font-medium text-gray-500">Taxa de Imposto</Label>
                  <p className="text-sm">{(result.tax_rate * 100).toFixed(1)}%</p>
                </div>

                <div className="border-t pt-4">
                  <Label className="text-sm font-medium text-gray-500">IPRA Total Anual</Label>
                  <p className="text-3xl font-bold text-blue-600">
                    {formatCurrency(result.ipra_tax)}
                  </p>
                  <p className="text-sm text-gray-500 mt-2">
                    Cálculo: {result.formula_details.calculation}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Info className="h-5 w-5 mr-2" />
              Sobre a Fórmula IPRA
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-medium">Fórmula Oficial</h4>
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
            <div>
              <h4 className="font-medium">Taxas de Imposto</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li><strong>Residencial:</strong> 0,4% do valor patrimonial</li>
                <li><strong>Comercial/Industrial:</strong> 0,7% do valor patrimonial</li>
              </ul>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
