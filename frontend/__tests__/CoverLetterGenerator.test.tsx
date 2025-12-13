import { render, screen, waitFor } from '@testing-library/react'
import CoverLetterGenerator from '@/components/analysis/CoverLetterGenerator'
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

describe('CoverLetterGenerator Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetSession.mockResolvedValue({ 
        data: { session: { access_token: 'fake-token' } } 
    })
  })

  // Test ID: 3.1-UI-001
  // Priority: P1
  it('renders the initial state correctly', () => {
    render(<CoverLetterGenerator cvText="My CV" jdText="My JD" />)
    expect(screen.getByText('Cover Letter Assistant')).toBeDefined()
    expect(screen.getByText('Generate Cover Letter')).toBeDefined()
  })

  // Test ID: 3.1-UI-002
  // Priority: P2
  it('disables button if inputs are missing', () => {
    render(<CoverLetterGenerator cvText="" jdText="" />)
    const button = screen.getByRole('button', { name: /generate cover letter/i })
    expect(button).toBeDisabled()
  })

  // Test ID: 3.1-UI-003
  // Priority: P1
  it('calls API and displays result on success', async () => {
    // Return a promise that we can resolve later to test loading state
    let resolveMock: (value: any) => void = () => {}
    const mockPromise = new Promise((resolve) => {
        resolveMock = resolve
    })
    
    mockPost.mockReturnValue(mockPromise)
    const user = userEvent.setup()

    render(<CoverLetterGenerator cvText="CV Content" jdText="JD Content" />)

    const button = screen.getByRole('button', { name: /generate cover letter/i })
    await user.click(button)

    // Now loading should be visible
    expect(screen.getByText(/generating/i)).toBeDefined()
    expect(button).toBeDisabled()

    // Resolve the promise
    resolveMock({ 
        data: { cover_letter: 'Generated cover letter content' } 
    })

    await waitFor(() => {
        expect(mockPost).toHaveBeenCalledWith(
            expect.stringContaining('/api/v1/generation/cover-letter'),
            {
                cv_text: 'CV Content',
                job_description_text: 'JD Content'
            },
            expect.objectContaining({
                headers: { 'Authorization': 'Bearer fake-token' }
            })
        )
    })

    await waitFor(() => {
        const textarea = screen.getByRole('textbox') as HTMLTextAreaElement
        expect(textarea.value).toBe('Generated cover letter content')
    })
  })

  // Test ID: 3.1-UI-004
  // Priority: P1
  it('handles API errors gracefully', async () => {
    mockPost.mockRejectedValue({ 
        response: { data: { detail: 'Service unavailable' } } 
    })
    const user = userEvent.setup()

    render(<CoverLetterGenerator cvText="CV" jdText="JD" />)

    const button = screen.getByRole('button', { name: /generate cover letter/i })
    await user.click(button)

    await waitFor(() => {
        expect(screen.getByText('Service unavailable')).toBeDefined()
    })
    
    // Button should be enabled again
    expect(screen.getByRole('button', { name: /generate cover letter/i })).not.toBeDisabled()
  })
})
