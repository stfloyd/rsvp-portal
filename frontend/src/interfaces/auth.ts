export interface User {
  id: number
  email: string
  firstName: string
  lastName: string
  groups: string[]
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface LoginResponse {
  token: string
  user: User
}
