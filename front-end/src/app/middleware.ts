// """src/middleware.ts: """


// __author__ = 'Rajesh Pethe'
// __date__ = '04/16/2024 16:59:57'
// __credits__ = ['Rajesh Pethe']


import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { cookies } from "next/headers";


export function middleware(request: NextRequest) {
    const cookieStore = cookies();
    const accessToken = cookieStore.get("accessToken");

    if (!accessToken && request.nextUrl.pathname !== "/") {
        return NextResponse.redirect(new URL("/", request.url));
    }
}

export const config = {
    matcher: ["/((?!api|auth|_next/static|_next/image|.*\\.png$).*)"],
};
