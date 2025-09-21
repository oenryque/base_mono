// Exportações principais do pacote de contratos
export * from './common';
export * from './auth';
export * from './users';

// Re-exportações para facilitar o uso
export {
  // Common
  PaginationSchema,
  ErrorSchema,
  SuccessSchema,
  UserRole,
  UserStatus,
  API_VERSION,
  JWT_ACCESS_TOKEN_EXPIRES,
  JWT_REFRESH_TOKEN_EXPIRES,
  validateEmail,
  validatePassword,
  
  // Auth
  LoginRequestSchema,
  RegisterRequestSchema,
  ChangePasswordRequestSchema,
  RefreshTokenRequestSchema,
  TokenResponseSchema,
  UserResponseSchema,
  AuthUserResponseSchema,
  TokenValidationSchema,
  AuthHeaderSchema,
  
  // Users
  CreateUserRequestSchema,
  UpdateUserRequestSchema,
  UserQuerySchema,
  UserStatsSchema,
  UserListResponseSchema,
  UserDetailResponseSchema,
  ActivateUserRequestSchema,
  DeactivateUserRequestSchema,
  ResetPasswordRequestSchema,
} from './common';

export {
  LoginRequestSchema,
  RegisterRequestSchema,
  ChangePasswordRequestSchema,
  RefreshTokenRequestSchema,
  TokenResponseSchema,
  UserResponseSchema,
  AuthUserResponseSchema,
  TokenValidationSchema,
  AuthHeaderSchema,
} from './auth';

export {
  CreateUserRequestSchema,
  UpdateUserRequestSchema,
  UserQuerySchema,
  UserStatsSchema,
  UserListResponseSchema,
  UserDetailResponseSchema,
  ActivateUserRequestSchema,
  DeactivateUserRequestSchema,
  ResetPasswordRequestSchema,
} from './users';
