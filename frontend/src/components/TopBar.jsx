export default function TopBar() {
  return (
    <div
      className="flex justify-between items-center
                 px-8 py-4
                 border-b border-gray-700
                 bg-gray-900
                 sticky top-0 z-50"
    >
      {/* LOGO */}
      <div className="flex items-center">
        {/* Removed CloudVault text */}
      </div>

      {/* ACTIONS */}
      <div className="flex items-center gap-4">
        {/* LOGOUT */}
        <button
          onClick={() => {
            localStorage.removeItem("token");
            window.location.href = "/login";
          }}
          className="
            px-4 py-2
            rounded-full
            font-medium
            bg-red-500 text-white
            hover:bg-red-600
            transition
          "
        >
          Logout
        </button>
      </div>
    </div>
  );
}
