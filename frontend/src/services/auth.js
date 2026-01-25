import  api  from "./api";

export async function loginUser(email, password) {
  const res = await api.post("/auth/login", {
    email,
    password
  });

  localStorage.setItem("token", res.data.access_token);
  return res.data;
}
