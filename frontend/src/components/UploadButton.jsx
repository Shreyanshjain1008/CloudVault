import { useState } from "react";
import  api  from "../services/api";

export default function UploadButton({ onUploaded }) {
  const [progress, setProgress] = useState(0);
  const [uploading, setUploading] = useState(false);

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    setProgress(0);

    try {
      await api.post("/files/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (e) => {
          const percent = Math.round((e.loaded * 100) / e.total);
          setProgress(percent);
        },
      });

      onUploaded(); // refresh file list
    } catch {
      alert("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mb-6">
      <input
        type="file"
        onChange={(e) => uploadFile(e.target.files[0])}
      />

      {uploading && (
        <div className="mt-2 w-full bg-gray-700 rounded">
          <div
            className="bg-blue-600 text-white text-sm p-1 rounded"
            style={{ width: `${progress}%` }}
          >
            {progress}%
          </div>
        </div>
      )}
    </div>
  );
}
