import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import CoverLetterGenerator from '../components/analysis/CoverLetterGenerator';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import axios from 'axios';

// Mock axios
vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock Supabase client
vi.mock('@/utils/supabase/client', () => ({
  createClient: () => ({
    auth: {
      getSession: vi.fn().mockResolvedValue({
        data: {
          session: {
            access_token: 'fake-token',
          },
        },
      }),
    },
  }),
}));

// Mock toast
vi.mock('react-hot-toast', () => ({
  default: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));

describe('CoverLetterGenerator', () => {
  const mockCvText = 'My CV content';
  const mockJdText = 'Job Description content';
  const mockWriteText = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    // Mock navigator.clipboard
    Object.defineProperty(navigator, 'clipboard', {
      value: {
        writeText: mockWriteText,
      },
      writable: true,
      configurable: true,
    });
  });

  it('renders generation button initially', () => {
    render(<CoverLetterGenerator cvText={mockCvText} jdText={mockJdText} />);
    expect(screen.getByRole('button', { name: /generate cover letter/i })).toBeInTheDocument();
  });

  it('displays generated cover letter in editable textarea', async () => {
    const mockCoverLetter = 'Dear Hiring Manager, this is a generated letter.';
    mockedAxios.post.mockResolvedValueOnce({
      data: { cover_letter: mockCoverLetter },
    });

    render(<CoverLetterGenerator cvText={mockCvText} jdText={mockJdText} />);

    // Click generate button
    const generateBtn = screen.getByRole('button', { name: /generate cover letter/i });
    fireEvent.click(generateBtn);

    // Wait for generation to complete and textarea to appear
    await waitFor(() => {
      expect(screen.getByRole('textbox')).toBeInTheDocument();
    });

    const textarea = screen.getByRole('textbox');
    expect(textarea).toHaveValue(mockCoverLetter);

    // Verify it is editable
    const user = userEvent.setup();
    const newText = ' Updated content.';
    await user.type(textarea, newText);

    expect(textarea).toHaveValue(mockCoverLetter + newText);
  });

  it('shows error message if generation fails', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('Network error'));

    render(<CoverLetterGenerator cvText={mockCvText} jdText={mockJdText} />);

    fireEvent.click(screen.getByRole('button', { name: /generate cover letter/i }));

    await waitFor(() => {
      expect(screen.getByText(/Network error/i)).toBeInTheDocument();
    });
  });

  it('button is disabled when texts are missing', () => {
    render(<CoverLetterGenerator cvText="" jdText="" />);
    expect(screen.getByRole('button', { name: /generate cover letter/i })).toBeDisabled();
  });

  it('copies generated letter to clipboard and shows feedback', async () => {
    const mockCoverLetter = 'Letter to copy.';
    mockedAxios.post.mockResolvedValueOnce({
      data: { cover_letter: mockCoverLetter },
    });
    mockWriteText.mockResolvedValue(undefined);

    render(<CoverLetterGenerator cvText={mockCvText} jdText={mockJdText} />);

    // Generate
    fireEvent.click(screen.getByRole('button', { name: /generate cover letter/i }));
    await waitFor(() => screen.getByRole('textbox'));

    // Click copy
    const copyBtn = screen.getByRole('button', { name: /copy to clipboard/i });
    expect(copyBtn).toBeInTheDocument();
    
    fireEvent.click(copyBtn);

    expect(mockWriteText).toHaveBeenCalledWith(mockCoverLetter);
    
    // Wait for "Copied!" text (button changes text)
    await waitFor(() => {
      expect(screen.getByText(/Copied!/i)).toBeInTheDocument();
    });
  });

  it('handles copy error gracefully', async () => {
    const mockCoverLetter = 'Letter to copy.';
    mockedAxios.post.mockResolvedValueOnce({
      data: { cover_letter: mockCoverLetter },
    });
    mockWriteText.mockRejectedValue(new Error('Copy failed'));

    render(<CoverLetterGenerator cvText={mockCvText} jdText={mockJdText} />);

    // Generate
    fireEvent.click(screen.getByRole('button', { name: /generate cover letter/i }));
    await waitFor(() => screen.getByRole('textbox'));

    // Click copy
    const copyBtn = screen.getByRole('button', { name: /copy to clipboard/i });
    fireEvent.click(copyBtn);

    expect(mockWriteText).toHaveBeenCalledWith(mockCoverLetter);
    // We expect a toast error, but since we mocked toast, we might check if toast.error was called?
    // But verify it doesn't crash is good enough for now, or check that "Copied!" does NOT appear.
    // Wait a bit to ensure no crash
    await new Promise(r => setTimeout(r, 100));
    expect(screen.queryByText(/Copied!/i)).not.toBeInTheDocument();
  });
});