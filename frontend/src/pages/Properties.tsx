import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Search, Eye, Calculator } from 'lucide-react'

interface Property {
  id: number
  ncontr: number
  nome: string
  matriz: string
  valpatr: number
  cod_bairro: number
  proprietar: number
  nuit: string
}

interface PropertiesResponse {
  total: number
  skip: number
  limit: number
  properties: Property[]
}

export function Properties() {
  const [properties, setProperties] = useState<Property[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [currentPage, setCurrentPage] = useState(0)
  const [total, setTotal] = useState(0)
  const limit = 20

  const fetchProperties = async (searchQuery = '', skip = 0) => {
    try {
      setLoading(true)
      const url = new URL(`${import.meta.env.VITE_API_URL}/api/properties`)
      url.searchParams.set('limit', limit.toString())
      url.searchParams.set('skip', skip.toString())
      if (searchQuery) {
        url.searchParams.set('search', searchQuery)
      }

      const response = await fetch(url.toString())
      const data: PropertiesResponse = await response.json()
      
      setProperties(data.properties)
      setTotal(data.total)
    } catch (error) {
      console.error('Error fetching properties:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProperties()
  }, [])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setCurrentPage(0)
    fetchProperties(search, 0)
  }

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage)
    fetchProperties(search, newPage * limit)
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-MZ', {
      style: 'currency',
      currency: 'MZN'
    }).format(value)
  }

  const totalPages = Math.ceil(total / limit)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Propriedades</h1>
        <p className="text-gray-600">Gerir e visualizar propriedades registradas</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Pesquisar Propriedades</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="flex gap-4">
            <div className="flex-1">
              <Input
                type="text"
                placeholder="Pesquisar por nome, matriz ou NUIT..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <Button type="submit">
              <Search className="h-4 w-4 mr-2" />
              Pesquisar
            </Button>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>
            Lista de Propriedades ({total.toLocaleString()} total)
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex items-center justify-center h-32">
              <div className="text-lg">Carregando propriedades...</div>
            </div>
          ) : (
            <>
              <div className="overflow-x-auto">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-2">NCONTR</th>
                      <th className="text-left p-2">Nome</th>
                      <th className="text-left p-2">Matriz</th>
                      <th className="text-left p-2">Valor Patrimonial</th>
                      <th className="text-left p-2">Bairro</th>
                      <th className="text-left p-2">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {properties.map((property) => (
                      <tr key={property.id} className="border-b hover:bg-gray-50">
                        <td className="p-2">{property.ncontr}</td>
                        <td className="p-2">{property.nome || 'N/A'}</td>
                        <td className="p-2">{property.matriz || 'N/A'}</td>
                        <td className="p-2">
                          {property.valpatr ? formatCurrency(property.valpatr) : 'N/A'}
                        </td>
                        <td className="p-2">{property.cod_bairro || 'N/A'}</td>
                        <td className="p-2">
                          <div className="flex gap-2">
                            <Link to={`/properties/${property.id}`}>
                              <Button variant="outline" size="sm">
                                <Eye className="h-4 w-4" />
                              </Button>
                            </Link>
                            <Link to={`/properties/${property.id}`}>
                              <Button variant="outline" size="sm">
                                <Calculator className="h-4 w-4" />
                              </Button>
                            </Link>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {totalPages > 1 && (
                <div className="flex justify-center gap-2 mt-4">
                  <Button
                    variant="outline"
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={currentPage === 0}
                  >
                    Anterior
                  </Button>
                  <span className="flex items-center px-4">
                    Página {currentPage + 1} de {totalPages}
                  </span>
                  <Button
                    variant="outline"
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={currentPage >= totalPages - 1}
                  >
                    Próxima
                  </Button>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
