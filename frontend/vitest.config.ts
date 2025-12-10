import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./setupTests.ts'], // Add this line
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './'),
    },
  },
})
