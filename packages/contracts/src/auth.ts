import { z } from 'zod';
import { UserRole, UserStatus } from './common';

// Schemas de autenticação para Devs/Admins
export const LoginRequestSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(6, 'Senha deve ter pelo menos 6 caracteres'),
});

export const RegisterRequestSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(8, 'Senha deve ter pelo menos 8 caracteres'),
  name: z.string().min(2, 'Nome deve ter pelo menos 2 caracteres'),
  role: z.nativeEnum(UserRole).default(UserRole.DEVELOPER),
});

export const ChangePasswordRequestSchema = z.object({
  current_password: z.string().min(1, 'Senha atual é obrigatória'),
  new_password: z.string().min(8, 'Nova senha deve ter pelo menos 8 caracteres'),
  confirm_password: z.string().min(8, 'Confirmação de senha é obrigatória'),
}).refine((data) => data.new_password === data.confirm_password, {
  message: 'Senhas não coincidem',
  path: ['confirm_password'],
});

export const RefreshTokenRequestSchema = z.object({
  refresh_token: z.string().min(1, 'Refresh token é obrigatório'),
});

// Schemas de resposta
export const TokenResponseSchema = z.object({
  access_token: z.string(),
  refresh_token: z.string(),
  token_type: z.literal('Bearer'),
  expires_in: z.number(),
});

export const UserResponseSchema = z.object({
  id: z.number(),
  email: z.string().email(),
  name: z.string(),
  role: z.nativeEnum(UserRole),
  status: z.nativeEnum(UserStatus),
  is_active: z.boolean(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export const AuthUserResponseSchema = UserResponseSchema.extend({
  last_login: z.string().datetime().optional(),
});

// Schemas de validação de token
export const TokenValidationSchema = z.object({
  user_id: z.number(),
  email: z.string().email(),
  role: z.nativeEnum(UserRole),
  exp: z.number(),
  iat: z.number(),
});

// Tipos TypeScript derivados dos schemas
export type LoginRequest = z.infer<typeof LoginRequestSchema>;
export type RegisterRequest = z.infer<typeof RegisterRequestSchema>;
export type ChangePasswordRequest = z.infer<typeof ChangePasswordRequestSchema>;
export type RefreshTokenRequest = z.infer<typeof RefreshTokenRequestSchema>;
export type TokenResponse = z.infer<typeof TokenResponseSchema>;
export type UserResponse = z.infer<typeof UserResponseSchema>;
export type AuthUserResponse = z.infer<typeof AuthUserResponseSchema>;
export type TokenValidation = z.infer<typeof TokenValidationSchema>;

// Schemas para validação de headers
export const AuthHeaderSchema = z.object({
  authorization: z.string().regex(/^Bearer\s+.+/, 'Formato de token inválido'),
});

export type AuthHeader = z.infer<typeof AuthHeaderSchema>;
