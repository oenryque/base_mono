import React from 'react'
import { NavLink } from 'react-router-dom'
import { useAuthStore } from '@/lib/auth'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  Users,
  Settings,
  User,
  BarChart3,
  Shield,
  Code
} from 'lucide-react'

interface NavItem {
  name: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  roles?: ('admin' | 'developer')[]
}

const navigation: NavItem[] = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: 'Usuários',
    href: '/users',
    icon: Users,
    roles: ['admin', 'developer'],
  },
  {
    name: 'Estatísticas',
    href: '/stats',
    icon: BarChart3,
    roles: ['admin'],
  },
  {
    name: 'Configurações',
    href: '/settings',
    icon: Settings,
    roles: ['admin'],
  },
]

export const Sidebar: React.FC = () => {
  const { user } = useAuthStore()
  const [isCollapsed, setIsCollapsed] = React.useState(false)

  // Filtrar itens de navegação baseado no role do usuário
  const filteredNavigation = navigation.filter(item => {
    if (!item.roles) return true
    return item.roles.includes(user?.role as 'admin' | 'developer')
  })

  return (
    <div className={cn(
      'bg-white border-r border-gray-200 transition-all duration-300',
      isCollapsed ? 'w-16' : 'w-64'
    )}>
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          {!isCollapsed && (
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Code className="h-5 w-5 text-white" />
              </div>
              <span className="text-lg font-semibold text-gray-900">
                Monorepo
              </span>
            </div>
          )}
          
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1 rounded-md hover:bg-gray-100"
          >
            <div className="h-5 w-5 flex flex-col justify-center space-y-1">
              <div className="h-0.5 w-4 bg-gray-600 rounded"></div>
              <div className="h-0.5 w-4 bg-gray-600 rounded"></div>
              <div className="h-0.5 w-4 bg-gray-600 rounded"></div>
            </div>
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {filteredNavigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  'flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900',
                  isCollapsed && 'justify-center'
                )
              }
            >
              <item.icon className="h-5 w-5 flex-shrink-0" />
              {!isCollapsed && <span>{item.name}</span>}
            </NavLink>
          ))}
        </nav>

        {/* User info */}
        {!isCollapsed && user && (
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center space-x-3">
              <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
                <User className="h-4 w-4 text-primary-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user.name}
                </p>
                <p className="text-xs text-gray-500 capitalize">
                  {user.role}
                </p>
              </div>
              {user.role === 'admin' && (
                <Shield className="h-4 w-4 text-primary-600" />
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
