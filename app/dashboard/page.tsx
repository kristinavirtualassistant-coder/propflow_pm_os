'use client';

import BillingLedger from '@/frontend/components/BillingLedger';
import WorkOrderManager from '@/frontend/components/WorkOrderManager';
import LeadScoringPanel from '@/frontend/components/LeadScoringPanel';

export default function OperationsDashboard() {
  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">PropFlow Operations Center</h1>
        <p className="text-slate-500 text-sm mt-1">Live management suite for rent billing, maintenance dispatch, and applicant screening.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <BillingLedger />
        <WorkOrderManager />
      </div>

      <LeadScoringPanel />
    </div>
  );
}
