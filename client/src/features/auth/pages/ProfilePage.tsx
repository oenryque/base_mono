import React from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuthStore } from '@/lib/auth'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/Card'
import { User, Mail, Shield, Calendar, Activity } from 'lucide-react'
import { formatDate } from '@/lib/utils'

const profileSchema = z.object({
  name: z.string().min(2, 'Nome deve ter pelo menos 2 caracteres'),
  email: z.string().email('Email inválido'),
})

const passwordSchema = z.object({
  currentPassword: z.string().min(1, 'Senha atual é obrigatória'),
  newPassword: z.string().min(8, 'Nova senha deve ter pelo menos 8 caracteres'),
  confirmPassword: z.string().min(1, 'Confirmação de senha é obrigatória'),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: 'Senhas não coincidem',
  path: ['confirmPassword'],
})

type ProfileFormData = z.infer<typeof profileSchema>
type PasswordFormData = z.infer<typeof passwordSchema>

export const ProfilePage: React.FC = () => {
  const { user, setUser } = useAuthStore()
  const [isEditing, setIsEditing] = React.useState(false)
  const [isChangingPassword, setIsChangingPassword] = React.useState(false)
  const [isLoading, setIsLoading] = React.useState(false)
  const [message, setMessage] = React.useState<{ type: 'success' | 'error'; text: string } | null>(null)

  const {
    register: registerProfile,
    handleSubmit: handleSubmitProfile,
    formState: { errors: profileErrors },
    reset: resetProfile,
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      name: user?.name || '',
      email: user?.email || '',
    },
  })

  const {
    register: registerPassword,
    handleSubmit: handleSubmitPassword,
    formState: { errors: passwordErrors },
    reset: resetPassword,
  } = useForm<PasswordFormData>({
    resolver: zodResolver(passwordSchema),
  })

  const onSubmitProfile = async (data: ProfileFormData) => {
    try {
      setIsLoading(true)
      setMessage(null)
      
      // Aqui você faria a chamada para a API para atualizar o perfil
      // await apiClient.updateProfile(data)
      
      // Simular atualização
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setUser({ ...user!, ...data })
      setIsEditing(false)
      setMessage({ type: 'success', text: 'Perfil atualizado com sucesso!' })
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro ao atualizar perfil' })
    } finally {
      setIsLoading(false)
    }
  }

  const onSubmitPassword = async (data: PasswordFormData) => {
    try {
      setIsLoading(true)
      setMessage(null)
      
      // Aqui você faria a chamada para a API para alterar a senha
      // await apiClient.changePassword(data)
      
      // Simular alteração
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setIsChangingPassword(false)
      resetPassword()
      setMessage({ type: 'success', text: 'Senha alterada com sucesso!' })
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro ao alterar senha' })
    } finally {
      setIsLoading(false)
    }
  }

  const handleCancelEdit = () => {
    resetProfile()
    setIsEditing(false)
  }

  const handleCancelPassword = () => {
    resetPassword()
    setIsChangingPassword(false)
  }

  if (!user) {
    return <div>Carregando...</div>
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Meu Perfil</h1>
        <p className="text-gray-600">Gerencie suas informações pessoais</p>
      </div>

      {/* Message */}
      {message && (
        <div className={`alert ${message.type === 'success' ? 'alert-success' : 'alert-error'}`}>
          <span>{message.text}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Info */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Informações Pessoais</CardTitle>
                  <CardDescription>
                    Atualize suas informações de perfil
                  </CardDescription>
                </div>
                {!isEditing && (
                  <Button
                    variant="outline"
                    onClick={() => setIsEditing(true)}
                  >
                    Editar
                  </Button>
                )}
              </div>
            </CardHeader>
            <CardContent>
              {isEditing ? (
                <form onSubmit={handleSubmitProfile(onSubmitProfile)} className="space-y-4">
                  <Input
                    {...registerProfile('name')}
                    label="Nome completo"
                    error={profileErrors.name?.message}
                    required
                  />
                  
                  <Input
                    {...registerProfile('email')}
                    type="email"
                    label="Email"
                    error={profileErrors.email?.message}
                    required
                  />
                  
                  <div className="flex space-x-2">
                    <Button
                      type="submit"
                      loading={isLoading}
                      disabled={isLoading}
                    >
                      Salvar
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={handleCancelEdit}
                    >
                      Cancelar
                    </Button>
                  </div>
                </form>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <User className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">Nome</p>
                      <p className="text-sm text-gray-600">{user.name}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <Mail className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">Email</p>
                      <p className="text-sm text-gray-600">{user.email}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <Shield className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">Função</p>
                      <p className="text-sm text-gray-600 capitalize">{user.role}</p>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Account Info */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Informações da Conta</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
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
                  <Activity className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Último login</p>
                    <p className="text-sm text-gray-600">
                      {formatDate(user.last_login)}
                    </p>
                  </div>
                </div>
              )}
              
              <div className="flex items-center space-x-3">
                <div className="h-5 w-5 flex items-center justify-center">
                  <div className={`h-2 w-2 rounded-full ${user.is_active ? 'bg-success-500' : 'bg-error-500'}`} />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900">Status</p>
                  <p className="text-sm text-gray-600 capitalize">
                    {user.is_active ? 'Ativo' : 'Inativo'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Change Password */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Alterar Senha</CardTitle>
                  <CardDescription>
                    Mantenha sua conta segura
                  </CardDescription>
                </div>
                {!isChangingPassword && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setIsChangingPassword(true)}
                  >
                    Alterar
                  </Button>
                )}
              </div>
            </CardHeader>
            {isChangingPassword && (
              <CardContent>
                <form onSubmit={handleSubmitPassword(onSubmitPassword)} className="space-y-4">
                  <Input
                    {...registerPassword('currentPassword')}
                    type="password"
                    label="Senha atual"
                    error={passwordErrors.currentPassword?.message}
                    required
                  />
                  
                  <Input
                    {...registerPassword('newPassword')}
                    type="password"
                    label="Nova senha"
                    error={passwordErrors.newPassword?.message}
                    required
                  />
                  
                  <Input
                    {...registerPassword('confirmPassword')}
                    type="password"
                    label="Confirmar nova senha"
                    error={passwordErrors.confirmPassword?.message}
                    required
                  />
                  
                  <div className="flex space-x-2">
                    <Button
                      type="submit"
                      size="sm"
                      loading={isLoading}
                      disabled={isLoading}
                    >
                      Salvar
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={handleCancelPassword}
                    >
                      Cancelar
                    </Button>
                  </div>
                </form>
              </CardContent>
            )}
          </Card>
        </div>
      </div>
    </div>
  )
}
