import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from 'react-query'
import { apiClient } from '@/lib/apiClient'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/Card'
import { Button } from '@/components/Button'
import { 
  ArrowLeft, 
  Edit, 
  User, 
  Mail, 
  Shield, 
  Calendar, 
  Activity, 
  Clock,
  CheckCircle,
  XCircle
} from 'lucide-react'
import { formatDate, formatRelativeTime } from '@/lib/utils'

export const UserDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  // Buscar usuário
  const { data: userData, isLoading, error } = useQuery(
    ['user', id],
    () => apiClient.getUserById(Number(id)),
    {
      enabled: !!id,
    }
  )

  const user = userData?.data

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error || !user) {
    return (
      <div className="text-center py-8">
        <p className="text-error-600">Usuário não encontrado</p>
        <Button
          variant="outline"
          onClick={() => navigate('/users')}
          className="mt-4"
        >
          Voltar para usuários
        </Button>
      </div>
    )
  }

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'admin':
        return <Shield className="h-5 w-5 text-warning-600" />
      case 'developer':
        return <User className="h-5 w-5 text-primary-600" />
      default:
        return <User className="h-5 w-5 text-gray-600" />
    }
  }

  const getStatusInfo = (isActive: boolean, status: string) => {
    if (isActive) {
      return {
        icon: <CheckCircle className="h-5 w-5 text-success-600" />,
        text: 'Ativo',
        color: 'text-success-600',
        bgColor: 'bg-success-100',
      }
    }
    return {
      icon: <XCircle className="h-5 w-5 text-error-600" />,
      text: 'Inativo',
      color: 'text-error-600',
      bgColor: 'bg-error-100',
    }
  }

  const statusInfo = getStatusInfo(user.is_active, user.status)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            onClick={() => navigate('/users')}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Voltar
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{user.name}</h1>
            <p className="text-gray-600">Detalhes do usuário</p>
          </div>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline">
            <Edit className="h-4 w-4 mr-2" />
            Editar
          </Button>
          {user.is_active ? (
            <Button variant="error">
              <XCircle className="h-4 w-4 mr-2" />
              Desativar
            </Button>
          ) : (
            <Button variant="success">
              <CheckCircle className="h-4 w-4 mr-2" />
              Ativar
            </Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* User Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Basic Info */}
          <Card>
            <CardHeader>
              <CardTitle>Informações Básicas</CardTitle>
              <CardDescription>
                Dados pessoais do usuário
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-3">
                <Mail className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Email</p>
                  <p className="text-sm text-gray-600">{user.email}</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                {getRoleIcon(user.role)}
                <div>
                  <p className="text-sm font-medium text-gray-900">Função</p>
                  <p className="text-sm text-gray-600 capitalize">{user.role}</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                {statusInfo.icon}
                <div>
                  <p className="text-sm font-medium text-gray-900">Status</p>
                  <p className={`text-sm ${statusInfo.color}`}>{statusInfo.text}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Account Activity */}
          <Card>
            <CardHeader>
              <CardTitle>Atividade da Conta</CardTitle>
              <CardDescription>
                Histórico de atividades do usuário
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <Calendar className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Membro desde</p>
                    <p className="text-sm text-gray-600">
                      {formatDate(user.created_at)}
                    </p>
                  </div>
                </div>
                
                {user.last_login && (
                  <div className="flex items-center space-x-3">
                    <Clock className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">Último login</p>
                      <p className="text-sm text-gray-600">
                        {formatRelativeTime(user.last_login)}
                      </p>
                    </div>
                  </div>
                )}
                
                {user.login_count && (
                  <div className="flex items-center space-x-3">
                    <Activity className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">Total de logins</p>
                      <p className="text-sm text-gray-600">{user.login_count}</p>
                    </div>
                  </div>
                )}
                
                {user.last_ip && (
                  <div className="flex items-center space-x-3">
                    <Activity className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">Último IP</p>
                      <p className="text-sm text-gray-600 font-mono">{user.last_ip}</p>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Status Card */}
          <Card>
            <CardHeader>
              <CardTitle>Status da Conta</CardTitle>
            </CardHeader>
            <CardContent>
              <div className={`p-4 rounded-lg ${statusInfo.bgColor}`}>
                <div className="flex items-center space-x-2">
                  {statusInfo.icon}
                  <span className={`font-medium ${statusInfo.color}`}>
                    {statusInfo.text}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  {user.is_active 
                    ? 'Usuário pode acessar o sistema' 
                    : 'Usuário não pode acessar o sistema'
                  }
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Ações Rápidas</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full justify-start">
                <Edit className="h-4 w-4 mr-2" />
                Editar perfil
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Mail className="h-4 w-4 mr-2" />
                Enviar email
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Shield className="h-4 w-4 mr-2" />
                Alterar permissões
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Activity className="h-4 w-4 mr-2" />
                Ver atividades
              </Button>
            </CardContent>
          </Card>

          {/* Account Stats */}
          <Card>
            <CardHeader>
              <CardTitle>Estatísticas</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Dias ativo</span>
                  <span className="text-sm font-medium">
                    {Math.floor((new Date().getTime() - new Date(user.created_at).getTime()) / (1000 * 60 * 60 * 24))}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Logins totais</span>
                  <span className="text-sm font-medium">{user.login_count || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Última atualização</span>
                  <span className="text-sm font-medium">
                    {formatRelativeTime(user.updated_at)}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
