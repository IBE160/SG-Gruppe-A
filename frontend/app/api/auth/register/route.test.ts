import { POST } from './route';
import { createMocks } from 'node-mocks-http';
import pool from '@/lib/db';
import bcrypt from 'bcrypt';

// Mock dependencies
jest.mock('@/lib/db', () => ({
  query: jest.fn(),
}));

jest.mock('bcrypt', () => ({
  hash: jest.fn(),
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
    // Mock user exists
    (pool.query as jest.Mock).mockResolvedValueOnce({ rows: [{ id: 1 }] });

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
    expect(body.error).toBe('User already exists');
  });

  it('should create user and return 201 if valid', async () => {
    // Mock user does not exist
    (pool.query as jest.Mock).mockResolvedValueOnce({ rows: [] });
    
    // Mock hash
    (bcrypt.hash as jest.Mock).mockResolvedValue('hashed_password');

    // Mock insert success
    (pool.query as jest.Mock).mockResolvedValueOnce({ 
      rows: [{ id: 'uuid-123', email: 'test@example.com' }] 
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
    expect(pool.query).toHaveBeenCalledTimes(2); // Check and Insert
    expect(bcrypt.hash).toHaveBeenCalled();
  });
});
