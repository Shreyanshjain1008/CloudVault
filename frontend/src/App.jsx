import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Trash from "./pages/Trash";
import Login from "./pages/Login";
import Shared from "./pages/Shared";
import { isAuthenticated } from "./hooks/useAuth";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          path="/"
          element={isAuthenticated() ? <Dashboard /> : <Navigate to="/login" />}
        />

        <Route
          path="/shared"
          element={isAuthenticated() ? <Shared /> : <Navigate to="/login" />}
        />

        <Route
          path="/trash"
          element={isAuthenticated() ? <Trash /> : <Navigate to="/login" />}
        />
      </Routes>
    </BrowserRouter>
  );
}
