"use client";

import { useEffect, useState } from "react";

export default function TenantPortal() {
  const [lease, setLease] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [paymentSuccess, setPaymentSuccess] = useState<any>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/tenant/lease")
      .then((res) => res.json())
      .then((data) => {
        setLease(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load lease info:", err);
        setLoading(false);
      });
  }, []);

  const handlePayRent = async () => {
    setIsProcessing(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/tenant/pay-rent?amount=${lease.monthly_rent}`, {
        method: "POST",
      });
      const data = await res.json();
      setPaymentSuccess(data);
    } catch (err) {
      console.error("Payment failed:", err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          🏡 Tenant Self-Service Portal
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          PropFlow PM OS — Lease Overview, Maintenance & Auto-Pay Management
        </p>
      </div>

      {loading ? (
        <div className="p-8 bg-white rounded-2xl border border-slate-200 text-center text-slate-400 text-sm animate-pulse">
          Loading lease account metrics...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
          {/* Main Lease & Payment Card */}
          <div className="md:col-span-7 bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
            <div className="flex justify-between items-start border-b border-slate-100 pb-4">
              <div>
                <h2 className="text-xl font-bold text-slate-900">{lease.tenant_name}</h2>
                <p className="text-xs text-slate-500 mt-0.5">{lease.property_address} ({lease.unit})</p>
              </div>
              <span className="bg-emerald-100 text-emerald-800 text-xs font-extrabold px-3 py-1 rounded-full">
                {lease.payment_status}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-4 text-xs">
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                <p className="text-slate-400 font-semibold">Monthly Rent</p>
                <p className="text-2xl font-extrabold text-slate-900 mt-1">${lease.monthly_rent.toLocaleString()}</p>
              </div>
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                <p className="text-slate-400 font-semibold">Next Due Date</p>
                <p className="text-2xl font-extrabold text-slate-900 mt-1">{lease.next_due_date}</p>
              </div>
            </div>

            {paymentSuccess ? (
              <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl space-y-1">
                <p className="text-xs font-bold text-emerald-900">🎉 Rent Payment Processed Successfully!</p>
                <p className="text-[11px] text-emerald-700">Transaction ID: {paymentSuccess.transaction_id}</p>
                <p className="text-[11px] text-emerald-700">Method: {paymentSuccess.payment_method}</p>
              </div>
            ) : (
              <button
                onClick={handlePayRent}
                disabled={isProcessing}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs py-3.5 rounded-xl transition-colors shadow-sm flex justify-center items-center gap-2"
              >
                {isProcessing ? "Processing ACH Transfer..." : `💳 Pay September Rent ($${lease.monthly_rent.toLocaleString()})`}
              </button>
            )}
          </div>

          {/* Lease Info & Settings */}
          <div className="md:col-span-5 space-y-6">
            <div className="bg-slate-900 text-white p-6 rounded-2xl border border-slate-800 space-y-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                📜 Lease Document Details
              </h3>
              <div className="space-y-2 text-xs text-slate-300">
                <div className="flex justify-between">
                  <span>Start Date:</span>
                  <span className="font-semibold text-white">{lease.lease_start}</span>
                </div>
                <div className="flex justify-between">
                  <span>End Date:</span>
                  <span className="font-semibold text-white">{lease.lease_end}</span>
                </div>
                <div className="flex justify-between">
                  <span>Security Deposit Held:</span>
                  <span className="font-semibold text-white">${lease.security_deposit.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span>Auto-Pay Status:</span>
                  <span className="text-emerald-400 font-bold">{lease.auto_pay ? "ACTIVE" : "INACTIVE"}</span>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 space-y-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900">
                🛠️ Submit Urgent Maintenance Request
              </h3>
              <p className="text-xs text-slate-500">
                Need a repair? Submitting a ticket automatically dispatches our assigned contractor network.
              </p>
              <a
                href="/work-orders"
                className="block text-center bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs py-2.5 rounded-xl transition-colors"
              >
                Go to Work Order Center
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
