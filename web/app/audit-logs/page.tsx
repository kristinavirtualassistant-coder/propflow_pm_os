"use client";

import { useEffect, useState } from "react";

export default function AuditLogsPage() {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");

  const fetchLogs = () => {
    setLoading(true);
    fetch("http://127.0.0.1:8000/api/v1/system/audit-logs")
      .then((res) => res.json())
      .then((data) => {
        setLogs(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch audit logs:", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const filteredLogs = logs.filter(
    (log) =>
      log.event_type.toLowerCase().includes(filter.toLowerCase()) ||
      log.description.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            📜 System Audit Trail & Event Logs
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            PropFlow PM OS — Immutable Activity Log & Security Event Inspector
          </p>
        </div>

        <button
          onClick={fetchLogs}
          className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition-colors flex items-center gap-2 shadow-sm"
        >
          🔄 Refresh Log Stream
        </button>
      </div>

      {/* Filter & Search Controls */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
        <span className="text-xs font-bold text-slate-400 uppercase tracking-wider pl-2">Filter Events:</span>
        <input
          type="text"
          placeholder="Search by event type or description (e.g. WORK_ORDER, BACKUP)..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Log Feed Table */}
      {loading ? (
        <div className="p-8 bg-white rounded-2xl border border-slate-200 text-center text-slate-400 text-sm animate-pulse">
          Streaming security event audit trail from propflow.db...
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <table className="w-full text-xs text-left border-collapse">
            <thead>
              <tr className="bg-slate-100 border-b border-slate-200 text-slate-700 font-bold uppercase text-[10px] tracking-wider">
                <th className="p-4">Timestamp (UTC)</th>
                <th className="p-4">Log ID</th>
                <th className="p-4">Event Type</th>
                <th className="p-4">Description</th>
                <th className="p-4">Payload Data</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
              {filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan={5} className="p-8 text-center text-slate-400 font-sans">
                    No system audit logs found matching "{filter}".
                  </td>
                </tr>
              ) : (
                filteredLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="p-4 text-slate-500 whitespace-nowrap">{log.timestamp}</td>
                    <td className="p-4 font-bold text-slate-900">{log.id}</td>
                    <td className="p-4">
                      <span className="bg-blue-50 text-blue-800 text-[10px] font-extrabold px-2.5 py-1 rounded-md border border-blue-200">
                        {log.event_type}
                      </span>
                    </td>
                    <td className="p-4 font-sans text-slate-700">{log.description}</td>
                    <td className="p-4 text-slate-500">
                      {log.payload ? JSON.stringify(log.payload) : "—"}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
