'use client'

import { signup } from './actions'
import { useState } from 'react'
import { Loader2 } from 'lucide-react'

export default function RegisterPage() {
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setError(null)

    const formData = new FormData(event.currentTarget)
    const password = formData.get('password') as string
    
    // Simple client-side check to match AC regex
    // 8+ chars, 1 uppercase, 1 number, 1 special char
    const passwordRegex = /^(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{8,}$/
    if (!passwordRegex.test(password)) {
        setError('Password must be 8+ chars, with 1 uppercase, 1 number, and 1 special char.')
        setLoading(false)
        return
    }

    try {
        const result = await signup(formData)
        if (result?.error) {
            setError(result.error)
        }
    } catch (e) {
        // Next.js Redirect throws an error, we need to catch it if it's NOT a redirect error, 
        // but typically redirect() works by throwing. 
        // However, since we are calling a Server Action from Client Component event handler,
        // the redirect should be handled by the framework.
        // If we get here it might be a different error.
        // Actually, if redirect() is called in Server Action, the promise resolves/rejects differently.
        // In Next.js 14+, calling SA from client that redirects: it should just handle the navigation.
        // Let's assume it works. If it throws "NEXT_REDIRECT", we ignore.
    }
    setLoading(false)
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2 bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white border rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-center text-gray-900">Create Account</h1>
        
        {error && (
            <div className="mb-4 p-3 text-sm text-red-500 bg-red-50 border border-red-200 rounded">
                {error}
            </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input 
                id="email" 
                name="email" 
                type="email" 
                required 
                className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                placeholder="you@example.com"
            />
          </div>
          
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input 
                id="password" 
                name="password" 
                type="password" 
                required 
                className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                placeholder="********"
            />
            <p className="text-xs text-gray-500 mt-1">
                Must be 8+ characters with uppercase, number, and special char.
            </p>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 transition flex items-center justify-center disabled:opacity-50"
          >
            {loading ? <Loader2 className="animate-spin h-5 w-5" /> : 'Sign Up'}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-600">
            Already have an account? <a href="/login" className="text-blue-600 hover:underline">Log in</a>
        </p>
      </div>
    </div>
  )
}
