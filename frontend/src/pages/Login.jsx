import { useState } from "react";
import api from "../services/api";
import "./login.css";

export default function Login() {
  const [isSignup, setIsSignup] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async () => {
    try {
      if (isSignup) {
        await api.post("/auth/register", { name, email, password });
        alert("Signup successful. Please login.");
        setIsSignup(false);
      } else {
        const res = await api.post("/auth/login", { email, password });
        localStorage.setItem("token", res.data.access_token);
        window.location.href = "/";
      }
    } catch (error) {
      console.error("Auth error:", error);
      alert("Authentication failed: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        {/* LEFT SIDE */}
        <div className="login-left">
          <h2 className="brand">CloudVault</h2>
          <h1>{isSignup ? "Join Us!" : "Welcome Back!"}</h1>
          <p>{isSignup ? "Create your secure cloud storage account." : "Access your secure cloud storage anytime."}</p>

        </div>

        {/* RIGHT SIDE */}
        <div className="login-right">
          <h2>{isSignup ? "Sign Up" : "Sign In"}</h2>

          {isSignup && (
            <input
              type="text"
              placeholder="Full Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          )}

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {!isSignup && (
            <div className="login-options">
              <label>
                <input type="checkbox" /> Remember me
              </label>
              <span className="link" onClick={() => alert("Forgot password functionality not implemented yet.")}>Forgot password?</span>
            </div>
          )}

          <button type="button" className="login-btn" onClick={submit}>
            {isSignup ? "Sign Up" : "Sign In"}
          </button>

          <p className="signup">
            {isSignup ? "Already have an account?" : "Don't have an account?"} <span className="link" onClick={() => setIsSignup(!isSignup)}>{isSignup ? "Sign In" : "Sign up"}</span>
          </p>
        </div>
      </div>
    </div>
  );
}
