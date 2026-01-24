import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import TopBar from "../components/TopBar";
import FileGrid from "../components/FileGrid";
import api from "../services/api";
import { isAuthenticated } from "../hooks/useAuth";
import { Navigate } from "react-router-dom";

export default function Trash() {
  const [files, setFiles] = useState([]);

  const loadTrash = async () => {
    const res = await api.get("/files/trash");
    setFiles(res.data);
  };

  useEffect(() => {
    loadTrash();
  }, []);

  if (!isAuthenticated()) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="flex min-h-screen bg-gray-900">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <TopBar />

        <div className="flex-1 p-8">
          <h2 className="text-2xl font-semibold text-red-400 mb-2">
            Trash
          </h2>

          <p className="text-sm text-gray-400 mb-6">
            Items in trash can be restored or permanently deleted.
          </p>

          <FileGrid
            files={files}
            mode="trash"
            onRefresh={loadTrash}
          />
        </div>
      </div>
    </div>
  );
}
