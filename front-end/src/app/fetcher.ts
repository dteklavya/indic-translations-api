// """src/app/fetchers.ts: """


// __author__ = 'Rajesh Pethe'
// __date__ = '04/14/2024 18:04:43'
// __credits__ = ['Rajesh Pethe']


import wretch, { Wretch, WretchError } from "wretch";
import { AuthActions } from "@/app/auth/utils";

// Get required function from AuthActions utility
const { refreshJWT, storeToken, getToken } = AuthActions();

const api = () => {
    return (
        wretch("http://localhost:8000")
            // Initialize authentication with access token
            .auth(`Bearer ${getToken("access")}`)
            // Catch 401 un-authorized
            .catcher(401, async (error: WretchError, request: Wretch) => {
                try {
                    // Attempt to refresh token
                    const { access } = (await refreshJWT().json()) as {
                        access: string;
                    }

                    // Store the new access token
                    storeToken(access, "access");

                    // Replay the original request
                    return request
                        .auth(`Bearer ${access}`)
                        .fetch()
                        .unauthorized(() => {
                            window.location.replace("/");
                        })
                        .json();
                } catch (err) {
                    window.location.replace("/");
                }
            })
    )
}

export const fetcher = (url: string): Promise<any> => {
    return api().get(url).json();
};
