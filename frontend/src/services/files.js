import api from "./api";

/**
 * Search files
 */
export const searchFiles = (q) => api.get(`/files/search?q=${encodeURIComponent(q)}`);

/**
 * Get trash
 */
export const getTrash = () => api.get("/files/trash");

/**
 * Upload a single file.
 * IMPORTANT: do NOT set Content-Type manually — the browser will set the correct multipart boundary.
 */
export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file); // server expects field name "file"

  return api.post("/files/upload", formData);
};