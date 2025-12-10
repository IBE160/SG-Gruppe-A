import { createClient } from '@/utils/supabase/server'
import { redirect } from 'next/navigation'
import { CVUpload } from '@/components/cv/CVUpload'

export default async function Dashboard() {
  const supabase = await createClient()

  const {
    data: { user },
  } = await supabase.auth.getUser()

  if (!user) {
    return redirect('/login')
  }

  return (
    <div className="flex flex-col items-center min-h-screen py-10 bg-gray-50">
      <main className="w-full max-w-4xl px-4">
        <h1 className="text-3xl font-bold mb-8 text-gray-800">Dashboard</h1>
        <p className="mb-6 text-gray-600">Welcome, {user.email}</p>
        
        <div className="bg-white p-6 rounded-lg shadow-sm">
            <CVUpload />
        </div>
      </main>
    </div>
  )
}
