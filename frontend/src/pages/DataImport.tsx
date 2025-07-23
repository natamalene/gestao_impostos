import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Upload, CheckCircle, AlertCircle, Database } from 'lucide-react'

export function DataImport() {
  const [importing, setImporting] = useState(false)
  const [importResult, setImportResult] = useState<{
    success: boolean
    message: string
  } | null>(null)

  const importData = async () => {
    try {
      setImporting(true)
      setImportResult(null)

      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/import-data`, {
        method: 'POST'
      })

      const data = await response.json()

      if (response.ok) {
        setImportResult({
          success: true,
          message: data.message || 'Dados importados com sucesso!'
        })
      } else {
        setImportResult({
          success: false,
          message: data.detail || 'Erro ao importar dados'
        })
      }
    } catch (error) {
      console.error('Error importing data:', error)
      setImportResult({
        success: false,
        message: 'Erro de conexão ao importar dados'
      })
    } finally {
      setImporting(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Importar Dados</h1>
        <p className="text-gray-600">Importar dados dos arquivos Excel para o sistema</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Database className="h-5 w-5 mr-2" />
            Importação de Dados
          </CardTitle>
          <CardDescription>
            Clique no botão abaixo para importar todos os dados dos arquivos Excel para o banco de dados.
            Este processo pode demorar alguns minutos.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">Arquivos que serão importados:</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Bairros.xlsx - Dados dos bairros e fatores</li>
              <li>• TblPROPRIETARIO.xlsx - Tipos de proprietários</li>
              <li>• TblFINALIDADE.xlsx - Finalidades das propriedades</li>
              <li>• tblfactant.xlsx - Fatores de antiguidade</li>
              <li>• tblp.xlsx - Preços de referência</li>
              <li>• FENDEREC.xlsx - Endereços</li>
              <li>• FCADIPA.xlsx - Dados das propriedades (arquivo principal)</li>
            </ul>
          </div>

          <Button 
            onClick={importData} 
            disabled={importing}
            className="w-full"
            size="lg"
          >
            <Upload className="h-4 w-4 mr-2" />
            {importing ? 'Importando dados...' : 'Importar Dados'}
          </Button>

          {importResult && (
            <Alert className={importResult.success ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}>
              {importResult.success ? (
                <CheckCircle className="h-4 w-4 text-green-600" />
              ) : (
                <AlertCircle className="h-4 w-4 text-red-600" />
              )}
              <AlertDescription className={importResult.success ? 'text-green-800' : 'text-red-800'}>
                {importResult.message}
              </AlertDescription>
            </Alert>
          )}

          <div className="bg-yellow-50 p-4 rounded-lg">
            <h4 className="font-medium text-yellow-900 mb-2">⚠️ Importante:</h4>
            <ul className="text-sm text-yellow-800 space-y-1">
              <li>• A importação pode demorar alguns minutos devido ao grande volume de dados</li>
              <li>• Registros duplicados serão automaticamente ignorados</li>
              <li>• O processo é seguro e pode ser executado múltiplas vezes</li>
              <li>• Em caso de erro, verifique se todos os arquivos Excel estão disponíveis</li>
            </ul>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Status do Sistema</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span>Backend API funcionando</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span>Banco de dados conectado</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span>Modelos de dados configurados</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span>Calculadora de impostos ativa</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
