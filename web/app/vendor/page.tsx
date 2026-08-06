"use client";

import { useEffect, useState } from "react";

interface WorkOrder {
  id: string;
  property_address: string;
  unit: string;
  title: string;
  description: string;
  priority: "LOW" | "MEDIUM" | "HIGH" | "EMERGENCY";
  status: "OPEN" | "IN_PROGRESS" | "COMPLETED";
  created_at: string;
}

export default function VendorPortal() {
  const [orders, setOrders] = useState<WorkOrder[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"ACTIVE" | "COMPLETED">("ACTIVE");

  const fetchVendorOrders = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/vendor/work-orders");
      const data: WorkOrder[] = await res.json();
      setOrders(data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVendorOrders();
  }, []);

  const handleMarkComplete = async (id: string) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/vendor/complete-order/${id}`, {
        method: "POST",
      });
      if (res.ok) {
        fetchVendorOrders();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const activeTickets = orders.filter((o) => o.status === "OPEN" || o.status === "IN_PROGRESS");
  const completedTickets = orders.filter((o) => o.status === "COMPLETED");
  const emergencyCount = activeTickets.filter((o) => o.priority === "EMERGENCY" || o.priority === "HIGH").length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">5. Maintenance Vendor & Contractor Portal</h1>
          <p className="text-slate-500 text-sm">Dispatched Jobs, Diagnostic Specs, and Work Completion Logs</p>
        </div>
        <div className="flex items-center gap-2">
          {emergencyCount > 0 && (
            <span className="bg-rose-100 text-rose-800 text-xs font-bold px-3 py-1 rounded-full animate-pulse">
              ⚠️ {emergencyCount} High Priority / Emergency
            </span>
          )}
          <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded-full">
            Austin Plumbing & HVAC Crew
          </span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-200 gap-4">
        <button
          onClick={() => setActiveTab("ACTIVE")}
          className={`pb-3 font-semibold text-sm transition-colors border-b-2 ${
            activeTab === "ACTIVE"
              ? "border-blue-600 text-blue-600"
              : "border-transparent text-slate-500 hover:text-slate-700"
          }`}
        >
          Active Assigned Jobs ({activeTickets.length})
        </button>
        <button
          onClick={() => setActiveTab("COMPLETED")}
          className={`pb-3 font-semibold text-sm transition-colors border-b-2 ${
            activeTab === "COMPLETED"
              ? "border-emerald-600 text-emerald-600"
              : "border-transparent text-slate-500 hover:text-slate-700"
          }`}
        >
          Completed History ({completedTickets.length})
        </button>
      </div>

      {/* Job Cards */}
      {loading ? (
        <div className="p-8 text-center text-slate-500 bg-white rounded-xl border">
          Loading assigned work orders...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {(activeTab === "ACTIVE" ? activeTickets : completedTickets).map((ticket) => (
            <div
              key={ticket.id}
              className={`bg-white p-6 rounded-xl border shadow-sm space-y-4 ${
                ticket.priority === "EMERGENCY" ? "border-rose-300 ring-1 ring-rose-200" : "border-slate-200"
              }`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-xs font-mono text-slate-400 font-bold">{ticket.id}</span>
                  <h3 className="text-lg font-bold text-slate-900">{ticket.title}</h3>
                  <p className="text-sm font-medium text-slate-600">
                    📍 {ticket.property_address} {ticket.unit ? `(${ticket.unit})` : ""}
                  </p>
                </div>
                <span
                  className={`text-[10px] font-bold px-2.5 py-1 rounded uppercase ${
                    ticket.priority === "EMERGENCY"
                      ? "bg-rose-100 text-rose-800"
                      : ticket.priority === "HIGH"
                      ? "bg-amber-100 text-amber-800"
                      : "bg-slate-100 text-slate-700"
                  }`}
                >
                  {ticket.priority}
                </span>
              </div>

              <div className="text-sm bg-slate-50 p-3 rounded-lg border border-slate-100 space-y-1">
                <p className="font-semibold text-slate-700 text-xs uppercase">Issue Diagnostics:</p>
                <p className="text-slate-600">{ticket.description}</p>
              </div>

              <div className="flex justify-between items-center pt-2 border-t">
                <span className="text-xs text-slate-400">Created: {ticket.created_at}</span>

                {ticket.status !== "COMPLETED" ? (
                  <button
                    onClick={() => handleMarkComplete(ticket.id)}
                    className="bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold px-4 py-2 rounded-lg transition-colors shadow-sm flex items-center gap-1"
                  >
                    <span>✓</span> Mark Job Completed
                  </button>
                ) : (
                  <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1 rounded">
                    ✓ Job Completed
                  </span>
                )}
              </div>
            </div>
          ))}

          {(activeTab === "ACTIVE" ? activeTickets : completedTickets).length === 0 && (
            <div className="col-span-2 p-8 text-center text-slate-400 bg-white rounded-xl border border-dashed">
              No {activeTab.toLowerCase()} jobs found.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
