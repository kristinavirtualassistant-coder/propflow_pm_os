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

export default function PMAdminPortal() {
  const [orders, setOrders] = useState<WorkOrder[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    property_address: "",
    unit: "",
    title: "",
    description: "",
    priority: "MEDIUM",
  });

  const fetchOrders = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/work-orders");
      const data = await res.json();
      setOrders(data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleCreateOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/work-orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (res.ok) {
        setIsModalOpen(false);
        setFormData({ property_address: "", unit: "", title: "", description: "", priority: "MEDIUM" });
        fetchOrders();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleStatusChange = async (id: string, newStatus: string) => {
    try {
      await fetch(`http://127.0.0.1:8000/api/v1/work-orders/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });
      fetchOrders();
    } catch (err) {
      console.error(err);
    }
  };

  const openCount = orders.filter((o) => o.status === "OPEN").length;
  const inProgressCount = orders.filter((o) => o.status === "IN_PROGRESS").length;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center border-b pb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">2. PM Admin Master Command Center</h1>
          <p className="text-slate-500 text-sm">Portfolio Operations & Maintenance Work Order Dispatch</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm px-4 py-2 rounded-lg transition-colors"
        >
          + New Maintenance Ticket
        </button>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-xs font-medium text-slate-500 uppercase">Active Properties</p>
          <p className="text-2xl font-bold text-slate-900 mt-1">12 Managed</p>
        </div>
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-xs font-medium text-slate-500 uppercase">Occupancy Rate</p>
          <p className="text-2xl font-bold text-emerald-600 mt-1">94.2%</p>
        </div>
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-xs font-medium text-slate-500 uppercase">Open Tickets</p>
          <p className="text-2xl font-bold text-rose-600 mt-1">{openCount} Unassigned</p>
        </div>
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-xs font-medium text-slate-500 uppercase">In Progress</p>
          <p className="text-2xl font-bold text-amber-600 mt-1">{inProgressCount} Active</p>
        </div>
      </div>

      {/* Work Orders List */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 border-b bg-slate-50 flex justify-between items-center">
          <h3 className="font-bold text-slate-800">Maintenance & Work Order Queue</h3>
          <span className="text-xs text-slate-500">{orders.length} Total Tickets</span>
        </div>

        {loading ? (
          <div className="p-6 text-center text-slate-500 text-sm">Loading tickets from database...</div>
        ) : (
          <div className="divide-y divide-slate-100">
            {orders.map((ticket) => (
              <div key={ticket.id} className="p-5 flex flex-col md:flex-row justify-between md:items-center gap-4 hover:bg-slate-50/50">
                <div className="space-y-1 max-w-xl">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-slate-400">{ticket.id}</span>
                    <h4 className="font-bold text-slate-900">{ticket.title}</h4>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${
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
                  <p className="text-xs text-slate-500 font-medium">
                    📍 {ticket.property_address} {ticket.unit ? `(${ticket.unit})` : ""}
                  </p>
                  <p className="text-sm text-slate-600">{ticket.description}</p>
                </div>

                <div className="flex items-center gap-3">
                  <select
                    value={ticket.status}
                    onChange={(e) => handleStatusChange(ticket.id, e.target.value)}
                    className="text-xs font-semibold px-3 py-1.5 rounded-lg border outline-none bg-white cursor-pointer"
                  >
                    <option value="OPEN">🔴 OPEN</option>
                    <option value="IN_PROGRESS">🟡 IN_PROGRESS</option>
                    <option value="COMPLETED">🟢 COMPLETED</option>
                  </select>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border space-y-4">
            <h2 className="text-xl font-bold text-slate-900 border-b pb-3">Create Work Order</h2>
            <form onSubmit={handleCreateOrder} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Property Address</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. 1204 East 6th St"
                  value={formData.property_address}
                  onChange={(e) => setFormData({ ...formData, property_address: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Unit (Optional)</label>
                  <input
                    type="text"
                    placeholder="e.g. Apt 2B"
                    value={formData.unit}
                    onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Priority</label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm bg-white outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                    <option value="EMERGENCY">EMERGENCY</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Issue Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Water Leak Under Kitchen Sink"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Description</label>
                <textarea
                  required
                  rows={3}
                  placeholder="Provide diagnostic details..."
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="flex justify-end gap-2 pt-3 border-t">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
                >
                  Dispatch Ticket
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
