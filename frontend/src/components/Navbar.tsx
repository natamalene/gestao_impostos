import { Link, useLocation } from 'react-router-dom'
import { Home, Building, Calculator, Upload, BarChart3 } from 'lucide-react'

export function Navbar() {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/properties', label: 'Propriedades', icon: Building },
    { path: '/calculator', label: 'Calculadora', icon: Calculator },
    { path: '/register', label: 'Cadastrar', icon: Upload },
    { path: '/simulation', label: 'Simulação', icon: Calculator },
    { path: '/import', label: 'Importar Dados', icon: Upload },
  ]

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <BarChart3 className="h-8 w-8 text-blue-600" />
            <h1 className="text-xl font-bold text-gray-900">
              Sistema de Imposto Predial
            </h1>
          </div>
          
          <div className="flex space-x-4">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === path
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}
