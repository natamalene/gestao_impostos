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
  codigo: number
  descricao: string
}

interface Purpose {
  id: number
  codigo: number
  descricao: string
}

interface Address {
  id: number
  cod_r: string
  morada: string
}

interface AgeFactor {
  id: number
  cod: string
  id_range: string
  tiphab: number
  tipcom: number
}

export function PropertyRegistration() {
  const [neighborhoods, setNeighborhoods] = useState<Neighborhood[]>([])
  const [ownerTypes, setOwnerTypes] = useState<OwnerType[]>([])
  const [purposes, setPurposes] = useState<Purpose[]>([])
  const [addresses, setAddresses] = useState<Address[]>([])
  const [ageFactors, setAgeFactors] = useState<AgeFactor[]>([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [success, setSuccess] = useState(false)

  const [formData, setFormData] = useState({
    nome: '',
    matriz: '',
    valpatr: '',
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
        const [neighborhoodsRes, ownerTypesRes, purposesRes, addressesRes, ageFactorsRes] = await Promise.all([
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/neighborhoods`),
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/owner-types`),
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/purposes`),
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/addresses`),
          fetch(`${(import.meta as any).env.VITE_API_URL}/api/age-factors`)
        ])

        const [neighborhoodsData, ownerTypesData, purposesData, addressesData, ageFactorsData] = await Promise.all([
          neighborhoodsRes.json(),
          ownerTypesRes.json(),
          purposesRes.json(),
          addressesRes.json(),
          ageFactorsRes.json()
        ])

        setNeighborhoods(neighborhoodsData)
        setOwnerTypes(ownerTypesData)
        setPurposes(purposesData)
        setAddresses(addressesData)
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
    
    if (!formData.nome || !formData.valpatr || !formData.cod_bairro) {
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
          valpatr: parseFloat(formData.valpatr),
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
        setSuccess(true)
        setFormData({
          nome: '',
          matriz: '',
          valpatr: '',
          cod_bairro: '',
          proprietar: '',
          nuit: '',
          endereco_cod: '',
          finalidade_id: '',
          are_tereno: '',
          are_constr: '',
          factant: ''
        })
        setTimeout(() => setSuccess(false), 3000)
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

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Cadastrar Nova Propriedade</h1>
        <p className="text-gray-600">Registre uma nova propriedade no sistema</p>
      </div>

      {success && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <div className="flex items-center">
            <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
            <p className="text-green-800">Propriedade cadastrada com sucesso!</p>
          </div>
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Dados da Propriedade</CardTitle>
          <CardDescription>
            Preencha as informações da propriedade. O CÓDIGO será gerado automaticamente pelo sistema. Campos marcados com * são obrigatórios.
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
                <Label htmlFor="valpatr">Valor Patrimonial (MZN) *</Label>
                <Input
                  id="valpatr"
                  type="number"
                  step="0.01"
                  placeholder="Ex: 1000000"
                  value={formData.valpatr}
                  onChange={(e) => handleInputChange('valpatr', e.target.value)}
                  required
                />
              </div>

              <div>
                <Label htmlFor="cod_bairro">Bairro *</Label>
                <Select value={formData.cod_bairro} onValueChange={(value) => handleInputChange('cod_bairro', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione um bairro" />
                  </SelectTrigger>
                  <SelectContent>
                    {neighborhoods.map((neighborhood) => (
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
                    {ownerTypes.map((type) => (
                      <SelectItem key={type.id} value={type.codigo.toString()}>
                        {type.descricao}
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
                    {addresses.map((address) => (
                      <SelectItem key={address.id} value={address.cod_r}>
                        {address.morada}
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
                    {purposes.map((purpose) => (
                      <SelectItem key={purpose.id} value={purpose.codigo.toString()}>
                        {purpose.descricao}
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
                    {ageFactors.map((factor) => (
                      <SelectItem key={factor.id} value={factor.cod}>
                        {factor.cod} - {factor.id_range}
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
