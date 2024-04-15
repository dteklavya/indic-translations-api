// """src/app/auth/utils: """


// __author__ = "Rajesh Pethe"
// __date__ = "04/14/2024 16:29:19"
// __credits__ = ["Rajesh Pethe"]

import wretch from "wretch";
import Cookies from "js-cookie";
import { emitWarning } from "process";

// Base API settings
const api = wretch("http://localhost:8000").accept("application/json")

/**
 * Stores a token in cookies
 * @param {string} token = Te token to be stored.
 * @param {"access" | "refresh"} type - Type of token.
 */
const storeToken = (token: string, type: "access" | "refresh") => {
    Cookies.set(type + "Token", token);
};

/**
 * Retrieves a token from cookies.
 * @param {"access" | "refresh"} type - Type of token to retrieve.
 * @returns {string | undefined} The token if found.
 */
const getToken = (type: string) => {
    return Cookies.get(type + "Token");
};

/**
 * Removes both tokens from cookies. Logs out!
 */
const removeTokens = () => {
    Cookies.remove("accessToken");
    Cookies.remove("refreshToken");
};

// User authentication handling
const register = (email: string, username: string, password: string) => {
    return api.post({ email, username, password }, "/auth/users/");
};

const login = (email: string, password: string) => {
    return api.post({ username: email, password }, "/auth/jwt/create");
};

const logout = () => {
    const refreshToken = getToken("refresh");
    return api.post({ refresh: refreshToken }, "/auth/logout/");
};

const refreshJWT = () => {
    const refreshToken = getToken("refresh");
    return api.post({ refresh: refreshToken }, "/auth/jwt/refresh");
};

const resetPassword = (email: string) => {
    return api.post({ email }, "/auth/users/reset_password/");
};

const resetPasswordConfirm = (
    new_password: string,
    re_new_password: string,
    token: string,
    uid: string
) => {
    return api.post(
        { uid, token, new_password, re_new_password },
        "/auth/users/reset_password_confirm/"
    );
};


// Exports
export const AuthActions = () => {
    return {
        login,
        resetPasswordConfirm,
        refreshJWT,
        register,
        resetPassword,
        storeToken,
        getToken,
        logout,
        removeTokens,
    };
};
