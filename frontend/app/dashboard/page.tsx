import { createClient } from '@/utils/supabase/server'
import { redirect } from 'next/navigation'
import Link from 'next/link'
import { CVUpload } from '@/components/cv/CVUpload'
import JobDescriptionInput from '@/components/job/JobDescriptionInput'

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
      <main className="w-full max-w-6xl px-4 md:px-8">
        <h1 className="text-3xl font-bold mb-8 text-gray-800">Dashboard</h1>
        <p className="mb-6 text-gray-600">Welcome, {user.email}</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div className="bg-white p-6 rounded-lg shadow-sm h-full">
                <h2 className="text-xl font-semibold mb-4">1. Upload CV</h2>
                <CVUpload />
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm h-full">
                <h2 className="text-xl font-semibold mb-4">2. Add Job Description</h2>
                <JobDescriptionInput />
            </div>
        </div>
        
        <div className="text-center mt-8">
            <Link 
              href="/analysis"
              className="inline-block bg-blue-600 text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-blue-700 transition shadow-md w-full md:w-auto"
            >
              Generate Cover Letter & Analyze Gap &rarr;
            </Link>
        </div>
      </main>
    </div>
  )
}
