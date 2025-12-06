import { Pool } from 'pg';

// Use a global variable to preserve the pool across hot reloads in development
let pool: Pool;

if (process.env.NODE_ENV === 'production') {
  pool = new Pool({
    connectionString: process.env.DATABASE_URL,
  });
} else {
  // @ts-ignore
  if (!global.pool) {
    // @ts-ignore
    global.pool = new Pool({
      connectionString: process.env.DATABASE_URL,
    });
  }
  // @ts-ignore
  pool = global.pool;
}

export default pool;
