import { createClient } from '@/utils/supabase/server'
import { signOut } from './login/actions'
import Link from 'next/link'

export default async function Home() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <main className="flex flex-col items-center justify-center w-full flex-1 px-4 md:px-20 text-center">
        <h1 className="text-4xl md:text-6xl font-bold mb-8">
          Welcome to <span className="text-blue-600">AI Cover Letter</span>
        </h1>

        <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl">
          Generate tailored cover letters and optimize your CV for ATS systems in seconds.
        </p>

        {user ? (
          <div className="flex flex-col items-center gap-4">
            <p className="text-xl">
              Logged in as <code className="p-2 font-mono text-lg bg-gray-100 rounded-md dark:bg-gray-800">{user.email}</code>
            </p>
            <div className="flex gap-4">
                <Link href="/dashboard" className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition">
                    Go to Dashboard
                </Link>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-4">
            <div className="flex gap-4">
              <Link href="/login" className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition">
                Get Started
              </Link>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}