'use client'

import { useActionState } from 'react'
import { login } from './actions'
import Link from 'next/link'

const initialState = {
  message: '',
  errors: {},
}

export function LoginForm() {
  const [state, formAction, isPending] = useActionState(login, initialState)

  return (
    <form action={formAction} className="flex flex-col gap-4 p-8 border rounded-lg shadow-md w-full max-w-md bg-white">
      <h1 className="text-2xl font-bold mb-4 text-center text-black">Login</h1>
      
      <div className="flex flex-col gap-1">
        <label htmlFor="email" className="text-black">Email</label>
        <input 
          id="email" 
          name="email" 
          type="email" 
          required 
          className="border p-2 rounded"
          disabled={isPending}
        />
        {state?.errors?.email && (
          <p className="text-red-500 text-xs">{state.errors.email[0]}</p>
        )}
      </div>
      
      <div className="flex flex-col gap-1">
        <label htmlFor="password" className="text-black">Password</label>
        <input 
          id="password" 
          name="password" 
          type="password" 
          required 
          className="border p-2 rounded"
          disabled={isPending}
        />
        {state?.errors?.password && (
          <p className="text-red-500 text-xs">{state.errors.password[0]}</p>
        )}
      </div>

      {state?.message && state.message !== 'Validation failed' && (
        <div aria-live="polite" className="text-red-500 text-sm text-center p-2 bg-red-50 rounded">
          {state.message}
        </div>
      )}

      <div className="flex flex-col gap-4 mt-4">
        <button 
          type="submit"
          disabled={isPending}
          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:opacity-50 transition-colors"
        >
          {isPending ? 'Logging in...' : 'Log in'}
        </button>
        
        <div className="text-center text-sm text-black">
          Don't have an account?{' '}
          <Link href="/register" className="text-blue-500 hover:underline">
            Sign up
          </Link>
        </div>
      </div>
    </form>
  )
}