import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import TopBar from "../components/TopBar";
import UploadButton from "../components/UploadButton";
import UploadZone from "../components/UploadZone";
import FileGrid from "../components/FileGrid";
import api from "../services/api";

export default function Dashboard() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  const loadFiles = async (query = "") => {
    try {
      const url = query ? `/files/search?q=${query}` : "/files";
      const res = await api.get(url);
      setFiles(res.data);
    } catch {
      alert("Failed to load files");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFiles();
  }, []);

  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    loadFiles(query);
  };

  return (
    <div className="flex min-h-screen bg-gray-900">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <TopBar />

        {/* SEARCH BAR */}
        <div className="px-8 py-6 bg-gray-900 border-b border-gray-700">
          <input
            value={searchQuery}
            onChange={handleSearch}
            placeholder="Search files..."
            className="
              w-full max-w-2xl
              px-6 py-4
              text-lg
              rounded-full
              border border-gray-700
              outline-none
              bg-gray-800
              text-white
              focus:ring-2 focus:ring-blue-500
            "
          />
        </div>

        <div className="flex-1 overflow-y-auto px-8 pt-8 pb-8 space-y-8">
          {/* Upload Actions */}
          <div className="flex gap-4">
            <UploadButton onUploaded={() => loadFiles(searchQuery)} />
          </div>

          {/* Drag & Drop Zone */}
          <UploadZone onUploaded={() => loadFiles(searchQuery)} />

          {/* Files */}
          {loading ? (
            <p className="text-center text-gray-400">
              Loading files...
            </p>
          ) : (
            <FileGrid files={files} onRefresh={() => loadFiles(searchQuery)} />
          )}
        </div>
      </div>
    </div>
  );
}
