import Sidebar from "../components/Sidebar";
import TopBar from "../components/TopBar";

export default function Shared() {
  return (
    <div className="flex bg-gray-900 min-h-screen">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <TopBar onSearch={() => {}} />

        <div className="p-10">
          <h1 className="text-2xl font-semibold mb-4 text-white">
            Shared with me
          </h1>

          <div className="bg-gray-800 rounded-xl shadow p-10 text-center text-gray-400">
            <p className="text-lg">
              No files have been shared with you yet.
            </p>
            <p className="text-sm mt-2">
              When someone shares a file with you, it will appear here.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
