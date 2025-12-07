import { POST } from './route';
import { createMocks } from 'node-mocks-http';
import { supabase } from '@/lib/supabaseClient';

// Mock Supabase client
jest.mock('@/lib/supabaseClient', () => ({
  supabase: {
    auth: {
      signUp: jest.fn(),
    },
  },
}));

describe('POST /api/auth/register', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should return 400 if validation fails', async () => {
    const { req } = createMocks({
      method: 'POST',
      json: async () => ({ email: 'invalid-email', password: '123' }),
    });

    const response = await POST(req);
    const body = await response.json();

    expect(response.status).toBe(400);
    expect(body.error).toBe('Validation error');
  });

  it('should return 400 if user already exists', async () => {
    // Mock Supabase signUp to return an error
    (supabase.auth.signUp as jest.Mock).mockResolvedValueOnce({ 
      error: { message: 'User already registered' } 
    });

    const { req } = createMocks({
      method: 'POST',
      json: async () => ({ 
        email: 'test@example.com', 
        password: 'Password123!' 
      }),
    });

    const response = await POST(req);
    const body = await response.json();

    expect(response.status).toBe(400);
    expect(body.error).toBe('User already registered');
  });

  it('should create user and return 201 if valid', async () => {
    // Mock Supabase signUp to succeed
    (supabase.auth.signUp as jest.Mock).mockResolvedValueOnce({
      data: { user: { id: 'uuid-123', email: 'test@example.com' } },
      error: null,
    });

    const { req } = createMocks({
      method: 'POST',
      json: async () => ({ 
        email: 'test@example.com', 
        password: 'Password123!' 
      }),
    });

    const response = await POST(req);
    const body = await response.json();

    expect(response.status).toBe(201);
    expect(body.message).toBe('User created successfully');
    expect(supabase.auth.signUp).toHaveBeenCalledTimes(1);
  });
});
