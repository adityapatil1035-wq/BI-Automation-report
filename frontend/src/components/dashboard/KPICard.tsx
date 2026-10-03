import React from 'react';
import { KPI } from '../../types';
import { TrendingUp, TrendingDown, DollarSign, Activity, AlertTriangle } from 'lucide-react';

export const KPICard: React.FC<{ kpi: KPI }> = ({ kpi }) => {
  const isPositive = kpi.status === 'positive';
  const isWarning = kpi.status === 'warning';

  return (
    <div className="bg-slate-800/80 border border-slate-700/80 hover:border-blue-500/40 transition-all rounded-xl p-5 shadow-lg relative overflow-hidden group">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{kpi.name}</p>
          <h3 className="text-2xl font-bold text-white mt-1 tracking-tight">{kpi.value}</h3>
        </div>
        <div className={`p-2.5 rounded-lg ${
          isPositive ? 'bg-emerald-500/10 text-emerald-400' : isWarning ? 'bg-amber-500/10 text-amber-400' : 'bg-blue-500/10 text-blue-400'
        }`}>
          {isPositive ? <TrendingUp className="w-5 h-5" /> : isWarning ? <AlertTriangle className="w-5 h-5" /> : <Activity className="w-5 h-5" />}
        </div>
      </div>
      
      <div className="mt-3 flex items-center justify-between text-xs">
        <span className={`font-semibold flex items-center gap-1 ${
          isPositive ? 'text-emerald-400' : 'text-slate-400'
        }`}>
          {kpi.trend} <span className="text-[10px] text-slate-400 font-normal">vs prev period</span>
        </span>
        <span className="text-[10px] text-slate-400 font-medium capitalize bg-slate-700/50 px-2 py-0.5 rounded">
          {kpi.unit}
        </span>
      </div>
    </div>
  );
};
