'use client';

import { useState } from 'react';

export default function LeadScoringPanel() {
  const [income, setIncome] = useState(9000);
  const [rent, setRent] = useState(2500);
  const [credit, setCredit] = useState(720);
  const [lead, setLead] = useState<any>(null);

  const evaluateApplicant = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/leads/score?income=${income}&rent=${rent}&credit_score=${credit}`, {
        method: 'POST'
      });
      const data = await res.json();
      setLead(data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
      <h2 className="text-lg font-bold text-slate-900">Lead Qualification Scoring</h2>
      <div className="grid grid-cols-3 gap-3">
        <div>
          <label className="text-xs font-semibold text-slate-500">Monthly Income ($)</label>
          <input type="number" className="w-full mt-1 p-2 border rounded-md text-sm" value={income} onChange={(e) => setIncome(Number(e.target.value))} />
        </div>
        <div>
          <label className="text-xs font-semibold text-slate-500">Target Rent ($)</label>
          <input type="number" className="w-full mt-1 p-2 border rounded-md text-sm" value={rent} onChange={(e) => setRent(Number(e.target.value))} />
        </div>
        <div>
          <label className="text-xs font-semibold text-slate-500">Credit Score</label>
          <input type="number" className="w-full mt-1 p-2 border rounded-md text-sm" value={credit} onChange={(e) => setCredit(Number(e.target.value))} />
        </div>
      </div>
      <button onClick={evaluateApplicant} className="w-full py-2 bg-blue-600 text-white font-semibold text-sm rounded-md hover:bg-blue-700">
        Evaluate Applicant
      </button>
      {lead && (
        <div className="p-4 bg-slate-50 rounded-lg border text-sm space-y-1">
          <p><span className="font-medium text-slate-600">Qualification Score:</span> <strong className="text-indigo-600">{lead.lead_score} / 100</strong></p>
          <p><span className="font-medium text-slate-600">Tier:</span> <span className="px-2 py-0.5 rounded text-xs font-bold bg-emerald-100 text-emerald-800">{lead.qualification_tier}</span></p>
        </div>
      )}
    </div>
  );
}
