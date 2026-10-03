import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { Database, ShieldCheck, Sparkles } from 'lucide-react';

interface NavbarProps {
  onOpenNLQuery: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpenNLQuery }) => {
  const { user, activeDataset, datasets, setActiveDataset } = useAuth();

  return (
    <header className="h-16 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-6 flex items-center justify-between sticky top-0 z-30">
      {/* Active Dataset Selector */}
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 bg-slate-800/80 border border-slate-700/80 rounded-lg px-3 py-1.5 text-sm">
          <Database className="w-4 h-4 text-blue-400" />
          <span className="text-slate-400 font-medium text-xs">Dataset:</span>
          <select
            value={activeDataset?.id || ''}
            onChange={(e) => {
              const ds = datasets.find(d => d.id === Number(e.target.value));
              if (ds) setActiveDataset(ds);
            }}
            className="bg-transparent text-slate-100 font-semibold focus:outline-none text-sm cursor-pointer"
          >
            {datasets.map(d => (
              <option key={d.id} value={d.id} className="bg-slate-900 text-slate-100">
                {d.name} ({d.row_count} rows)
              </option>
            ))}
          </select>
        </div>

        {activeDataset && (
          <div className="hidden md:flex items-center space-x-2">
            <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
              Domain: {activeDataset.domain}
            </span>
            <span className={`px-2.5 py-1 rounded-md text-xs font-semibold flex items-center gap-1 border ${
              activeDataset.data_quality_score >= 90 
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
            }`}>
              <ShieldCheck className="w-3.5 h-3.5" /> Quality: {activeDataset.data_quality_score}%
            </span>
          </div>
        )}
      </div>

      {/* Right Action Controls */}
      <div className="flex items-center space-x-4">
        <button
          onClick={onOpenNLQuery}
          className="flex items-center space-x-2 px-3.5 py-1.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-blue-500/20 transition-all cursor-pointer"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Ask Your Data</span>
        </button>

        {/* User Profile */}
        <div className="flex items-center space-x-2 bg-slate-800/80 border border-slate-700/80 rounded-lg px-3 py-1.5">
          <div className="w-6 h-6 rounded-full bg-blue-500/20 border border-blue-500/40 flex items-center justify-center font-bold text-blue-400 text-[11px]">
            {user?.full_name?.charAt(0) || 'A'}
          </div>
          <span className="hidden sm:inline font-medium text-xs text-slate-200">{user?.full_name || 'Admin User'}</span>
        </div>
      </div>
    </header>
  );
};
