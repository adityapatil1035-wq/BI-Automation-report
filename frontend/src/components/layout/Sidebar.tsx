import React from 'react';
import { 
  LayoutDashboard, 
  UploadCloud, 
  Sparkles, 
  BarChart3, 
  TrendingUp, 
  FileText, 
  CalendarClock, 
  Settings, 
  ShieldCheck, 
  HelpCircle,
  Activity
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'executive', label: 'Executive Dashboard', icon: LayoutDashboard },
    { id: 'upload', label: 'Upload Data & Sources', icon: UploadCloud },
    { id: 'quality', label: 'Data Quality & Cleaning', icon: ShieldCheck },
    { id: 'builder', label: 'Dashboard Generator', icon: BarChart3 },
    { id: 'insights', label: 'AI Business Insights', icon: Sparkles },
    { id: 'anomalies', label: 'Anomaly Detection', icon: Activity },
    { id: 'ask', label: 'Ask Your Data (NL)', icon: HelpCircle },
    { id: 'forecasting', label: 'Forecasting Studio', icon: TrendingUp },
    { id: 'reports', label: 'Report Generator', icon: FileText },
    { id: 'scheduler', label: 'Report Scheduler', icon: CalendarClock },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between shrink-0 h-screen sticky top-0">
      <div>
        {/* SaaS Logo */}
        <div className="h-16 px-6 flex items-center space-x-3 border-b border-slate-800">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-white tracking-wide">AUTO BI PLATFORM</h1>
            <p className="text-[10px] text-slate-400 font-medium">Enterprise Intelligence AI</p>
          </div>
        </div>

        {/* Menu Navigation */}
        <nav className="p-4 space-y-1.5 overflow-y-auto max-h-[calc(100vh-140px)]">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  isActive
                    ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Pro Badge */}
      <div className="p-4 border-t border-slate-800/80">
        <div className="bg-slate-800/60 rounded-lg p-3 border border-slate-700/50">
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-xs font-bold text-slate-200">System Online</span>
          </div>
          <p className="text-[10px] text-slate-400 mt-1">Automated Analytics Engine v1.0</p>
        </div>
      </div>
    </aside>
  );
};
