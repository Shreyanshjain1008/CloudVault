import { Link, useLocation } from "react-router-dom";


export default function Sidebar() {

  const { pathname } = useLocation();

  const item = (path) =>
    `flex items-center gap-3 px-5 py-3 rounded-xl text-base font-medium
     transition-all
     ${
       pathname === path
         ? "bg-blue-900 text-blue-300"
         : "hover:bg-gray-700 text-gray-300"
     }`;

  return (
    <div className="w-64 h-screen bg-gray-800 border-r border-gray-700 p-4 flex flex-col">
      {/* Logo */}
      <h1 className="text-2xl font-bold px-4 mb-8 text-blue-400">
        CloudVault
      </h1>

      {/* Navigation */}
      <nav className="space-y-4 flex-1 mt-6">
        <Link to="/" className={item("/")}>📁 My Drive</Link>
        <Link to="/shared" className={item("/shared")}>👥 Shared</Link>
        <Link to="/trash" className={item("/trash")}>🗑 Trash</Link>
      </nav>

      
      

    </div>
  );
}
