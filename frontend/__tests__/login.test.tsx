import { expect, test, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { LoginForm } from '../app/login/login-form'

// Mock the server actions
vi.mock('../app/login/actions', () => ({
  login: vi.fn(),
}))

// Mock useActionState since it might not be fully supported in jsdom/react-testing-library setup for React 19 yet
// or effectively standard behavior.
// Actually, React 19 support in tooling is bleeding edge.
// If this fails, I'll just mock the hook.

test('LoginForm renders email and password fields', () => {
  render(<LoginForm />)
  expect(screen.getByLabelText(/email/i)).toBeDefined()
  expect(screen.getByLabelText(/password/i)).toBeDefined()
  expect(screen.getByRole('button', { name: /log in/i })).toBeDefined()
  expect(screen.getByText(/don't have an account/i)).toBeDefined()
})
