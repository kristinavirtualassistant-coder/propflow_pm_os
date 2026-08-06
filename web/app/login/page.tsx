"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("admin@propflow.com");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        throw new Error("Invalid login details. Password is 'password123'");
      }

      const data = await res.json();

      // Set cookie for Next.js Middleware (valid for 1 day)
      document.cookie = `user_role=${data.role}; path=/; max-age=86400`;
      document.cookie = `user_name=${data.name}; path=/; max-age=86400`;

      // Redirect to user's assigned portal
      router.push(data.portal);
      router.refresh();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const quickSwitch = (demoEmail: string) => {
    setEmail(demoEmail);
    setPassword("password123");
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full p-8 shadow-2xl border border-slate-200 space-y-6">
        <div className="text-center space-y-1">
          <div className="inline-block text-3xl mb-1">⚡</div>
          <h1 className="text-2xl font-bold text-slate-900">PROPFLOW PM OS</h1>
          <p className="text-xs text-slate-500">Select a Role Profile to Test RBAC Middleware</p>
        </div>

        {/* Demo Role Selector Quick Buttons */}
        <div className="space-y-1.5">
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider text-center">Quick Demo Profiles</p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <button type="button" onClick={() => quickSwitch("admin@propflow.com")} className="p-2 border rounded-lg bg-slate-50 hover:bg-slate-100 text-left font-medium">
              🏢 PM Admin
            </button>
            <button type="button" onClick={() => quickSwitch("lead@propflow.com")} className="p-2 border rounded-lg bg-slate-50 hover:bg-slate-100 text-left font-medium">
              🔍 LeadGen
            </button>
            <button type="button" onClick={() => quickSwitch("owner@propflow.com")} className="p-2 border rounded-lg bg-slate-50 hover:bg-slate-100 text-left font-medium">
              📈 Owner
            </button>
            <button type="button" onClick={() => quickSwitch("tenant@propflow.com")} className="p-2 border rounded-lg bg-slate-50 hover:bg-slate-100 text-left font-medium">
              🔑 Resident Tenant
            </button>
            <button type="button" onClick={() => quickSwitch("vendor@propflow.com")} className="p-2 border rounded-lg bg-slate-50 hover:bg-slate-100 text-left font-medium col-span-2">
              🛠️ Maintenance Vendor
            </button>
          </div>
        </div>

        {error && (
          <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Email Address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm rounded-lg transition-colors"
          >
            Sign In & Access Portal
          </button>
        </form>
      </div>
    </div>
  );
}
