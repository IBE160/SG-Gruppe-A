import React from 'react';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import JobDescriptionInput from '../components/job/JobDescriptionInput';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import { vi } from 'vitest';
import toast from 'react-hot-toast';

// Mock axios post request
vi.mock('axios');
const mockedAxios = axios as {
  post: ReturnType<typeof vi.fn>;
};

// Mock useRouter
vi.mock('next/navigation', () => ({
  useRouter: vi.fn(),
}));

// Mock react-hot-toast
vi.mock('react-hot-toast', () => ({
  default: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));

describe('JobDescriptionInput', () => {
  const mockRouter = {
    refresh: vi.fn(),
  };

  beforeEach(() => {
    mockedAxios.post.mockClear();
    (useRouter as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockRouter);
    // No need to spy on window.alert anymore
  });

  afterEach(() => {
    vi.restoreAllMocks(); // Restore all mocks after each test
    cleanup();
  });

  it('renders the job description input form', () => {
    render(<JobDescriptionInput />);
    expect(screen.getByRole('heading', { name: /paste job description/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/job description/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /save job description/i })).toBeInTheDocument();
  });

  it('shows validation error for empty input', async () => {
    render(<JobDescriptionInput />);
    const saveButton = screen.getByRole('button', { name: /save job description/i });
    await userEvent.click(saveButton);

    expect(await screen.findByText(/job description must be at least 5 characters/i)).toBeInTheDocument();
    expect(mockedAxios.post).not.toHaveBeenCalled();
  });

  it('shows validation error for short input', async () => {
    render(<JobDescriptionInput />);
    const textArea = screen.getByLabelText(/job description/i);
    await userEvent.type(textArea, 'abc');
    const saveButton = screen.getByRole('button', { name: /save job description/i });
    await userEvent.click(saveButton);

    expect(await screen.findByText(/job description must be at least 5 characters/i)).toBeInTheDocument();
    expect(mockedAxios.post).not.toHaveBeenCalled();
  });

  it('submits valid job description and clears form', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { id: 'test-id', title: 'Test Job Description' } });
    
    render(<JobDescriptionInput />);
    const textArea = screen.getByLabelText(/job description/i);
    await userEvent.type(textArea, 'This is a valid job description with enough characters.');
    const saveButton = screen.getByRole('button', { name: /save job description/i });
    await userEvent.click(saveButton);

    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalledTimes(1);
      expect(mockedAxios.post).toHaveBeenCalledWith('/api/job-description', {
        content: 'This is a valid job description with enough characters.',
      });
      expect(toast.success).toHaveBeenCalledWith('Job description saved successfully!');
      expect(textArea).toHaveValue(''); // Check if form is cleared
      expect(mockRouter.refresh).toHaveBeenCalledTimes(1); // Check if router.refresh was called
    });
  });

  it('handles API submission error', async () => {
    mockedAxios.post.mockRejectedValueOnce({ response: { data: { detail: 'Network error' } } });
    
    render(<JobDescriptionInput />);
    const textArea = screen.getByLabelText(/job description/i);
    await userEvent.type(textArea, 'This is a valid job description to trigger an error.');
    const saveButton = screen.getByRole('button', { name: /save job description/i });
    await userEvent.click(saveButton);

    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalledTimes(1);
      expect(toast.error).toHaveBeenCalledWith('Failed to save job description: Network error');
    });
  });
});
