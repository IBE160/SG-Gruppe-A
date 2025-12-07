import { login, signup } from './actions'

export default function LoginPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <form className="flex flex-col gap-4 p-8 border rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Login / Signup</h1>
        <label htmlFor="email">Email:</label>
        <input id="email" name="email" type="email" required className="border p-2 rounded" />
        <label htmlFor="password">Password:</label>
        <input id="password" name="password" type="password" required className="border p-2 rounded" />
        <div className="flex gap-4 mt-4">
          <button formAction={login} className="bg-blue-500 text-white p-2 rounded flex-1 hover:bg-blue-600">Log in</button>
          <button formAction={signup} className="bg-green-500 text-white p-2 rounded flex-1 hover:bg-green-600">Sign up</button>
        </div>
      </form>
    </div>
  )
}
