"use client";

import { useState } from "react";

interface FinancialRecord {
  id: string;
  owner_name: string;
  property_address: string;
  gross_rent: number;
  management_fee_pct: number;
  reserve_fund_pct: number;
  maintenance_deductions: number;
  month_year: string;
  management_fee_amount: number;
  reserve_fund_amount: number;
  net_distribution: number;
}

export default function FinancialCharts({ records }: { records: FinancialRecord[] }) {
  const [selectedRecordId, setSelectedRecordId] = useState<string>(records[0]?.id || "");

  if (!records || records.length === 0) {
    return (
      <div className="bg-white p-6 rounded-2xl border border-slate-200 text-center text-slate-500 text-sm">
        No financial records available for visual analytics.
      </div>
    );
  }

  const selectedRecord = records.find((r) => r.id === selectedRecordId) || records[0];

  // Calculate percentage splits for visualization
  const gross = selectedRecord.gross_rent || 1;
  const mgmtPct = Math.round((selectedRecord.management_fee_amount / gross) * 100);
  const reservePct = Math.round((selectedRecord.reserve_fund_amount / gross) * 100);
  const maintPct = Math.round((selectedRecord.maintenance_deductions / gross) * 100);
  const netPct = Math.max(0, 100 - (mgmtPct + reservePct + maintPct));

  return (
    <div className="bg-slate-900 text-white rounded-2xl p-6 border border-slate-800 space-y-6 shadow-xl">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            📊 Financial Breakdown & Revenue Distribution
          </h2>
          <p className="text-xs text-slate-400">
            Real-time breakdown of gross rent, management fees, reserves, and net owner payout.
          </p>
        </div>

        {/* Property Filter Dropdown */}
        <select
          value={selectedRecordId}
          onChange={(e) => setSelectedRecordId(e.target.value)}
          className="bg-slate-800 text-slate-200 border border-slate-700 text-xs rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
        >
          {records.map((r) => (
            <option key={r.id} value={r.id}>
              {r.property_address} ({r.month_year})
            </option>
          ))}
        </select>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-slate-800/60 border border-slate-700/50 p-3.5 rounded-xl">
          <p className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Gross Revenue</p>
          <p className="text-xl font-extrabold text-white mt-1">${selectedRecord.gross_rent.toLocaleString()}</p>
          <span className="text-[10px] text-blue-400 font-medium">100% Collected</span>
        </div>

        <div className="bg-slate-800/60 border border-slate-700/50 p-3.5 rounded-xl">
          <p className="text-[10px] uppercase font-bold text-amber-400 tracking-wider">Management Fee</p>
          <p className="text-xl font-extrabold text-amber-300 mt-1">-${selectedRecord.management_fee_amount.toLocaleString()}</p>
          <span className="text-[10px] text-slate-400">{(selectedRecord.management_fee_pct * 100).toFixed(0)}% Fee Structure</span>
        </div>

        <div className="bg-slate-800/60 border border-slate-700/50 p-3.5 rounded-xl">
          <p className="text-[10px] uppercase font-bold text-purple-400 tracking-wider">Reserve Fund</p>
          <p className="text-xl font-extrabold text-purple-300 mt-1">-${selectedRecord.reserve_fund_amount.toLocaleString()}</p>
          <span className="text-[10px] text-slate-400">{(selectedRecord.reserve_fund_pct * 100).toFixed(0)}% Capital Escrow</span>
        </div>

        <div className="bg-emerald-950/40 border border-emerald-800/50 p-3.5 rounded-xl">
          <p className="text-[10px] uppercase font-bold text-emerald-400 tracking-wider">Net Owner Payout</p>
          <p className="text-xl font-extrabold text-emerald-300 mt-1">${selectedRecord.net_distribution.toLocaleString()}</p>
          <span className="text-[10px] text-emerald-400 font-semibold">{netPct}% Net Yield</span>
        </div>
      </div>

      {/* Visual Stacked Revenue Bar chart */}
      <div className="space-y-2">
        <div className="flex justify-between text-xs text-slate-400 font-medium">
          <span>Rent Revenue Allocation Split</span>
          <span className="text-emerald-400 font-bold">${selectedRecord.net_distribution.toLocaleString()} Disbursed</span>
        </div>

        <div className="h-6 w-full bg-slate-800 rounded-lg overflow-hidden flex p-1 gap-1">
          <div
            style={{ width: `${netPct}%` }}
            className="bg-emerald-500 rounded-md h-full transition-all duration-500 flex items-center justify-center text-[10px] font-extrabold text-slate-950"
            title={`Net Distribution: ${netPct}%`}
          >
            {netPct > 12 && `${netPct}% Net`}
          </div>

          <div
            style={{ width: `${mgmtPct}%` }}
            className="bg-amber-500 rounded-md h-full transition-all duration-500 flex items-center justify-center text-[10px] font-extrabold text-slate-950"
            title={`PM Fee: ${mgmtPct}%`}
          >
            {mgmtPct > 5 && `${mgmtPct}%`}
          </div>

          <div
            style={{ width: `${reservePct}%` }}
            className="bg-purple-500 rounded-md h-full transition-all duration-500 flex items-center justify-center text-[10px] font-extrabold text-slate-950"
            title={`Reserve: ${reservePct}%`}
          >
            {reservePct > 5 && `${reservePct}%`}
          </div>

          {maintPct > 0 && (
            <div
              style={{ width: `${maintPct}%` }}
              className="bg-rose-500 rounded-md h-full transition-all duration-500 flex items-center justify-center text-[10px] font-extrabold text-white"
              title={`Maintenance Deductions: ${maintPct}%`}
            >
              {maintPct > 5 && `${maintPct}%`}
            </div>
          )}
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-4 text-[11px] text-slate-400 pt-1">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
            <span>Net Owner Distribution</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span>
            <span>Management Fee ({selectedRecord.management_fee_pct * 100}%)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-purple-500 inline-block"></span>
            <span>Reserve Fund Escrow</span>
          </div>
          {selectedRecord.maintenance_deductions > 0 && (
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span>
              <span>Maintenance Deductions (-${selectedRecord.maintenance_deductions})</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
