"use client";

import { useEffect, useState } from "react";

export default function FinancialsPage() {
  const [financials, setFinancials] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/financials")
      .then((res) => res.json())
      .then((data) => {
        setFinancials(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load financials:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          💼 Portfolio Financial Accounting
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          PropFlow PM OS — Real-Time Rent Roll, Management Fee Splits & Net Distributions
        </p>
      </div>

      {loading ? (
        <div className="p-8 bg-white rounded-2xl border border-slate-200 text-center text-slate-400 text-sm animate-pulse">
          Loading property financial ledgers...
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <table className="w-full text-xs text-left border-collapse">
            <thead>
              <tr className="bg-slate-100 border-b border-slate-200 text-slate-700 font-bold uppercase text-[10px] tracking-wider">
                <th className="p-4">Owner Name</th>
                <th className="p-4">Property Address</th>
                <th className="p-4">Gross Rent</th>
                <th className="p-4">Mgmt Fee</th>
                <th className="p-4">Reserve Fund</th>
                <th className="p-4">Maintenance</th>
                <th className="p-4">Net Distribution</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
              {financials.map((f) => (
                <tr key={f.id} className="hover:bg-slate-50 transition-colors">
                  <td className="p-4 font-sans font-bold text-slate-900">{f.owner_name}</td>
                  <td className="p-4 font-sans text-slate-600">{f.property_address}</td>
                  <td className="p-4 text-emerald-700 font-extrabold">${f.gross_rent?.toLocaleString()}</td>
                  <td className="p-4 text-slate-500">${f.management_fee_amount?.toLocaleString()}</td>
                  <td className="p-4 text-slate-500">${f.reserve_fund_amount?.toLocaleString()}</td>
                  <td className="p-4 text-rose-600">${f.maintenance_deductions?.toLocaleString()}</td>
                  <td className="p-4 text-blue-700 font-black">${f.net_distribution?.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
