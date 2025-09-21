import { z } from 'zod';

// Tipos comuns compartilhados
export const PaginationSchema = z.object({
  page: z.number().int().positive().default(1),
  per_page: z.number().int().positive().max(100).default(10),
  total: z.number().int().nonnegative().optional(),
  pages: z.number().int().nonnegative().optional(),
});

export const ErrorSchema = z.object({
  error: z.string(),
  message: z.string(),
  details: z.record(z.any()).optional(),
});

export const SuccessSchema = z.object({
  success: z.boolean().default(true),
  message: z.string().optional(),
  data: z.any().optional(),
});

// Tipos TypeScript derivados dos schemas
export type Pagination = z.infer<typeof PaginationSchema>;
export type Error = z.infer<typeof ErrorSchema>;
export type Success = z.infer<typeof SuccessSchema>;

// Enums comuns
export enum UserRole {
  ADMIN = 'admin',
  DEVELOPER = 'developer',
  USER = 'user',
}

export enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  PENDING = 'pending',
  SUSPENDED = 'suspended',
}

// Constantes
export const API_VERSION = 'v1';
export const JWT_ACCESS_TOKEN_EXPIRES = 3600; // 1 hora
export const JWT_REFRESH_TOKEN_EXPIRES = 2592000; // 30 dias

// Utilitários de validação
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePassword = (password: string): boolean => {
  // Mínimo 8 caracteres, pelo menos 1 letra maiúscula, 1 minúscula, 1 número
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/;
  return passwordRegex.test(password);
};
