"use client";

import { useEffect, useState } from "react";
import FinancialCharts from "@/components/FinancialCharts";

export default function OwnerPortal() {
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
        console.error("Failed to fetch financial data:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          📈 Property Owner Portal
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Apex Lone Star Holdings LLC — Monthly Revenue Statements & Reserve Capital Allocation
        </p>
      </div>

      {loading ? (
        <div className="p-8 bg-white rounded-2xl border border-slate-200 text-center text-slate-400 text-sm animate-pulse">
          Loading property financial statements...
        </div>
      ) : (
        <>
          {/* Revenue Analytics & Interactive Visual Charts */}
          <FinancialCharts records={financials} />

          {/* Statement Table */}
          <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
            <div className="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
              <h3 className="font-bold text-slate-800 text-sm uppercase tracking-wider">
                Detailed Statement Statements
              </h3>
              <span className="text-xs bg-emerald-100 text-emerald-800 font-bold px-2.5 py-1 rounded-full">
                {financials.length} Properties Active
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-600">
                <thead className="bg-slate-100 text-slate-500 uppercase text-[10px] font-bold">
                  <tr>
                    <th className="px-4 py-3">Property Address</th>
                    <th className="px-4 py-3">Period</th>
                    <th className="px-4 py-3 text-right">Gross Rent</th>
                    <th className="px-4 py-3 text-right">PM Fee</th>
                    <th className="px-4 py-3 text-right">Reserve Fund</th>
                    <th className="px-4 py-3 text-right">Maintenance</th>
                    <th className="px-4 py-3 text-right text-emerald-700 font-bold">Net Distribution</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-medium">
                  {financials.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="px-4 py-3 font-semibold text-slate-900">{item.property_address}</td>
                      <td className="px-4 py-3 text-slate-500">{item.month_year}</td>
                      <td className="px-4 py-3 text-right font-mono text-slate-900">${item.gross_rent.toLocaleString()}</td>
                      <td className="px-4 py-3 text-right font-mono text-amber-600">-${item.management_fee_amount.toLocaleString()}</td>
                      <td className="px-4 py-3 text-right font-mono text-purple-600">-${item.reserve_fund_amount.toLocaleString()}</td>
                      <td className="px-4 py-3 text-right font-mono text-rose-600">-${item.maintenance_deductions.toLocaleString()}</td>
                      <td className="px-4 py-3 text-right font-mono font-bold text-emerald-600">${item.net_distribution.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
