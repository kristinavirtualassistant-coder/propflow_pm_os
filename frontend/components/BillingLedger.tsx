'use client';

import { useState } from 'react';

export default function BillingLedger() {
  const [tenantId, setTenantId] = useState('t_101');
  const [baseRent, setBaseRent] = useState(2500);
  const [daysLate, setDaysLate] = useState(6);
  const [result, setResult] = useState<any>(null);

  const calculateBalance = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/billing/balance?tenant_id=${tenantId}&base_rent=${baseRent}&days_late=${daysLate}`);
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
      <h2 className="text-lg font-bold text-slate-900">Tenant Rent Ledger & Late Fees</h2>
      <div className="grid grid-cols-3 gap-3">
        <div>
          <label className="text-xs font-semibold text-slate-500">Tenant ID</label>
          <input className="w-full mt-1 p-2 border rounded-md text-sm" value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
        </div>
        <div>
          <label className="text-xs font-semibold text-slate-500">Base Rent ($)</label>
          <input type="number" className="w-full mt-1 p-2 border rounded-md text-sm" value={baseRent} onChange={(e) => setBaseRent(Number(e.target.value))} />
        </div>
        <div>
          <label className="text-xs font-semibold text-slate-500">Days Overdue</label>
          <input type="number" className="w-full mt-1 p-2 border rounded-md text-sm" value={daysLate} onChange={(e) => setDaysLate(Number(e.target.value))} />
        </div>
      </div>
      <button onClick={calculateBalance} className="w-full py-2 bg-indigo-600 text-white font-semibold text-sm rounded-md hover:bg-indigo-700">
        Calculate Total Due
      </button>
      {result && (
        <div className="p-4 bg-slate-50 rounded-lg border text-sm space-y-1">
          <p><span className="font-medium text-slate-600">Late Fee:</span> <strong className="text-amber-600">${result.late_fee}</strong></p>
          <p><span className="font-medium text-slate-600">Total Outstanding:</span> <strong className="text-slate-900">${result.total_due}</strong></p>
          <p><span className="font-medium text-slate-600">Account Status:</span> <span className="px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-800">{result.status}</span></p>
        </div>
      )}
    </div>
  );
}
