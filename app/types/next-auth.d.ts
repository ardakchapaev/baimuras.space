
import NextAuth from 'next-auth';

declare module 'next-auth' {
  interface Session {
    user: {
      id: string;
      email: string;
      name?: string;
      username: string;
      roles: Array<{
        id: string;
        name: string;
        description?: string;
      }>;
    };
  }

  interface User {
    id: string;
    email: string;
    name?: string;
    username: string;
    roles: Array<{
      id: string;
      name: string;
      description?: string;
    }>;
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    username: string;
    roles: Array<{
      id: string;
      name: string;
      description?: string;
    }>;
  }
}
