'use client';

import { useState } from 'react';

export default function WorkOrderManager() {
  const [tenantId, setTenantId] = useState('t_101');
  const [description, setDescription] = useState('Leaking kitchen sink pipe');
  const [category, setCategory] = useState('plumbing');
  const [order, setOrder] = useState<any>(null);

  const submitTicket = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/maintenance/work-orders?tenant_id=${tenantId}&description=${encodeURIComponent(description)}&category=${category}`, {
        method: 'POST'
      });
      const data = await res.json();
      setOrder(data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
      <h2 className="text-lg font-bold text-slate-900">Maintenance Work Orders</h2>
      <div className="space-y-3">
        <div>
          <label className="text-xs font-semibold text-slate-500">Category</label>
          <select className="w-full mt-1 p-2 border rounded-md text-sm" value={category} onChange={(e) => setCategory(e.target.value)}>
            <option value="plumbing">Plumbing</option>
            <option value="electrical">Electrical</option>
            <option value="hvac">HVAC / Heating</option>
            <option value="general">General Repairs</option>
          </select>
        </div>
        <div>
          <label className="text-xs font-semibold text-slate-500">Issue Description</label>
          <textarea className="w-full mt-1 p-2 border rounded-md text-sm" rows={2} value={description} onChange={(e) => setDescription(e.target.value)} />
        </div>
      </div>
      <button onClick={submitTicket} className="w-full py-2 bg-emerald-600 text-white font-semibold text-sm rounded-md hover:bg-emerald-700">
        Submit Maintenance Ticket
      </button>
      {order && (
        <div className="p-4 bg-slate-50 rounded-lg border text-sm space-y-1">
          <p><span className="font-medium text-slate-600">Ticket ID:</span> <span className="font-mono">{order.order_id}</span></p>
          <p><span className="font-medium text-slate-600">Urgency Level:</span> <strong className={order.urgency === 'HIGH' ? 'text-red-600' : 'text-blue-600'}>{order.urgency}</strong></p>
        </div>
      )}
    </div>
  );
}
