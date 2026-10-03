import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { KPICard } from '../components/dashboard/KPICard';
import { ChartWidget } from '../components/dashboard/ChartWidget';
import { KPI, Widget, Dashboard } from '../types';
import { Sparkles, Filter, RefreshCw, Layers } from 'lucide-react';

export const DashboardBuilder: React.FC = () => {
  const { activeDataset } = useAuth();
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [kpis, setKpis] = useState<KPI[]>([]);
  const [widgets, setWidgets] = useState<Widget[]>([]);
  const [filters, setFilters] = useState<any[]>([]);
  const [selectedRegion, setSelectedRegion] = useState<string>('All');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [loading, setLoading] = useState(false);

  const fetchDashboardSpecs = () => {
    if (!activeDataset) return;
    setLoading(true);
    api.post(`/dashboards/generate/${activeDataset.id}`)
      .then((res) => {
        setDashboard(res.data);
        const config = res.data.layout_config || {};
        setKpis(config.kpis || []);
        setWidgets(config.widgets || []);
        setFilters(config.filters || []);
      })
      .catch((err) => console.error('Failed to generate dashboard:', err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDashboardSpecs();
  }, [activeDataset]);

  if (!activeDataset) {
    return <p className="text-slate-400 text-sm">Please select a dataset from the top navigation bar.</p>;
  }

  // Filter widget data client-side dynamically
  const getFilteredWidgets = () => {
    return widgets.map((w) => {
      if (w.type === 'kpi_cards' || !Array.isArray(w.data)) return w;
      
      let filteredData = [...w.data];
      if (selectedRegion !== 'All' && w.data[0]?.region) {
        filteredData = filteredData.filter((item) => item.region === selectedRegion);
      }
      if (selectedCategory !== 'All' && w.data[0]?.category) {
        filteredData = filteredData.filter((item) => item.category === selectedCategory);
      }
      return { ...w, data: filteredData };
    });
  };

  const activeWidgets = getFilteredWidgets();

  return (
    <div className="space-y-6">
      {/* Header & AI Auto Generate Button */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Interactive Dashboard Studio</h1>
          <p className="text-xs text-slate-400 mt-1">
            Automated chart dimension selection & dynamic visualization engine for dataset <span className="text-slate-200 font-semibold">{activeDataset.name}</span>
          </p>
        </div>

        <button
          onClick={fetchDashboardSpecs}
          disabled={loading}
          className="flex items-center space-x-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 transition-all cursor-pointer"
        >
          <Sparkles className="w-4 h-4" />
          <span>{loading ? 'Generating...' : 'Generate Dashboard with AI'}</span>
        </button>
      </div>

      {/* Dynamic Filter Bar */}
      <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-4 flex flex-wrap items-center gap-4 text-xs">
        <div className="flex items-center space-x-2 text-slate-300 font-bold">
          <Filter className="w-4 h-4 text-blue-400" />
          <span>Dynamic Dashboard Filters:</span>
        </div>

        {/* Region Filter */}
        <div className="flex items-center space-x-2 bg-slate-900/70 px-3 py-1.5 rounded-lg border border-slate-700">
          <span className="text-slate-400">Region:</span>
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="bg-transparent text-slate-100 font-semibold focus:outline-none cursor-pointer"
          >
            <option value="All" className="bg-slate-900">All Regions</option>
            {filters.find(f => f.id === 'region')?.options?.map((r: string) => (
              <option key={r} value={r} className="bg-slate-900">{r}</option>
            ))}
          </select>
        </div>

        {/* Category Filter */}
        <div className="flex items-center space-x-2 bg-slate-900/70 px-3 py-1.5 rounded-lg border border-slate-700">
          <span className="text-slate-400">Category:</span>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="bg-transparent text-slate-100 font-semibold focus:outline-none cursor-pointer"
          >
            <option value="All" className="bg-slate-900">All Categories</option>
            {filters.find(f => f.id === 'category')?.options?.map((c: string) => (
              <option key={c} value={c} className="bg-slate-900">{c}</option>
            ))}
          </select>
        </div>

        {(selectedRegion !== 'All' || selectedCategory !== 'All') && (
          <button
            onClick={() => { setSelectedRegion('All'); setSelectedCategory('All'); }}
            className="text-xs text-blue-400 hover:text-blue-300 underline font-semibold cursor-pointer"
          >
            Reset Filters
          </button>
        )}
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi) => (
          <KPICard key={kpi.id} kpi={kpi} />
        ))}
      </div>

      {/* Customizable Widget Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {activeWidgets.slice(1).map((w, idx) => (
          <div key={w.id} className={idx % 3 === 0 ? "lg:col-span-8" : "lg:col-span-4"}>
            <ChartWidget widget={w} />
          </div>
        ))}
      </div>
    </div>
  );
};
