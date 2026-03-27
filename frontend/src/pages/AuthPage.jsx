import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

import { useAuth } from "../auth/AuthContext";

export default function AuthPage({ mode }) {
  const isLogin = mode === "login";
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, isAuthReady, login, register } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const redirectTo = location.state?.from?.pathname || "/";

  async function handleSubmit(event) {
    event.preventDefault();
    setErrorMessage("");
    setIsSubmitting(true);

    try {
      if (isLogin) {
        await login(email, password);
        navigate(redirectTo, { replace: true });
      } else {
        await register(email, password);
        await login(email, password);
        navigate("/", { replace: true });
      }
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isAuthReady && isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="page-shell">
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />

      <main className="auth-card">
        <p className="eyebrow">Study English With Tobi</p>
        <h1>{isLogin ? "Welcome back" : "Create your account"}</h1>
        <p className="auth-subtitle">
          {isLogin
            ? "Log in to continue your listening practice."
            : "Register to save access to your English learning workspace."}
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label className="field-label" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            className="auth-input"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@example.com"
            required
          />

          <label className="field-label" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            className="auth-input"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="At least 6 characters"
            minLength={6}
            required
          />

          {errorMessage ? <div className="error-banner">{errorMessage}</div> : null}

          <button className="primary-button auth-submit" type="submit" disabled={isSubmitting}>
            {isSubmitting
              ? isLogin
                ? "Signing in..."
                : "Creating account..."
              : isLogin
                ? "Login"
                : "Register"}
          </button>
        </form>

        <p className="auth-switch">
          {isLogin ? "Need an account?" : "Already have an account?"}{" "}
          <Link to={isLogin ? "/register" : "/login"} className="auth-link">
            {isLogin ? "Register" : "Login"}
          </Link>
        </p>
      </main>
    </div>
  );
}
