export function isAuthenticated() {
  const token = localStorage.getItem("token");
  return !!token; // true if token exists
}
