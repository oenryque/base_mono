import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '@/lib/auth'

export interface ProtectedRouteProps {
  children: React.ReactNode
  requiredRole?: 'admin' | 'developer'
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  requiredRole 
}) => {
  const { isAuthenticated, user } = useAuthStore()
  const location = useLocation()

  // Se não estiver autenticado, redirecionar para login
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  // Se role específica for necessária
  if (requiredRole && user?.role !== requiredRole) {
    // Se for admin, pode acessar tudo
    if (user?.role === 'admin') {
      return <>{children}</>
    }
    
    // Se não tiver permissão, redirecionar para dashboard
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}
