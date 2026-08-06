"use client";

import { useEffect, useState } from "react";

interface Lead {
  id: string;
  address: string;
  city: string;
  owner: string;
  type: string;
  equity: string;
  tags: string[];
  phones: string[];
}

export default function LeadGenPortal() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Modal & Form State
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [formData, setFormData] = useState({
    address: "",
    city: "Austin, TX",
    owner: "",
    type: "INDIVIDUAL",
    equity: "$250,000",
    tagsInput: "ABSENTEE_OWNER, HIGH_EQUITY",
    phonesInput: "",
  });

  // Fetch leads from FastAPI
  const fetchLeads = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/leads");
      if (!res.ok) throw new Error("Failed to fetch leads from FastAPI backend");
      const data = await res.json();
      setLeads(data);
      setLoading(false);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  // Handle Form Submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);

    const payload = {
      address: formData.address,
      city: formData.city,
      owner: formData.owner,
      type: formData.type,
      equity: formData.equity,
      tags: formData.tagsInput.split(",").map((t) => t.trim()).filter(Boolean),
      phones: formData.phonesInput.split(",").map((p) => p.trim()).filter(Boolean),
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Failed to create new lead");

      // Reset form and close modal
      setFormData({
        address: "",
        city: "Austin, TX",
        owner: "",
        type: "INDIVIDUAL",
        equity: "$250,000",
        tagsInput: "ABSENTEE_OWNER, HIGH_EQUITY",
        phonesInput: "",
      });
      setIsModalOpen(false);
      setSubmitting(false);

      // Refresh list
      fetchLeads();
    } catch (err: any) {
      alert(`Error adding lead: ${err.message}`);
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header Bar */}
      <div className="flex justify-between items-center border-b pb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">1. LeadGen & Off-Market Deal Finder</h1>
          <p className="text-slate-500 text-sm">PropStream-Style Skip-Tracing & Pipeline Management</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsModalOpen(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm px-4 py-2 rounded-lg transition-colors flex items-center gap-1 shadow-sm"
          >
            <span>+</span> Add New Lead
          </button>
          <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded-full">
            Active Market: Austin, TX
          </span>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="p-8 text-center text-slate-500 bg-white rounded-xl border border-slate-200">
          Loading live leads from FastAPI backend...
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-sm">
          Error: {error}
        </div>
      )}

      {/* Leads Grid */}
      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {leads.map((lead) => (
            <div key={lead.id} className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-bold text-slate-900">{lead.address}</h3>
                  <p className="text-sm text-slate-500">{lead.city}</p>
                </div>
                <span className="bg-amber-100 text-amber-800 text-xs font-bold px-2.5 py-1 rounded">
                  Est. Equity: {lead.equity}
                </span>
              </div>
              <div className="text-sm space-y-1 bg-slate-50 p-3 rounded-lg border border-slate-100">
                <p><span className="font-medium text-slate-700">Owner:</span> {lead.owner} ({lead.type})</p>
                <p><span className="font-medium text-slate-700">Skip-Traced Phone(s):</span> {lead.phones.length > 0 ? lead.phones.join(", ") : "None"}</p>
              </div>
              <div className="flex gap-2 flex-wrap">
                {lead.tags.map((tag) => (
                  <span key={tag} className="bg-slate-200 text-slate-700 text-xs px-2 py-0.5 rounded font-mono">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Lead Modal Overlay */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200 space-y-4">
            <div className="flex justify-between items-center border-b pb-3">
              <h2 className="text-xl font-bold text-slate-900">Add Off-Market Lead</h2>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 font-bold text-lg"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Property Address</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. 1204 East 6th St"
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">City / State</label>
                  <input
                    type="text"
                    required
                    value={formData.city}
                    onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Est. Equity</label>
                  <input
                    type="text"
                    required
                    value={formData.equity}
                    onChange={(e) => setFormData({ ...formData, equity: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Owner Name</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Jane Doe"
                    value={formData.owner}
                    onChange={(e) => setFormData({ ...formData, owner: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Owner Type</label>
                  <select
                    value={formData.type}
                    onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none bg-white"
                  >
                    <option value="INDIVIDUAL">INDIVIDUAL</option>
                    <option value="LLC">LLC</option>
                    <option value="TRUST">TRUST</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Skip-Traced Phone(s)</label>
                <input
                  type="text"
                  placeholder="+1 (512) 555-0123, +1 (512) 555-0124"
                  value={formData.phonesInput}
                  onChange={(e) => setFormData({ ...formData, phonesInput: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Tags (comma-separated)</label>
                <input
                  type="text"
                  value={formData.tagsInput}
                  onChange={(e) => setFormData({ ...formData, tagsInput: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 text-sm font-medium bg-blue-600 hover:bg-blue-700 text-white rounded-lg disabled:opacity-50"
                >
                  {submitting ? "Saving..." : "Save Lead to DB"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
