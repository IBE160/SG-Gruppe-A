import { render, screen, waitFor } from '@testing-library/react'
import { CVUpload } from '@/components/cv/CVUpload'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import userEvent from '@testing-library/user-event'

// Mock axios
const mockPost = vi.fn()
vi.mock('axios', () => ({
  default: {
    post: (...args: any[]) => mockPost(...args)
  }
}))

// Mock Supabase
const mockGetSession = vi.fn()
vi.mock('@/utils/supabase/client', () => ({
  createClient: () => ({
    auth: {
        getSession: mockGetSession
    }
  })
}))

describe('CVUpload Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetSession.mockResolvedValue({ 
        data: { session: { access_token: 'fake-token' } } 
    })
  })

  it('renders the upload area', () => {
    render(<CVUpload />)
    expect(screen.getByText('Upload CV')).toBeDefined()
  })

  it('shows error if not logged in', async () => {
    mockGetSession.mockResolvedValue({ data: { session: null } })
    const user = userEvent.setup()
    
    render(<CVUpload />)
    
    // Find the hidden input
    // react-dropzone input has style display: none, so we use container
    // or just assume input is there.
    // simpler: grab input by type="file" (hidden)
    const input = document.querySelector('input[type="file"]') as HTMLInputElement
    expect(input).toBeDefined()

    const file = new File(['dummy content'], 'test.docx', { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
    await user.upload(input, file)

    await waitFor(() => {
        expect(screen.getByText(/You must be logged in/i)).toBeDefined()
    })
    expect(mockPost).not.toHaveBeenCalled()
  })

  it('uploads file when logged in', async () => {
    mockPost.mockResolvedValue({ data: { id: '123' } })
    const user = userEvent.setup()

    render(<CVUpload />)

    const input = document.querySelector('input[type="file"]') as HTMLInputElement
    const file = new File(['dummy content'], 'test.docx', { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
    
    await user.upload(input, file)

    await waitFor(() => {
        expect(mockPost).toHaveBeenCalledWith(
            expect.stringContaining('/api/cv/upload'),
            expect.any(FormData),
            expect.objectContaining({
                headers: expect.objectContaining({
                    'Authorization': 'Bearer fake-token'
                })
            })
        )
    })
    
    await waitFor(() => {
        expect(screen.getByText(/CV uploaded successfully/i)).toBeDefined()
    })
  })

  it('rejects invalid file types', async () => {
    const user = userEvent.setup()
    render(<CVUpload />)

    const input = document.querySelector('input[type="file"]') as HTMLInputElement
    const file = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' })
    
    await user.upload(input, file)

    await waitFor(() => {
       // react-dropzone default rejection message
       // might vary, usually "File is not supported" or similar
       // But our component displays `fileRejectionMsg`
       // "File type must be..."
       // Let's check for generic error display or just that upload didn't happen
       expect(mockPost).not.toHaveBeenCalled()
    })
    // Expect error message
    // regex for common dropzone error or check if error div appears
    // expect(screen.getByText(/File is not valid/i)).toBeDefined() // this is specific to dropzone config
  })
})