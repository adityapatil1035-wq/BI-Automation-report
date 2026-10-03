import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { ShieldCheck, Wrench, CheckCircle2, ListFilter, Play, Sparkles } from 'lucide-react';

export const DataQualityManager: React.FC = () => {
  const { activeDataset, setActiveDataset, fetchDatasets } = useAuth();
  const [cleaning, setCleaning] = useState(false);
  const [imputeMissing, setImputeMissing] = useState(true);
  const [removeDuplicates, setRemoveDuplicates] = useState(true);
  const [handleOutliers, setHandleOutliers] = useState(true);
  const [dateParsing, setDateParsing] = useState(true);

  if (!activeDataset) {
    return <p className="text-slate-400 text-sm">Please select a dataset from the top navigation bar.</p>;
  }

  const handleRunCleaning = async () => {
    setCleaning(true);
    try {
      const res = await api.post(`/datasets/${activeDataset.id}/clean`, {
        impute_missing: imputeMissing,
        remove_duplicates: removeDuplicates,
        handle_outliers: handleOutliers,
        date_parsing: dateParsing,
      });
      setActiveDataset(res.data);
      await fetchDatasets();
      alert('Data cleaning pipeline executed successfully!');
    } catch (err) {
      alert('Failed to clean dataset');
    } finally {
      setCleaning(false);
    }
  };

  const colMeta = activeDataset.column_metadata || {};
  const transformLog = activeDataset.transformation_log || [];

  return (
    <div className="space-y-6">
      {/* Header & Quality Score Gauge */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Data Quality & Preprocessing Center</h1>
          <p className="text-xs text-slate-400 mt-1">
            Audit column-level completeness, type integrity, outlier boundaries, and run automated cleaning pipelines.
          </p>
        </div>

        <div className="flex items-center space-x-4 bg-slate-800/80 p-4 rounded-xl border border-slate-700/80">
          <div className="text-right">
            <p className="text-xs font-semibold text-slate-400">Current Quality Score</p>
            <p className="text-2xl font-bold text-emerald-400">{activeDataset.data_quality_score}%</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <ShieldCheck className="w-7 h-7" />
          </div>
        </div>
      </div>

      {/* Pipeline Controls & Column Metadata Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Cleaning Options Panel */}
        <div className="lg:col-span-5 bg-slate-800/80 border border-slate-700/80 rounded-xl p-6 shadow-lg space-y-5">
          <div className="flex items-center space-x-2 border-b border-slate-700/60 pb-3">
            <Wrench className="w-5 h-5 text-blue-400" />
            <h3 className="text-base font-bold text-white">Automated Cleaning Pipeline</h3>
          </div>

          <div className="space-y-4 text-xs">
            <label className="flex items-center justify-between bg-slate-900/60 p-3 rounded-lg border border-slate-700/60 cursor-pointer">
              <div>
                <span className="font-bold text-slate-200 block">Missing Value Imputation</span>
                <span className="text-[11px] text-slate-400">Numeric median / Categorical mode replacement</span>
              </div>
              <input type="checkbox" checked={imputeMissing} onChange={(e) => setImputeMissing(e.target.checked)} className="w-4 h-4 accent-blue-600 rounded" />
            </label>

            <label className="flex items-center justify-between bg-slate-900/60 p-3 rounded-lg border border-slate-700/60 cursor-pointer">
              <div>
                <span className="font-bold text-slate-200 block">Remove Duplicate Records</span>
                <span className="text-[11px] text-slate-400">Purge duplicate rows across all fields</span>
              </div>
              <input type="checkbox" checked={removeDuplicates} onChange={(e) => setRemoveDuplicates(e.target.checked)} className="w-4 h-4 accent-blue-600 rounded" />
            </label>

            <label className="flex items-center justify-between bg-slate-900/60 p-3 rounded-lg border border-slate-700/60 cursor-pointer">
              <div>
                <span className="font-bold text-slate-200 block">IQR Outlier Capping</span>
                <span className="text-[11px] text-slate-400">Winsorize extreme values beyond 1.5x IQR</span>
              </div>
              <input type="checkbox" checked={handleOutliers} onChange={(e) => setHandleOutliers(e.target.checked)} className="w-4 h-4 accent-blue-600 rounded" />
            </label>

            <label className="flex items-center justify-between bg-slate-900/60 p-3 rounded-lg border border-slate-700/60 cursor-pointer">
              <div>
                <span className="font-bold text-slate-200 block">Date Standardisation</span>
                <span className="text-[11px] text-slate-400">Parse mixed date formats into ISO YYYY-MM-DD</span>
              </div>
              <input type="checkbox" checked={dateParsing} onChange={(e) => setDateParsing(e.target.checked)} className="w-4 h-4 accent-blue-600 rounded" />
            </label>
          </div>

          <button
            onClick={handleRunCleaning}
            disabled={cleaning}
            className="w-full flex items-center justify-center space-x-2 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl text-xs shadow-lg shadow-blue-500/20 transition-all cursor-pointer"
          >
            <Play className="w-4 h-4" />
            <span>{cleaning ? 'Executing Pipeline...' : 'Run Automated Preprocessing'}</span>
          </button>
        </div>

        {/* Column Metadata Table */}
        <div className="lg:col-span-7 bg-slate-800/80 border border-slate-700/80 rounded-xl p-6 shadow-lg">
          <h3 className="text-base font-bold text-white mb-4">Column Profiling Audit</h3>
          <div className="overflow-x-auto max-h-[340px]">
            <table className="w-full text-xs text-left text-slate-300">
              <thead className="text-[11px] uppercase bg-slate-900/80 text-slate-400 sticky top-0">
                <tr>
                  <th className="py-2.5 px-3">Column</th>
                  <th className="py-2.5 px-3">Inferred Type</th>
                  <th className="py-2.5 px-3">Missing %</th>
                  <th className="py-2.5 px-3">Unique</th>
                  <th className="py-2.5 px-3">Sample Values</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {Object.entries(colMeta).map(([col, info]: any) => (
                  <tr key={col} className="hover:bg-slate-700/30">
                    <td className="py-2 px-3 font-semibold text-slate-200">{col}</td>
                    <td className="py-2 px-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono capitalize ${
                        info.type === 'numeric' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' :
                        info.type === 'datetime' ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20' :
                        'bg-slate-700 text-slate-300'
                      }`}>
                        {info.type}
                      </span>
                    </td>
                    <td className="py-2 px-3">
                      <span className={info.missing_pct > 0 ? 'text-amber-400 font-bold' : 'text-slate-400'}>
                        {info.missing_pct}%
                      </span>
                    </td>
                    <td className="py-2 px-3 text-slate-400">{info.unique_values}</td>
                    <td className="py-2 px-3 text-slate-400 font-mono text-[10px] truncate max-w-[150px]">
                      {info.sample_values?.join(', ')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Transformation Audit Log */}
      <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-6 shadow-lg">
        <h3 className="text-base font-bold text-white mb-4">Transformation Audit Trail Log</h3>
        {transformLog.length === 0 ? (
          <p className="text-xs text-slate-400 italic">No cleaning transformations have been applied yet. Run the automated preprocessing pipeline above.</p>
        ) : (
          <div className="space-y-2">
            {transformLog.map((log: any, idx: number) => (
              <div key={idx} className="bg-slate-900/60 p-3 rounded-lg border border-slate-700/60 flex items-start space-x-3 text-xs">
                <span className="w-5 h-5 rounded-full bg-blue-500/20 text-blue-400 font-bold flex items-center justify-center text-[10px] shrink-0">
                  {log.step}
                </span>
                <div>
                  <span className="font-bold text-slate-200">{log.action}</span>
                  {log.column && <span className="text-blue-400 ml-2 font-mono">[{log.column}]</span>}
                  <p className="text-slate-400 mt-0.5">{log.detail}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
