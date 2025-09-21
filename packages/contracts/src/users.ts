import { z } from 'zod';
import { UserRole, UserStatus, PaginationSchema } from './common';

// Schemas para CRUD de usuários (Devs/Admins)
export const CreateUserRequestSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(8, 'Senha deve ter pelo menos 8 caracteres'),
  name: z.string().min(2, 'Nome deve ter pelo menos 2 caracteres'),
  role: z.nativeEnum(UserRole).default(UserRole.DEVELOPER),
  status: z.nativeEnum(UserStatus).default(UserStatus.ACTIVE),
});

export const UpdateUserRequestSchema = z.object({
  email: z.string().email('Email inválido').optional(),
  name: z.string().min(2, 'Nome deve ter pelo menos 2 caracteres').optional(),
  role: z.nativeEnum(UserRole).optional(),
  status: z.nativeEnum(UserStatus).optional(),
});

export const UserQuerySchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  per_page: z.coerce.number().int().positive().max(100).default(10),
  search: z.string().optional(),
  role: z.nativeEnum(UserRole).optional(),
  status: z.nativeEnum(UserStatus).optional(),
  sort_by: z.enum(['id', 'name', 'email', 'created_at', 'updated_at']).default('created_at'),
  sort_order: z.enum(['asc', 'desc']).default('desc'),
});

export const UserStatsSchema = z.object({
  total_users: z.number(),
  active_users: z.number(),
  inactive_users: z.number(),
  pending_users: z.number(),
  suspended_users: z.number(),
  admin_users: z.number(),
  developer_users: z.number(),
  user_users: z.number(),
  users_created_today: z.number(),
  users_created_this_week: z.number(),
  users_created_this_month: z.number(),
});

export const UserListResponseSchema = z.object({
  users: z.array(z.object({
    id: z.number(),
    email: z.string().email(),
    name: z.string(),
    role: z.nativeEnum(UserRole),
    status: z.nativeEnum(UserStatus),
    is_active: z.boolean(),
    created_at: z.string().datetime(),
    updated_at: z.string().datetime(),
    last_login: z.string().datetime().optional(),
  })),
  pagination: PaginationSchema,
});

export const UserDetailResponseSchema = z.object({
  id: z.number(),
  email: z.string().email(),
  name: z.string(),
  role: z.nativeEnum(UserRole),
  status: z.nativeEnum(UserStatus),
  is_active: z.boolean(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
  last_login: z.string().datetime().optional(),
  login_count: z.number().optional(),
  last_ip: z.string().optional(),
});

// Schemas para ações específicas
export const ActivateUserRequestSchema = z.object({
  user_id: z.number().int().positive(),
});

export const DeactivateUserRequestSchema = z.object({
  user_id: z.number().int().positive(),
});

export const ResetPasswordRequestSchema = z.object({
  user_id: z.number().int().positive(),
  new_password: z.string().min(8, 'Nova senha deve ter pelo menos 8 caracteres'),
});

// Tipos TypeScript derivados dos schemas
export type CreateUserRequest = z.infer<typeof CreateUserRequestSchema>;
export type UpdateUserRequest = z.infer<typeof UpdateUserRequestSchema>;
export type UserQuery = z.infer<typeof UserQuerySchema>;
export type UserStats = z.infer<typeof UserStatsSchema>;
export type UserListResponse = z.infer<typeof UserListResponseSchema>;
export type UserDetailResponse = z.infer<typeof UserDetailResponseSchema>;
export type ActivateUserRequest = z.infer<typeof ActivateUserRequestSchema>;
export type DeactivateUserRequest = z.infer<typeof DeactivateUserRequestSchema>;
export type ResetPasswordRequest = z.infer<typeof ResetPasswordRequestSchema>;
