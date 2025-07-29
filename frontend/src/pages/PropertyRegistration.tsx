import React, { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select'
import { PlusCircle, CheckCircle } from 'lucide-react'

interface Neighborhood {
  id: number
  cod_b1: number
  descricao: string
  fact: number
}

interface OwnerType {
  id: number
  code: number
  description: string
}

interface Purpose {
  id: number
  code: number
  description: string
}

interface Address {
  id: number
  cod_r: number
  street_name: string
}

interface AgeFactor {
  id: number
  code: string
  id_range: string
  residential_factor: number
  commercial_factor: number
}

export function PropertyRegistration() {
  const [neighborhoods, setNeighborhoods] = useState<Neighborhood[]>([])
  const [ownerTypes, setOwnerTypes] = useState<OwnerType[]>([])
  const [purposes, setPurposes] = useState<Purpose[]>([])
  const [addresses, setAddresses] = useState<Address[]>([])
  const [ageFactors, setAgeFactors] = useState<AgeFactor[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [success, setSuccess] = useState(false)
  const [createdProperty, setCreatedProperty] = useState<{codigo: number, valor_patrimonial: number} | null>(null)

  const [formData, setFormData] = useState({
    nome: '',
    matriz: '',
    cod_bairro: '',
    proprietar: '',
    nuit: '',
    endereco_cod: '',
    finalidade_id: '',
    are_tereno: '',
    are_constr: '',
    factant: ''
  })

  useEffect(() => {
    const fetchData = async () => {
      try {
        setError(null)
        const [neighborhoodsRes, ownerTypesRes, purposesRes, addressesRes, ageFactorsRes] = await Promise.all([
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/neighborhoods/`),
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/owner-types/`),
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/purposes/`),
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/addresses/`),
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/age-factors/`)
        ])

        if (!neighborhoodsRes.ok || !ownerTypesRes.ok || !purposesRes.ok || !addressesRes.ok || !ageFactorsRes.ok) {
          throw new Error('Failed to fetch data from API')
        }

        const [neighborhoodsData, ownerTypesData, purposesData, addressesData, ageFactorsData] = await Promise.all([
          neighborhoodsRes.json(),
          ownerTypesRes.json(),
          purposesRes.json(),
          addressesRes.json(),
          ageFactorsRes.json()
        ])

        setNeighborhoods(Array.isArray(neighborhoodsData) ? neighborhoodsData : [])
        setOwnerTypes(Array.isArray(ownerTypesData) ? ownerTypesData : [])
        setPurposes(Array.isArray(purposesData) ? purposesData : [])
        setAddresses(Array.isArray(addressesData) ? addressesData : [])
        setAgeFactors(Array.isArray(ageFactorsData) ? ageFactorsData : [])
      } catch (error) {
        console.error('Error fetching data:', error)
        setError('Erro ao carregar dados. Tente novamente.')
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
    
    if (!formData.nome || !formData.cod_bairro) {
      alert('Por favor, preencha todos os campos obrigatórios')
      return
    }

    try {
      setSubmitting(true)
      const response = await fetch(`${(import.meta as any).env.VITE_API_URL}/api/properties`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nome: formData.nome,
          matriz: formData.matriz || null,
          cod_bairro: parseInt(formData.cod_bairro),
          proprietar: formData.proprietar ? parseInt(formData.proprietar) : null,
          nuit: formData.nuit || null,
          endereco_cod: formData.endereco_cod || null,
          finalidade_id: formData.finalidade_id ? parseInt(formData.finalidade_id) : null,
          are_tereno: formData.are_tereno || null,
          are_constr: formData.are_constr || null,
          factant: formData.factant || null
        })
      })

      if (response.ok) {
        const result = await response.json()
        setSuccess(true)
        setCreatedProperty({
          codigo: result.codigo,
          valor_patrimonial: result.valor_patrimonial
        })
        setFormData({
          nome: '',
          matriz: '',
          cod_bairro: '',
          proprietar: '',
          nuit: '',
          endereco_cod: '',
          finalidade_id: '',
          are_tereno: '',
          are_constr: '',
          factant: ''
        })
        setTimeout(() => {
          setSuccess(false)
          setCreatedProperty(null)
        }, 5000)
      } else {
        const error = await response.json()
        alert(`Erro: ${error.detail}`)
      }
    } catch (error) {
      console.error('Error creating property:', error)
      alert('Erro ao cadastrar propriedade. Tente novamente.')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Carregando dados...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg text-red-600">{error}</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Cadastrar Nova Propriedade</h1>
        <p className="text-gray-600">Registre uma nova propriedade no sistema</p>
      </div>

      {success && createdProperty && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <div className="flex items-center mb-2">
            <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
            <p className="text-green-800 font-semibold">Propriedade cadastrada com sucesso!</p>
          </div>
          <div className="ml-7 space-y-1">
            <p className="text-green-700">
              <strong>CÓDIGO atribuído:</strong> {createdProperty.codigo}
            </p>
            <p className="text-green-700">
              <strong>Valor Patrimonial calculado:</strong> {new Intl.NumberFormat('pt-MZ', {
                style: 'currency',
                currency: 'MZN'
              }).format(createdProperty.valor_patrimonial)}
            </p>
          </div>
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Dados da Propriedade</CardTitle>
          <CardDescription>
            Preencha as informações da propriedade. O CÓDIGO e Valor Patrimonial serão calculados automaticamente pelo sistema usando a fórmula IPRA. Campos marcados com * são obrigatórios.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="nome">Nome do Proprietário *</Label>
                <Input
                  id="nome"
                  type="text"
                  placeholder="Nome completo"
                  value={formData.nome}
                  onChange={(e) => handleInputChange('nome', e.target.value)}
                  required
                />
              </div>

              <div>
                <Label htmlFor="matriz">Matriz</Label>
                <Input
                  id="matriz"
                  type="text"
                  placeholder="Código da matriz"
                  value={formData.matriz}
                  onChange={(e) => handleInputChange('matriz', e.target.value)}
                />
              </div>

              <div>
                <Label htmlFor="cod_bairro">Bairro *</Label>
                <Select value={formData.cod_bairro} onValueChange={(value) => handleInputChange('cod_bairro', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione um bairro" />
                  </SelectTrigger>
                  <SelectContent>
                    {neighborhoods.filter(neighborhood => neighborhood && neighborhood.cod_b1 && neighborhood.descricao).map((neighborhood) => (
                      <SelectItem key={neighborhood.id} value={neighborhood.cod_b1.toString()}>
                        {neighborhood.descricao}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="proprietar">Tipo de Proprietário</Label>
                <Select value={formData.proprietar} onValueChange={(value) => handleInputChange('proprietar', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    {ownerTypes.filter(type => type && type.code && type.description).map((type) => (
                      <SelectItem key={type.id} value={type.code.toString()}>
                        {type.description}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="nuit">NUIT</Label>
                <Input
                  id="nuit"
                  type="text"
                  placeholder="Número de identificação fiscal"
                  value={formData.nuit}
                  onChange={(e) => handleInputChange('nuit', e.target.value)}
                />
              </div>

              <div>
                <Label htmlFor="endereco_cod">Endereço</Label>
                <Select value={formData.endereco_cod} onValueChange={(value) => handleInputChange('endereco_cod', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o endereço" />
                  </SelectTrigger>
                  <SelectContent>
                    {addresses.filter(address => address && address.cod_r && address.street_name).map((address) => (
                      <SelectItem key={address.id} value={address.cod_r.toString()}>
                        {address.street_name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="finalidade_id">Finalidade</Label>
                <Select value={formData.finalidade_id} onValueChange={(value) => handleInputChange('finalidade_id', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione a finalidade" />
                  </SelectTrigger>
                  <SelectContent>
                    {purposes.filter(purpose => purpose && purpose.code && purpose.description).map((purpose) => (
                      <SelectItem key={purpose.id} value={purpose.code.toString()}>
                        {purpose.description}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="are_tereno">Área de Logradouro (m²)</Label>
                <Input
                  id="are_tereno"
                  type="text"
                  placeholder="Ex: 500"
                  value={formData.are_tereno}
                  onChange={(e) => handleInputChange('are_tereno', e.target.value)}
                />
                <p className="text-sm text-gray-500 mt-1">Área do terreno que serve de logradouro ao prédio urbano</p>
              </div>

              <div>
                <Label htmlFor="are_constr">Área Construída (m²)</Label>
                <Input
                  id="are_constr"
                  type="text"
                  placeholder="Ex: 200"
                  value={formData.are_constr}
                  onChange={(e) => handleInputChange('are_constr', e.target.value)}
                />
              </div>

              <div>
                <Label htmlFor="factant">Fator de Antiguidade</Label>
                <Select value={formData.factant} onValueChange={(value) => handleInputChange('factant', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o fator de antiguidade" />
                  </SelectTrigger>
                  <SelectContent>
                    {ageFactors.filter(factor => factor && factor.code && factor.id_range).map((factor) => (
                      <SelectItem key={factor.id} value={factor.code}>
                        {factor.code} - {factor.id_range}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <Button type="submit" className="w-full" disabled={submitting}>
              <PlusCircle className="h-4 w-4 mr-2" />
              {submitting ? 'Cadastrando...' : 'Cadastrar Propriedade'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
