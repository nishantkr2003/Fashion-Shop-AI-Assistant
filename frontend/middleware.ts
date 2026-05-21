import { NextRequest, NextResponse } from "next/server";

const PUBLIC = ["/login", "/signup"];

export function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname;

  const access = req.cookies.get("access_token");

  const isPublic = PUBLIC.some((p) => path.startsWith(p));

  if (!access && !isPublic) {
    return NextResponse.redirect(
      new URL(
        "/login",

        req.url,
      ),
    );
  }

  if (access && isPublic) {
    return NextResponse.redirect(
      new URL(
        "/chat",

        req.url,
      ),
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/chat/:path*", "/login", "/signup"],
};
