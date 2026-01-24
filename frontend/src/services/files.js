import api from "./api";

export const searchFiles = (q) =>
  api.get(`/files/search?q=${q}`);

export const getTrash = () =>
  api.get("/files/trash");

export const initUpload = (data) =>
  api.post("/files/init-upload", data);
