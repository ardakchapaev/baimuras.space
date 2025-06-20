
import { withAuth } from 'next-auth/middleware';

export default withAuth(
  function middleware(req) {
    // Additional middleware logic can be added here
  },
  {
    callbacks: {
      authorized: ({ token, req }) => {
        // Check if user is accessing admin routes
        if (req.nextUrl.pathname.startsWith('/admin')) {
          // Check if user has admin or manager role
          return token?.roles?.some((role: any) => 
            role.name === 'admin' || role.name === 'manager'
          ) ?? false;
        }
        return !!token;
      },
    },
  }
);

export const config = {
  matcher: ['/admin/:path*']
};
