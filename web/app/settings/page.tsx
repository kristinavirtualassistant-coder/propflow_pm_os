"use client";

import { useEffect, useState } from "react";

export default function SettingsPage() {
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then((res) => res.json())
      .then((data) => {
        setHealth(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Health check failed:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          ⚙️ System Configuration & Health
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          PropFlow PM OS — Infrastructure Status, Database Connections & System Parameters
        </p>
      </div>

      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-900">
          ⚡ Core System Health Check
        </h2>
        {loading ? (
          <p className="text-xs text-slate-400 animate-pulse">Querying system status...</p>
        ) : (
          <div className="grid grid-cols-2 gap-4 text-xs font-mono">
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
              <span className="text-slate-500 font-sans block">Backend Status</span>
              <span className="text-base font-bold text-emerald-600">{health?.status || "UNKNOWN"}</span>
            </div>
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
              <span className="text-slate-500 font-sans block">Database Connection</span>
              <span className="text-base font-bold text-blue-600">{health?.database || "DISCONNECTED"}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
