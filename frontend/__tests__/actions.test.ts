import { expect, test, vi, describe, beforeEach } from 'vitest'
import { login } from '../app/login/actions'

const mockSignInWithPassword = vi.fn()
const mockSignOut = vi.fn()

vi.mock('@/utils/supabase/server', () => ({
  createClient: vi.fn(() => Promise.resolve({
    auth: {
      signInWithPassword: mockSignInWithPassword,
      signOut: mockSignOut,
    },
  })),
}))

vi.mock('next/navigation', () => ({
  redirect: vi.fn(),
}))

vi.mock('next/cache', () => ({
  revalidatePath: vi.fn(),
}))

describe('login action', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  test('validates invalid email', async () => {
    const formData = new FormData()
    formData.append('email', 'invalid')
    formData.append('password', '123')

    const result = await login(null, formData)
    expect(result).toEqual({
      message: 'Validation failed',
      errors: {
        email: ['Invalid email address'],
      }
    })
    expect(mockSignInWithPassword).not.toHaveBeenCalled()
  })

  test('calls supabase with valid credentials', async () => {
    mockSignInWithPassword.mockResolvedValue({ error: null })
    const formData = new FormData()
    formData.append('email', 'test@example.com')
    formData.append('password', 'password123')

    // Since success redirects, it might throw "NEXT_REDIRECT" error or just return undefined if mocked.
    // Our mock redirect does nothing, so the function finishes.
    await login(null, formData)
    
    expect(mockSignInWithPassword).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    })
  })

  test('returns error when supabase fails', async () => {
    mockSignInWithPassword.mockResolvedValue({ error: { message: 'Invalid login' } })
    const formData = new FormData()
    formData.append('email', 'test@example.com')
    formData.append('password', 'password123')

    const result = await login(null, formData)
    
    expect(result).toEqual({
      message: 'Invalid login',
    })
  })
})
