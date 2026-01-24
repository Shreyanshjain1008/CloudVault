import { useState } from "react";
import  api  from "../services/api";

export default function UploadZone({ onUploaded }) {
  const [uploads, setUploads] = useState([]);

  const uploadFiles = async (files) => {
    [...files].forEach((file) => {
      const form = new FormData();
      form.append("file", file);

      const upload = {
        name: file.name,
        progress: 0,
      };

      setUploads((u) => [...u, upload]);

      api.post("/files/upload", form, {
        onUploadProgress: (e) => {
          upload.progress = Math.round((e.loaded * 100) / e.total);
          setUploads((u) => [...u]);
        },
      }).then((res) => {
        onUploaded(res.data);
      });
    });
  };

  return (
    <div
      onDrop={(e) => {
        e.preventDefault();
        uploadFiles(e.dataTransfer.files);
      }}
      onDragOver={(e) => e.preventDefault()}
      className="border-2 border-dashed rounded-xl p-6 text-center
                 bg-gray-800 border-gray-600"
    >
      <p className="text-gray-300">
        Drag & drop files here or click to upload
      </p>

      <input
        type="file"
        multiple
        className="hidden"
        id="fileInput"
        onChange={(e) => uploadFiles(e.target.files)}
      />

      <label
        htmlFor="fileInput"
        className="mt-3 inline-block px-4 py-2 bg-blue-600
                   text-white rounded cursor-pointer"
      >
        Select Files
      </label>

      <div className="mt-4 space-y-2">
        {uploads.map((f, i) => (
          <div key={i}>
            <p className="text-sm">{f.name}</p>
            <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded">
              <div
                className="h-2 bg-blue-600 rounded"
                style={{ width: `${f.progress}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
