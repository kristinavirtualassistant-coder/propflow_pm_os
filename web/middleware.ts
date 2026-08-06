import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Role-to-Route permissions map
const ROLE_PERMISSIONS: Record<string, string[]> = {
  pm_admin: ["/pm-admin", "/lead-gen", "/owner", "/tenant", "/vendor"], // Admin can view all
  lead_gen: ["/lead-gen"],
  owner: ["/owner"],
  tenant: ["/tenant"],
  vendor: ["/vendor"],
};

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const userRole = request.cookies.get("user_role")?.value;

  // 1. Allow access to login page and public static assets
  if (pathname === "/login" || pathname.startsWith("/_next") || pathname.includes(".")) {
    return NextResponse.next();
  }

  // 2. If no role cookie exists, redirect to login screen
  if (!userRole) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // 3. Check if current route is allowed for user's role
  const allowedRoutes = ROLE_PERMISSIONS[userRole] || [];
  const isAuthorized = allowedRoutes.some((route) => pathname.startsWith(route));

  if (!isAuthorized) {
    // Redirect user to their default permitted portal
    const defaultPortal = allowedRoutes[0] || "/login";
    return NextResponse.redirect(new URL(defaultPortal, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/lead-gen/:path*",
    "/pm-admin/:path*",
    "/owner/:path*",
    "/tenant/:path*",
    "/vendor/:path*",
    "/",
  ],
};
