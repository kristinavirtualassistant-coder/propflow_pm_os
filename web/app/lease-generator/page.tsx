"use client";

import { useState, useEffect } from "react";

export default function LeaseGenerator() {
  const [template, setTemplate] = useState<any>(null);
  const [formData, setFormData] = useState({
    tenant_name: "Sarah Connor",
    property_address: "1204 East 6th St",
    unit: "Apt 2B",
    lease_start: "2026-09-01",
    lease_end: "2027-08-31",
    monthly_rent: "2400",
    security_deposit: "2400",
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/lease-templates/default")
      .then((res) => res.json())
      .then((data) => setTemplate(data))
      .catch((err) => console.error("Error loading lease template:", err));
  }, []);

  const handleChange = (e: any) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div className="flex justify-between items-center print:hidden">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            📜 Automated Lease Document Generator
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            PropFlow PM OS — Real-Time PDF Contract Auto-Population Engine
          </p>
        </div>
        <button
          onClick={handlePrint}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs px-5 py-3 rounded-xl transition-colors shadow-sm flex items-center gap-2"
        >
          🖨️ Export PDF / Print Agreement
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Form Controls Sidebar (Hidden during print) */}
        <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-slate-200 space-y-4 shadow-sm print:hidden">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider border-b border-slate-100 pb-3">
            Lease Terms & Parameters
          </h2>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-600 font-semibold mb-1">Tenant Legal Name</label>
              <input
                type="text"
                name="tenant_name"
                value={formData.tenant_name}
                onChange={handleChange}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-medium"
              />
            </div>

            <div>
              <label className="block text-slate-600 font-semibold mb-1">Property Address</label>
              <input
                type="text"
                name="property_address"
                value={formData.property_address}
                onChange={handleChange}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-medium"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-600 font-semibold mb-1">Unit #</label>
                <input
                  type="text"
                  name="unit"
                  value={formData.unit}
                  onChange={handleChange}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-medium"
                />
              </div>
              <div>
                <label className="block text-slate-600 font-semibold mb-1">Monthly Rent ($)</label>
                <input
                  type="number"
                  name="monthly_rent"
                  value={formData.monthly_rent}
                  onChange={handleChange}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-medium"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-600 font-semibold mb-1">Lease Start</label>
                <input
                  type="date"
                  name="lease_start"
                  value={formData.lease_start}
                  onChange={handleChange}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-medium"
                />
              </div>
              <div>
                <label className="block text-slate-600 font-semibold mb-1">Lease End</label>
                <input
                  type="date"
                  name="lease_end"
                  value={formData.lease_end}
                  onChange={handleChange}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-medium"
                />
              </div>
            </div>

            <div>
              <label className="block text-slate-600 font-semibold mb-1">Security Deposit ($)</label>
              <input
                type="number"
                name="security_deposit"
                value={formData.security_deposit}
                onChange={handleChange}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-medium"
              />
            </div>
          </div>
        </div>

        {/* Live Document Preview Panel */}
        <div className="lg:col-span-7 bg-white p-10 rounded-2xl border border-slate-300 shadow-md text-slate-800 space-y-6 print:w-full print:border-none print:shadow-none">
          <div className="text-center border-b-2 border-slate-900 pb-6 space-y-1">
            <h2 className="text-2xl font-serif font-bold text-slate-950 uppercase tracking-widest">
              RESIDENTIAL LEASE AGREEMENT
            </h2>
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">
              State of {template?.governing_state || "Texas"} • Standard Statutory Form
            </p>
          </div>

          <div className="text-xs leading-relaxed space-y-4 text-slate-700">
            <p>
              This Residential Lease Agreement (&quot;Agreement&quot;) is entered into on this day, by and between{" "}
              <strong className="text-slate-950 underline">{template?.landlord_legal_name || "PropFlow Asset Management LLC"}</strong> (&quot;Landlord&quot;), and{" "}
              <strong className="text-slate-950 underline">{formData.tenant_name || "[Tenant Name]"}</strong> (&quot;Tenant&quot;).
            </p>

            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-1">
              <p className="font-bold text-slate-900 uppercase tracking-wider text-[10px]">1. Demised Premises</p>
              <p>
                Landlord agrees to lease to Tenant the real property located at:{" "}
                <strong className="text-slate-900">{formData.property_address} ({formData.unit})</strong>.
              </p>
            </div>

            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-1">
              <p className="font-bold text-slate-900 uppercase tracking-wider text-[10px]">2. Term & Financial Considerations</p>
              <p>
                The lease shall commence on <strong className="text-slate-900">{formData.lease_start}</strong> and terminate on{" "}
                <strong className="text-slate-900">{formData.lease_end}</strong>. Tenant agrees to pay monthly rent in the amount of{" "}
                <strong className="text-slate-900">${Number(formData.monthly_rent || 0).toLocaleString()}</strong> due on the 1st of each calendar month.
              </p>
              <p className="text-[11px] text-slate-500 pt-1">
                Security Deposit held in escrow: <strong>${Number(formData.security_deposit || 0).toLocaleString()}</strong>. Late fee of ${template?.late_fee_amount || 75} applies after {template?.grace_period_days || 5} days.
              </p>
            </div>

            <div className="space-y-1">
              <p className="font-bold text-slate-900 uppercase tracking-wider text-[10px]">3. Pet & Occupancy Policies</p>
              <p>{template?.pet_policy || "Allowed with deposit."} Maximum occupancy: {template?.occupancy_limit || 2} persons.</p>
            </div>
          </div>

          <div className="pt-12 grid grid-cols-2 gap-8 border-t border-slate-300">
            <div className="space-y-8">
              <div className="border-b border-slate-900 pb-1">
                <p className="text-[10px] text-slate-400 uppercase tracking-wider font-mono">Landlord Representative Signature</p>
              </div>
              <p className="text-xs font-bold text-slate-900">Date: _______________</p>
            </div>

            <div className="space-y-8">
              <div className="border-b border-slate-900 pb-1">
                <p className="text-[10px] text-slate-400 uppercase tracking-wider font-mono">Tenant Signature</p>
              </div>
              <p className="text-xs font-bold text-slate-900">Date: _______________</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
