import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuthStore } from '@/lib/auth'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/Card'
import { Code, Mail, Lock, User, AlertCircle } from 'lucide-react'

const registerSchema = z.object({
  name: z.string().min(2, 'Nome deve ter pelo menos 2 caracteres'),
  email: z.string().email('Email inválido'),
  password: z.string().min(8, 'Senha deve ter pelo menos 8 caracteres'),
  confirmPassword: z.string(),
  role: z.enum(['admin', 'developer']).default('developer'),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Senhas não coincidem',
  path: ['confirmPassword'],
})

type RegisterFormData = z.infer<typeof registerSchema>

export const RegisterPage: React.FC = () => {
  const { register: registerUser, isLoading, error, clearError } = useAuthStore()
  const navigate = useNavigate()

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      role: 'developer',
    },
  })

  const password = watch('password')

  const onSubmit = async (data: RegisterFormData) => {
    try {
      clearError()
      await registerUser({
        name: data.name,
        email: data.email,
        password: data.password,
        role: data.role,
      })
      navigate('/dashboard', { replace: true })
    } catch (error) {
      // Erro já é tratado pelo store
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="mx-auto h-12 w-12 bg-primary-600 rounded-lg flex items-center justify-center">
            <Code className="h-8 w-8 text-white" />
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900">
            Criar nova conta
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Registre-se para acessar o sistema de desenvolvimento
          </p>
        </div>

        {/* Register Form */}
        <Card>
          <CardHeader>
            <CardTitle>Registro</CardTitle>
            <CardDescription>
              Preencha os dados para criar sua conta
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {/* Error message */}
              {error && (
                <div className="alert alert-error">
                  <AlertCircle className="h-4 w-4" />
                  <span>{error}</span>
                </div>
              )}

              {/* Name */}
              <Input
                {...register('name')}
                type="text"
                label="Nome completo"
                placeholder="Seu nome completo"
                leftIcon={<User className="h-4 w-4" />}
                error={errors.name?.message}
                required
              />

              {/* Email */}
              <Input
                {...register('email')}
                type="email"
                label="Email"
                placeholder="seu@email.com"
                leftIcon={<Mail className="h-4 w-4" />}
                error={errors.email?.message}
                required
              />

              {/* Password */}
              <Input
                {...register('password')}
                type="password"
                label="Senha"
                placeholder="Mínimo 8 caracteres"
                leftIcon={<Lock className="h-4 w-4" />}
                error={errors.password?.message}
                helperText="Deve conter pelo menos 8 caracteres, 1 maiúscula, 1 minúscula e 1 número"
                required
              />

              {/* Confirm Password */}
              <Input
                {...register('confirmPassword')}
                type="password"
                label="Confirmar senha"
                placeholder="Confirme sua senha"
                leftIcon={<Lock className="h-4 w-4" />}
                error={errors.confirmPassword?.message}
                required
              />

              {/* Role */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tipo de conta
                </label>
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      {...register('role')}
                      type="radio"
                      value="developer"
                      className="mr-2"
                    />
                    <span className="text-sm">Desenvolvedor</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      {...register('role')}
                      type="radio"
                      value="admin"
                      className="mr-2"
                    />
                    <span className="text-sm">Administrador</span>
                  </label>
                </div>
              </div>

              {/* Submit button */}
              <Button
                type="submit"
                className="w-full"
                loading={isLoading}
                disabled={isLoading}
              >
                Criar conta
              </Button>
            </form>

            {/* Login link */}
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Já tem uma conta?{' '}
                <Link
                  to="/login"
                  className="font-medium text-primary-600 hover:text-primary-500"
                >
                  Faça login aqui
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center">
          <p className="text-xs text-gray-500">
            Sistema de desenvolvimento - Monorepo Template
          </p>
        </div>
      </div>
    </div>
  )
}
