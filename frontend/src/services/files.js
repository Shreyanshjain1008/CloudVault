import api from "./api";

export const searchFiles = (q) =>
  api.get(`/files/search?q=${q}`);

export const getTrash = () =>
  api.get("/files/trash");

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file); // MUST be "file"

  return api.post("/files/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};
