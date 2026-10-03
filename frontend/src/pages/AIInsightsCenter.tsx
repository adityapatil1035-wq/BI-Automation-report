import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { Insight, Anomaly } from '../types';
import { Sparkles, AlertOctagon, TrendingUp, Lightbulb, ShieldAlert, ArrowUpRight } from 'lucide-react';

export const AIInsightsCenter: React.FC = () => {
  const { activeDataset } = useAuth();
  const [insights, setInsights] = useState<Insight[]>([]);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (activeDataset) {
      setLoading(true);
      Promise.all([
        api.get(`/analytics/${activeDataset.id}/insights`),
        api.get(`/analytics/${activeDataset.id}/anomalies`),
      ])
        .then(([insRes, anomRes]) => {
          setInsights(insRes.data || []);
          setAnomalies(anomRes.data || []);
        })
        .catch((err) => console.error('Failed to fetch AI insights:', err))
        .finally(() => setLoading(false));
    }
  }, [activeDataset]);

  if (!activeDataset) {
    return <p className="text-slate-400 text-sm">Please select a dataset from the top navigation bar.</p>;
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-80 space-y-4">
        <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-medium text-slate-400">Synthesizing statistical and LLM AI insights...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white">AI Business Intelligence Engine</h1>
        <p className="text-xs text-slate-400 mt-1">
          Ground-truth statistical insights and machine learning anomaly detection computed directly from raw dataset records.
        </p>
      </div>

      {/* Strategic Insights Cards Grid */}
      <div>
        <div className="flex items-center space-x-2 mb-4">
          <Sparkles className="w-5 h-5 text-indigo-400" />
          <h2 className="text-lg font-bold text-white">Executive Strategic Insights</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {insights.map((ins) => (
            <div key={ins.id} className="bg-slate-800/80 border border-slate-700/80 hover:border-blue-500/40 rounded-xl p-6 shadow-lg space-y-4 transition-all">
              <div className="flex justify-between items-start">
                <span className="text-xs font-bold text-blue-400 uppercase tracking-wider bg-blue-500/10 px-2.5 py-1 rounded border border-blue-500/20">
                  {ins.category}
                </span>
                <span className="text-xs font-bold bg-slate-900 text-slate-200 px-3 py-1 rounded-lg border border-slate-700">
                  {ins.metric}
                </span>
              </div>

              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-1.5">
                  {ins.title}
                  <ArrowUpRight className="w-4 h-4 text-blue-400 shrink-0" />
                </h3>
                <p className="text-xs text-slate-300 mt-1.5 leading-relaxed">{ins.description}</p>
              </div>

              <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-700/60 flex items-start space-x-3 text-xs">
                <Lightbulb className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold text-slate-200 block">Recommended Action:</span>
                  <span className="text-slate-300 mt-0.5 block">{ins.recommendation}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Operational Anomaly Detection Center */}
      <div className="pt-4">
        <div className="flex items-center space-x-2 mb-4">
          <ShieldAlert className="w-5 h-5 text-amber-400" />
          <h2 className="text-lg font-bold text-white">Machine Learning Anomaly Audit Timeline</h2>
        </div>

        <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-6 shadow-lg">
          <div className="overflow-x-auto max-h-[380px]">
            <table className="w-full text-xs text-left text-slate-300">
              <thead className="text-[11px] uppercase bg-slate-900/80 text-slate-400 sticky top-0">
                <tr>
                  <th className="py-3 px-3">Date / Timestamp</th>
                  <th className="py-3 px-3">Metric Analyzed</th>
                  <th className="py-3 px-3">Actual Value</th>
                  <th className="py-3 px-3">Dataset Expected Avg</th>
                  <th className="py-3 px-3">Z-Score</th>
                  <th className="py-3 px-3">Severity</th>
                  <th className="py-3 px-3">Anomaly Explanation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {anomalies.map((anom) => (
                  <tr key={anom.id} className="hover:bg-slate-700/30">
                    <td className="py-2.5 px-3 font-semibold text-slate-200">{anom.date}</td>
                    <td className="py-2.5 px-3 font-medium text-blue-400">{anom.metric_name}</td>
                    <td className="py-2.5 px-3 font-bold text-slate-100">₹{anom.actual_value.toLocaleString()}</td>
                    <td className="py-2.5 px-3 text-slate-400">₹{anom.expected_value.toLocaleString()}</td>
                    <td className="py-2.5 px-3 font-mono font-bold text-amber-400">z={anom.z_score}</td>
                    <td className="py-2.5 px-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                        anom.severity === 'Critical' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                        anom.severity === 'High' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                        'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                      }`}>
                        {anom.severity}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-slate-300 max-w-[280px]">{anom.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
