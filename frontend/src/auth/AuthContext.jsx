import { createContext, useContext, useEffect, useMemo, useState } from "react";

import {
  apiRequest,
  clearToken,
  getToken,
  setToken as persistToken,
} from "../lib/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setTokenState] = useState(() => getToken());
  const [user, setUser] = useState(null);
  const [isAuthReady, setIsAuthReady] = useState(false);

  useEffect(() => {
    async function loadCurrentUser() {
      const existingToken = getToken();

      if (!existingToken) {
        setUser(null);
        setIsAuthReady(true);
        return;
      }

      try {
        const response = await apiRequest("/auth/me", { method: "GET" });
        if (!response.ok) {
          throw new Error("Session expired.");
        }

        const data = await response.json();
        setUser(data);
        setTokenState(existingToken);
      } catch {
        clearToken();
        setTokenState(null);
        setUser(null);
      } finally {
        setIsAuthReady(true);
      }
    }

    loadCurrentUser();
  }, []);

  async function register(email, password) {
    const response = await apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.detail || "Could not create your account.");
    }

    return data;
  }

  async function login(email, password) {
    const response = await apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.detail || "Invalid email or password.");
    }

    persistSessionToken(data.access_token);

    const meResponse = await apiRequest("/auth/me", { method: "GET" });
    const currentUser = await meResponse.json().catch(() => null);

    if (!meResponse.ok || !currentUser) {
      throw new Error("Logged in, but failed to load your account.");
    }

    setUser(currentUser);
    return currentUser;
  }

  function persistSessionToken(tokenValue) {
    persistToken(tokenValue);
    setTokenState(tokenValue);
  }

  function logout() {
    clearToken();
    setTokenState(null);
    setUser(null);
  }

  const value = useMemo(
    () => ({
      token,
      user,
      isAuthenticated: Boolean(token),
      isAuthReady,
      register,
      login,
      logout,
    }),
    [token, user, isAuthReady]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider.");
  }

  return context;
}
