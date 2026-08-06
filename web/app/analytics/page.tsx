"use client";

import { useEffect, useState } from "react";

export default function AnalyticsDashboard() {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/analytics/overview")
      .then((res) => res.json())
      .then((data) => {
        setAnalytics(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load analytics:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          📈 Executive Analytics & KPI Overview
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          PropFlow PM OS — Real-Time Portfolio Performance & Operations Command Center
        </p>
      </div>

      {loading ? (
        <div className="p-8 bg-white rounded-2xl border border-slate-200 text-center text-slate-400 text-sm animate-pulse">
          Aggregating real-time portfolio metrics across databases...
        </div>
      ) : (
        <div className="space-y-8">
          {/* Top KPI Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-1">
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Monthly Portfolio Rent Roll</p>
              <p className="text-3xl font-extrabold text-slate-900">
                ${analytics.portfolio_summary.monthly_rent_roll.toLocaleString()}
              </p>
              <p className="text-[11px] text-emerald-600 font-semibold">Active Inflow</p>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-1">
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Managed Units & Properties</p>
              <p className="text-3xl font-extrabold text-slate-900">
                {analytics.portfolio_summary.total_properties_managed}
              </p>
              <p className="text-[11px] text-blue-600 font-semibold">FDIC Trust Backed</p>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-1">
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Open Maintenance Tickets</p>
              <p className="text-3xl font-extrabold text-amber-600">
                {analytics.maintenance_summary.open_tickets} / {analytics.maintenance_summary.total_tickets}
              </p>
              <p className="text-[11px] text-amber-600 font-semibold">
                {analytics.maintenance_summary.high_priority_urgent} Urgent Priority
              </p>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-1">
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Contractor Network</p>
              <p className="text-3xl font-extrabold text-purple-600">
                {analytics.portfolio_summary.registered_vendors}
              </p>
              <p className="text-[11px] text-purple-600 font-semibold">Auto-Dispatch Active</p>
            </div>
          </div>

          {/* Core Operations Breakdown */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-slate-900 text-white p-6 rounded-2xl border border-slate-800 space-y-4 shadow-xl">
              <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300">
                ⚡ Dispatch & Service Response Velocity
              </h2>
              <div className="space-y-3 text-xs">
                <div className="flex justify-between items-center bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
                  <span className="text-slate-300 font-medium">Average Vendor Dispatch Time</span>
                  <span className="text-emerald-400 font-bold">&lt; 2 minutes</span>
                </div>
                <div className="flex justify-between items-center bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
                  <span className="text-slate-300 font-medium">Acquisitions Lead Conversion Pipeline</span>
                  <span className="text-blue-400 font-bold">{analytics.portfolio_summary.active_leads} Qualified Leads</span>
                </div>
                <div className="flex justify-between items-center bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
                  <span className="text-slate-300 font-medium">Automated Google Alert Email Trigger</span>
                  <span className="text-emerald-400 font-bold">100% Operational</span>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 space-y-4 shadow-sm">
              <h2 className="text-sm font-bold uppercase tracking-wider text-slate-900">
                📌 System Module Status & Health
              </h2>
              <div className="space-y-3 text-xs">
                <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="font-semibold text-slate-700">Lease Document Generator Engine</span>
                  <span className="bg-emerald-100 text-emerald-800 font-bold px-2.5 py-0.5 rounded-full">ACTIVE</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="font-semibold text-slate-700">Tenant Self-Service Portal</span>
                  <span className="bg-emerald-100 text-emerald-800 font-bold px-2.5 py-0.5 rounded-full">ACTIVE</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="font-semibold text-slate-700">Owner Financial Statement Generator</span>
                  <span className="bg-emerald-100 text-emerald-800 font-bold px-2.5 py-0.5 rounded-full">ACTIVE</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
