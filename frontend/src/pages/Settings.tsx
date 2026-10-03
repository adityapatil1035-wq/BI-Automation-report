import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Settings as SettingsIcon, Shield, Server, Mail, Key } from 'lucide-react';

export const Settings: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white">System & Workspace Settings</h1>
        <p className="text-xs text-slate-400 mt-1">
          Manage workspace profile, database integration, SMTP email service parameters, and AI API keys.
        </p>
      </div>

      <div className="space-y-6">
        {/* User & Workspace Profile */}
        <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl space-y-4">
          <div className="flex items-center space-x-2 text-blue-400 text-xs font-bold uppercase tracking-wider border-b border-slate-700/60 pb-3">
            <Shield className="w-4 h-4" />
            <span>Workspace Profile & User Role</span>
          </div>

          <div className="grid grid-cols-2 gap-4 text-xs">
            <div>
              <span className="text-slate-400 font-semibold">User Email</span>
              <p className="text-sm font-bold text-white mt-1">{user?.email || 'admin@acme.com'}</p>
            </div>
            <div>
              <span className="text-slate-400 font-semibold">Assigned Role</span>
              <p className="text-sm font-bold text-blue-400 mt-1">{user?.role || 'Admin'}</p>
            </div>
          </div>
        </div>

        {/* AI Layer Config */}
        <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl space-y-4">
          <div className="flex items-center space-x-2 text-indigo-400 text-xs font-bold uppercase tracking-wider border-b border-slate-700/60 pb-3">
            <Key className="w-4 h-4" />
            <span>AI Insight Engine Provider Configuration</span>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block font-bold text-slate-200 mb-1">OpenAI API Key (Optional)</label>
              <input
                type="password"
                placeholder="sk-..."
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
              />
              <p className="text-[11px] text-slate-400 mt-1">
                If omitted, the platform uses its statistical ground-truth insight engine automatically.
              </p>
            </div>
          </div>
        </div>

        {/* Database & SMTP Integration Status */}
        <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl space-y-4">
          <div className="flex items-center space-x-2 text-emerald-400 text-xs font-bold uppercase tracking-wider border-b border-slate-700/60 pb-3">
            <Server className="w-4 h-4" />
            <span>Database & Infrastructure Health</span>
          </div>

          <div className="space-y-2 text-xs">
            <div className="flex justify-between items-center bg-slate-900/60 p-3 rounded-lg border border-slate-700/60">
              <span className="font-semibold text-slate-300">Database Engine</span>
              <span className="text-emerald-400 font-bold">SQLAlchemy / SQLite (PostgreSQL Ready)</span>
            </div>
            <div className="flex justify-between items-center bg-slate-900/60 p-3 rounded-lg border border-slate-700/60">
              <span className="font-semibold text-slate-300">Background Job Scheduler</span>
              <span className="text-emerald-400 font-bold">APScheduler Background Service (Running)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
