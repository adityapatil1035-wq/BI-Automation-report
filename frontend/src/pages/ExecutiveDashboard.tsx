import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { KPICard } from '../components/dashboard/KPICard';
import { ChartWidget } from '../components/dashboard/ChartWidget';
import { KPI, Widget, Insight, Anomaly } from '../types';
import { Sparkles, FileText, FileSpreadsheet, TrendingUp, AlertOctagon, Layers } from 'lucide-react';

export const ExecutiveDashboard: React.FC = () => {
  const { activeDataset } = useAuth();
  const [kpis, setKpis] = useState<KPI[]>([]);
  const [widgets, setWidgets] = useState<Widget[]>([]);
  const [insights, setInsights] = useState<Insight[]>([]);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    if (activeDataset) {
      setLoading(true);
      Promise.all([
        api.get(`/analytics/${activeDataset.id}/kpis`),
        api.get(`/dashboards/generate/${activeDataset.id}`),
        api.get(`/analytics/${activeDataset.id}/insights`),
        api.get(`/analytics/${activeDataset.id}/anomalies`),
      ])
        .then(([kpiRes, dashRes, insRes, anomRes]) => {
          setKpis(kpiRes.data.kpis || []);
          setWidgets(dashRes.data.layout_config?.widgets || []);
          setInsights(insRes.data || []);
          setAnomalies(anomRes.data || []);
        })
        .catch((err) => console.error('Failed to load executive dashboard:', err))
        .finally(() => setLoading(false));
    }
  }, [activeDataset]);

  const handleExportPDF = async () => {
    if (!activeDataset) return;
    setExporting(true);
    try {
      const res = await api.post(`/reports/generate-pdf/${activeDataset.id}`);
      window.open(res.data.download_url, '_blank');
    } catch (err) {
      alert('Failed to generate PDF report');
    } finally {
      setExporting(false);
    }
  };

  const handleExportExcel = async () => {
    if (!activeDataset) return;
    setExporting(true);
    try {
      const res = await api.post(`/reports/generate-excel/${activeDataset.id}`);
      window.open(res.data.download_url, '_blank');
    } catch (err) {
      alert('Failed to generate Excel report');
    } finally {
      setExporting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 space-y-4">
        <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-medium text-slate-400">Analyzing dataset and synthesizing executive dashboard...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header & Quick Action Export */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500 animate-pulse"></span>
            <span className="text-xs font-bold text-blue-400 uppercase tracking-widest">Executive C-Suite Overview</span>
          </div>
          <h1 className="text-2xl font-bold text-white mt-1">
            {activeDataset?.domain || 'Sales'} Intelligence Dashboard
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Automated BI report for dataset <span className="text-slate-200 font-semibold">{activeDataset?.name}</span> ({activeDataset?.row_count} records)
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleExportPDF}
            disabled={exporting}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-bold shadow-lg shadow-blue-500/20 transition-all cursor-pointer"
          >
            <FileText className="w-4 h-4" />
            <span>Export Executive PDF</span>
          </button>

          <button
            onClick={handleExportExcel}
            disabled={exporting}
            className="flex items-center space-x-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold shadow-lg shadow-emerald-500/20 transition-all cursor-pointer"
          >
            <FileSpreadsheet className="w-4 h-4" />
            <span>Export Excel</span>
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi) => (
          <KPICard key={kpi.id} kpi={kpi} />
        ))}
      </div>

      {/* Top Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {widgets.slice(1, 4).map((w, idx) => (
          <div key={w.id} className={idx === 0 ? "lg:col-span-8" : "lg:col-span-4"}>
            <ChartWidget widget={w} />
          </div>
        ))}
      </div>

      {/* AI Business Insights & Anomalies Side by Side */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Insights Column */}
        <div className="lg:col-span-7 bg-slate-800/80 border border-slate-700/80 rounded-xl p-6 shadow-lg">
          <div className="flex items-center space-x-2 mb-4">
            <Sparkles className="w-5 h-5 text-indigo-400" />
            <h3 className="text-base font-bold text-white">AI Strategic Business Insights</h3>
          </div>
          <div className="space-y-4">
            {insights.slice(0, 3).map((ins) => (
              <div key={ins.id} className="bg-slate-900/70 p-4 rounded-xl border border-slate-700/60">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-blue-400 uppercase tracking-wider">{ins.category}</span>
                  <span className="text-xs font-bold bg-blue-500/10 text-blue-300 px-2 py-0.5 rounded border border-blue-500/20">
                    {ins.metric}
                  </span>
                </div>
                <h4 className="text-sm font-bold text-slate-100 mt-1">{ins.title}</h4>
                <p className="text-xs text-slate-300 mt-1">{ins.description}</p>
                <div className="mt-2.5 pt-2 border-t border-slate-800 flex items-center space-x-1.5 text-xs text-emerald-400 font-medium">
                  <TrendingUp className="w-3.5 h-3.5 shrink-0" />
                  <span><strong>Action:</strong> {ins.recommendation}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Anomalies Column */}
        <div className="lg:col-span-5 bg-slate-800/80 border border-slate-700/80 rounded-xl p-6 shadow-lg">
          <div className="flex items-center space-x-2 mb-4">
            <AlertOctagon className="w-5 h-5 text-amber-400" />
            <h3 className="text-base font-bold text-white">Operational Anomaly Flags</h3>
          </div>
          <div className="space-y-3">
            {anomalies.slice(0, 4).map((anom) => (
              <div key={anom.id} className="bg-slate-900/70 p-3.5 rounded-xl border border-amber-500/20 flex items-start space-x-3">
                <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${
                  anom.severity === 'Critical' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                }`}>
                  {anom.severity}
                </span>
                <div>
                  <p className="text-xs font-bold text-slate-200">{anom.anomaly_type} on {anom.date}</p>
                  <p className="text-[11px] text-slate-400 mt-0.5">{anom.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
