import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PropFlow PM OS — Property Management Operating System",
  description: "Billion-Dollar Scale Property Management Automation Operating System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-slate-50 text-slate-900 min-h-screen flex flex-col`}>
        {/* Top Operational Bar */}
        <div className="bg-slate-900 text-slate-300 text-[11px] px-8 py-2 flex justify-between items-center border-b border-slate-800 font-mono">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5 text-emerald-400 font-semibold">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
              PropFlow API: ONLINE
            </span>
            <span className="text-slate-600">|</span>
            <span>SQLite Trust Database (propflow.db)</span>
          </div>
          <div className="flex items-center gap-4">
            <span>Auto-Backup: Every 6h</span>
            <span className="text-slate-600">|</span>
            <span className="text-slate-400 font-sans">State of Texas Compliant</span>
          </div>
        </div>

        {/* Primary Navigation Header */}
        <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
          <div className="max-w-7xl mx-auto px-8 h-16 flex justify-between items-center">
            <Link href="/analytics" className="flex items-center gap-2 text-slate-950 font-black text-xl tracking-tight">
              <span className="bg-blue-600 text-white px-2 py-0.5 rounded-lg text-lg">P</span>
              PropFlow <span className="text-blue-600 text-xs uppercase tracking-widest font-bold font-mono">PM OS</span>
            </Link>

            <nav className="flex items-center gap-1 text-xs font-semibold text-slate-600">
              <Link href="/analytics" className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors">
                📈 Analytics
              </Link>
              <Link href="/leads" className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors">
                🎯 Acquisitions
              </Link>
              <Link href="/work-orders" className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors">
                🛠️ Maintenance
              </Link>
              <Link href="/financials" className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors">
                💼 Financials
              </Link>
              <Link href="/owner-statement" className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors">
                📊 Owner Statement
              </Link>
              <Link href="/lease-generator" className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors">
                📜 Lease Generator
              </Link>
              <Link href="/tenant" className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors">
                🏡 Tenant
              </Link>
              <Link href="/audit-logs" className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors">
                📜 Audit Logs
              </Link>
              <Link href="/settings" className="px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors">
                ⚙️ Settings
              </Link>
            </nav>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1">{children}</main>

        {/* System Footer */}
        <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500 font-mono">
          <div className="max-w-7xl mx-auto px-8 flex justify-between items-center">
            <p>PropFlow PM OS © 2026 — Enterprise Property Automation Platform</p>
            <p className="text-slate-400">FastAPI • Next.js 14 • SQLAlchemy • SQLite</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
