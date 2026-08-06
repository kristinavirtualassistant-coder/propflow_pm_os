"use client";

import { useState, useEffect } from "react";

interface LineItem {
  property_address: string;
  gross_rent: number;
  mgmt_fee: number;
  reserve_fund: number;
  maintenance: number;
  net: number;
}

interface StatementData {
  statement_period: string;
  owner_name: string;
  properties_count: number;
  total_gross_rent: number;
  total_management_fees: number;
  total_reserve_funds: number;
  total_maintenance_deductions: number;
  net_owner_distribution: number;
  line_items: LineItem[];
}

export default function OwnerStatementPage() {
  const [selectedOwner, setSelectedOwner] = useState("John Doe");
  const [statement, setStatement] = useState<StatementData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStatement() {
      setLoading(true);
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/v1/financials/owner-statement/${encodeURIComponent(selectedOwner)}`);
        const data = await res.json();
        setStatement(data);
      } catch (err) {
        console.error("Failed to fetch statement", err);
      } finally {
        setLoading(false);
      }
    }
    fetchStatement();
  }, [selectedOwner]);

  const pdfDownloadUrl = `http://127.0.0.1:8000/api/v1/financials/owner-statement/${encodeURIComponent(selectedOwner)}/download-pdf`;

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      {/* Page Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            💼 Owner Statement & Distribution Ledger
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            PropFlow PM OS — Automated Financial Statements & PDF Payout Exporter
          </p>
        </div>

        <div className="flex gap-3">
          <select
            value={selectedOwner}
            onChange={(e) => setSelectedOwner(e.target.value)}
            className="bg-white border border-slate-300 rounded-xl px-4 py-2 text-xs font-semibold text-slate-800 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="John Doe">Owner: John Doe</option>
            <option value="Jane Smith">Owner: Jane Smith</option>
            <option value="Austin Investments LLC">Owner: Austin Investments LLC</option>
          </select>

          <a
            href={pdfDownloadUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs px-5 py-2.5 rounded-xl transition-all shadow-md flex items-center gap-2"
          >
            📄 Download Official Statement PDF
          </a>
        </div>
      </div>

      {loading || !statement ? (
        <div className="p-12 text-center text-slate-400 font-semibold">Loading statement data...</div>
      ) : (
        <>
          {/* Top Financial Breakdown Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Gross Rent Collected</span>
              <span className="text-2xl font-black text-slate-900 mt-1 block">${statement.total_gross_rent.toLocaleString()}</span>
              <span className="text-xs text-emerald-600 font-medium mt-1 block">Period: {statement.statement_period}</span>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Management Fees (10%)</span>
              <span className="text-2xl font-black text-rose-600 mt-1 block">-${statement.total_management_fees.toLocaleString()}</span>
              <span className="text-xs text-slate-400 font-medium mt-1 block">Auto-deducted</span>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Maintenance & Reserve</span>
              <span className="text-2xl font-black text-amber-600 mt-1 block">
                -${(statement.total_reserve_funds + statement.total_maintenance_deductions).toLocaleString()}
              </span>
              <span className="text-xs text-slate-400 font-medium mt-1 block">Reserves & work orders</span>
            </div>

            <div className="bg-emerald-50 p-5 rounded-2xl border border-emerald-200 shadow-sm">
              <span className="text-xs font-bold text-emerald-700 uppercase tracking-wider block">Net Owner Disbursement</span>
              <span className="text-2xl font-black text-emerald-700 mt-1 block">${statement.net_owner_distribution.toLocaleString()}</span>
              <span className="text-xs text-emerald-800 font-medium mt-1 block">ACH Direct Deposit Ready</span>
            </div>
          </div>

          {/* Detailed Property Line Items Table */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="p-5 border-b border-slate-100 flex justify-between items-center">
              <h2 className="text-sm font-bold text-slate-900">
                Property Distribution Breakdown ({statement.properties_count} Properties)
              </h2>
              <span className="text-xs font-medium text-slate-500">Owner: {statement.owner_name}</span>
            </div>

            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 font-semibold uppercase border-b border-slate-100">
                <tr>
                  <th className="p-4">Property Address</th>
                  <th className="p-4">Gross Rent</th>
                  <th className="p-4">Mgmt Fee</th>
                  <th className="p-4">Reserve Fund</th>
                  <th className="p-4">Maintenance</th>
                  <th className="p-4 text-right">Net Payout</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium text-slate-800">
                {statement.line_items.map((item, i) => (
                  <tr key={i} className="hover:bg-slate-50 transition-colors">
                    <td className="p-4 font-bold text-slate-900">{item.property_address}</td>
                    <td className="p-4 text-slate-700">${item.gross_rent.toLocaleString()}</td>
                    <td className="p-4 text-rose-600">-${item.mgmt_fee.toLocaleString()}</td>
                    <td className="p-4 text-amber-600">-${item.reserve_fund.toLocaleString()}</td>
                    <td className="p-4 text-slate-600">-${item.maintenance.toLocaleString()}</td>
                    <td className="p-4 text-right font-bold text-emerald-600">${item.net.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
