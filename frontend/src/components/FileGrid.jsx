import { useState } from 'react';
import api from "../services/api";
import FilePreview from './FilePreview';

export default function FileGrid({ files, mode = "drive", onRefresh }) {
  const [previewFile, setPreviewFile] = useState(null);

  const viewFile = (file) => {
    setPreviewFile(file);
  };

  const closePreview = () => {
    setPreviewFile(null);
  };

  const moveToTrash = async (id) => {
    await api.delete(`/files/${id}`);
    onRefresh();
  };

  const restoreFile = async (id) => {
    await api.patch(`/files/${id}/restore`);
    onRefresh();
  };

  const deletePermanent = async (id) => {
    await api.delete(`/files/${id}/permanent`);
    onRefresh();
  };

  const toggleStar = async (id) => {
    await api.patch(`/files/${id}/star`);
    onRefresh();
  };

  return (
    <>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-6">
        {files.map((file) => (
          <div
            key={file.id}
            className="border-2 border-dashed rounded-2xl p-4 border-gray-600
                       bg-gray-800"
          >
            {/* PREVIEW */}
            <div
              onClick={() => viewFile(file)}
              className="h-32 flex items-center justify-center
                         cursor-pointer text-4xl"
            >
              📄
            </div>

            <p className="mt-2 font-medium truncate">{file.name}</p>

            {/* ACTIONS */}
            <div className="flex justify-between mt-3 text-sm">
              <button onClick={() => viewFile(file)}>👁</button>

              {mode === "drive" && (
                <>
                  <button onClick={() => toggleStar(file.id)}>
                    {file.is_starred ? "⭐" : "☆"}
                  </button>
                  <button onClick={() => moveToTrash(file.id)}>🗑</button>
                </>
              )}

              {mode === "trash" && (
                <>
                  <button onClick={() => restoreFile(file.id)}>♻</button>
                  <button onClick={() => deletePermanent(file.id)}>❌</button>
                </>
              )}
            </div>
          </div>
        ))}
      </div>

      {previewFile && (
        <FilePreview file={previewFile} onClose={closePreview} />
      )}
    </>
  );
}
