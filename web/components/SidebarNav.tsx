"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const PORTALS = [
  { key: "lead-gen", name: "1. LeadGen Portal", icon: "🔍", path: "/lead-gen" },
  { key: "pm-admin", name: "2. PM Admin", icon: "🏢", path: "/pm-admin" },
  { key: "owner", name: "3. Owner Portal", icon: "📈", path: "/owner" },
  { key: "tenant", name: "4. Tenant Portal", icon: "🔑", path: "/tenant" },
  { key: "vendor", name: "5. Vendor Portal", icon: "🛠️", path: "/vendor" },
];

export default function SidebarNav() {
  const pathname = usePathname();
  const router = useRouter();
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    const cookies = document.cookie.split("; ").reduce((acc: any, current) => {
      const [name, value] = current.split("=");
      acc[name] = value;
      return acc;
    }, {});
    setRole(cookies.user_role || null);
  }, [pathname]);

  const handleSignOut = () => {
    document.cookie = "user_role=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    document.cookie = "user_name=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    router.push("/login");
    router.refresh();
  };

  if (pathname === "/login") return null;

  return (
    <aside className="w-64 bg-slate-900 text-white min-h-screen p-4 flex flex-col justify-between">
      <div>
        <div className="flex items-center space-x-2 border-b border-slate-800 pb-4 mb-6">
          <span className="text-2xl">⚡</span>
          <div>
            <h1 className="font-bold text-lg text-blue-400">PROPFLOW PM OS</h1>
            <p className="text-xs text-slate-400">Role: <span className="text-emerald-400 font-mono uppercase">{role || "Guest"}</span></p>
          </div>
        </div>

        <nav className="space-y-1">
          {PORTALS.map((portal) => {
            const isActive = pathname.startsWith(portal.path);
            return (
              <Link
                key={portal.key}
                href={portal.path}
                className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <span>{portal.icon}</span>
                <span>{portal.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="border-t border-slate-800 pt-4 space-y-3">
        <button
          onClick={handleSignOut}
          className="w-full py-2 bg-slate-800 hover:bg-rose-900/40 text-slate-300 hover:text-rose-300 text-xs font-semibold rounded-lg transition-colors border border-slate-700"
        >
          🔒 Sign Out / Switch Role
        </button>
        <div className="text-[10px] text-slate-500 text-center">
          PropFlow RBAC Active
        </div>
      </div>
    </aside>
  );
}
