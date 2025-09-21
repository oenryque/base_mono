import React from 'react'
import { useAuthStore } from '@/lib/auth'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/Card'
import { 
  Users, 
  UserCheck, 
  UserX, 
  Shield, 
  Code, 
  Activity,
  TrendingUp,
  Clock
} from 'lucide-react'
import { formatDate } from '@/lib/utils'

// Mock data - em uma aplicação real, isso viria da API
const stats = {
  totalUsers: 24,
  activeUsers: 22,
  inactiveUsers: 2,
  adminUsers: 3,
  developerUsers: 21,
  usersCreatedToday: 2,
  usersCreatedThisWeek: 5,
  usersCreatedThisMonth: 12,
}

const recentActivity = [
  {
    id: 1,
    user: 'João Silva',
    action: 'Criou uma nova conta',
    time: '2 minutos atrás',
    type: 'user_created',
  },
  {
    id: 2,
    user: 'Maria Santos',
    action: 'Fez login no sistema',
    time: '15 minutos atrás',
    type: 'user_login',
  },
  {
    id: 3,
    user: 'Pedro Costa',
    action: 'Atualizou seu perfil',
    time: '1 hora atrás',
    type: 'profile_updated',
  },
  {
    id: 4,
    user: 'Ana Oliveira',
    action: 'Alterou sua senha',
    time: '2 horas atrás',
    type: 'password_changed',
  },
]

export const DashboardPage: React.FC = () => {
  const { user } = useAuthStore()

  const statCards = [
    {
      title: 'Total de Usuários',
      value: stats.totalUsers,
      icon: Users,
      color: 'primary' as const,
      change: { value: 12, type: 'increase' as const },
    },
    {
      title: 'Usuários Ativos',
      value: stats.activeUsers,
      icon: UserCheck,
      color: 'success' as const,
      change: { value: 8, type: 'increase' as const },
    },
    {
      title: 'Usuários Inativos',
      value: stats.inactiveUsers,
      icon: UserX,
      color: 'error' as const,
      change: { value: 2, type: 'decrease' as const },
    },
    {
      title: 'Administradores',
      value: stats.adminUsers,
      icon: Shield,
      color: 'warning' as const,
    },
    {
      title: 'Desenvolvedores',
      value: stats.developerUsers,
      icon: Code,
      color: 'primary' as const,
    },
    {
      title: 'Novos Hoje',
      value: stats.usersCreatedToday,
      icon: Activity,
      color: 'success' as const,
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Bem-vindo, {user?.name}!
        </h1>
        <p className="text-gray-600">
          Aqui está um resumo do que está acontecendo no sistema.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {statCards.map((stat, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  {stat.change && (
                    <div className="flex items-center mt-1">
                      <TrendingUp className={`h-4 w-4 mr-1 ${
                        stat.change.type === 'increase' ? 'text-success-500' : 'text-error-500'
                      }`} />
                      <span className={`text-sm ${
                        stat.change.type === 'increase' ? 'text-success-600' : 'text-error-600'
                      }`}>
                        {stat.change.value}% vs mês passado
                      </span>
                    </div>
                  )}
                </div>
                <div className={`p-3 rounded-lg bg-${stat.color}-100`}>
                  <stat.icon className={`h-6 w-6 text-${stat.color}-600`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>Atividade Recente</CardTitle>
            <CardDescription>
              Últimas ações realizadas no sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3">
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
                      <Activity className="h-4 w-4 text-primary-600" />
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">
                      {activity.user}
                    </p>
                    <p className="text-sm text-gray-600">
                      {activity.action}
                    </p>
                    <div className="flex items-center mt-1">
                      <Clock className="h-3 w-3 text-gray-400 mr-1" />
                      <span className="text-xs text-gray-500">
                        {activity.time}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <Card>
          <CardHeader>
            <CardTitle>Estatísticas Rápidas</CardTitle>
            <CardDescription>
              Resumo das métricas do sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Usuários criados esta semana</span>
                <span className="text-sm font-medium text-gray-900">
                  {stats.usersCreatedThisWeek}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Usuários criados este mês</span>
                <span className="text-sm font-medium text-gray-900">
                  {stats.usersCreatedThisMonth}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Taxa de usuários ativos</span>
                <span className="text-sm font-medium text-success-600">
                  {Math.round((stats.activeUsers / stats.totalUsers) * 100)}%
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Última atualização</span>
                <span className="text-sm font-medium text-gray-900">
                  {formatDate(new Date())}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* System Info */}
      <Card>
        <CardHeader>
          <CardTitle>Informações do Sistema</CardTitle>
          <CardDescription>
            Detalhes sobre o ambiente de desenvolvimento
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-primary-600">v1.0.0</p>
              <p className="text-sm text-gray-600">Versão</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-success-600">Online</p>
              <p className="text-sm text-gray-600">Status</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-warning-600">99.9%</p>
              <p className="text-sm text-gray-600">Uptime</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-primary-600">Dev</p>
              <p className="text-sm text-gray-600">Ambiente</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
