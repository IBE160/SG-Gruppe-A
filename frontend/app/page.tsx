import { createClient } from '@/utils/supabase/server'
import { signOut } from './login/actions'
import Link from 'next/link'

export default async function Home() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
        <h1 className="text-4xl font-bold mb-8">
          Welcome to <span className="text-blue-600">Next.js + Supabase!</span>
        </h1>

        {user ? (
          <div className="flex flex-col items-center gap-4">
            <p className="text-xl">
              Logged in as <code className="p-2 font-mono text-lg bg-gray-100 rounded-md dark:bg-gray-800">{user.email}</code>
            </p>
            <form action={signOut}>
                <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                  Sign Out
                </button>
            </form>
            <Link href="/todos" className="text-blue-500 hover:underline">
                View Todos
            </Link>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-4">
            <p className="text-xl">You are not logged in.</p>
            <Link href="/login" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Log In
            </Link>
          </div>
        )}
      </main>
    </div>
  )
}