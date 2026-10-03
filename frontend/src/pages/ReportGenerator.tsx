import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { FileText, FileSpreadsheet, Download, CheckCircle2, Sparkles, Layers } from 'lucide-react';

export const ReportGenerator: React.FC = () => {
  const { activeDataset } = useAuth();
  const [reportTitle, setReportTitle] = useState('Executive Sales Intelligence Report');
  const [reportType, setReportType] = useState('Monthly Management Report');
  const [generatingPdf, setGeneratingPdf] = useState(false);
  const [generatingExcel, setGeneratingExcel] = useState(false);
  const [lastGenerated, setLastGenerated] = useState<any>(null);

  if (!activeDataset) {
    return <p className="text-slate-400 text-sm">Please select a dataset from the top navigation bar.</p>;
  }

  const handleGeneratePdf = async () => {
    setGeneratingPdf(true);
    try {
      const res = await api.post(`/reports/generate-pdf/${activeDataset.id}`, null, {
        params: { report_title: reportTitle },
      });
      setLastGenerated(res.data);
      window.open(res.data.download_url, '_blank');
    } catch (err) {
      alert('Failed to generate PDF report');
    } finally {
      setGeneratingPdf(false);
    }
  };

  const handleGenerateExcel = async () => {
    setGeneratingExcel(true);
    try {
      const res = await api.post(`/reports/generate-excel/${activeDataset.id}`);
      setLastGenerated(res.data);
      window.open(res.data.download_url, '_blank');
    } catch (err) {
      alert('Failed to generate Excel report');
    } finally {
      setGeneratingExcel(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white">Automated PDF / Excel Report Builder</h1>
        <p className="text-xs text-slate-400 mt-1">
          Compile executive-ready formatted PDF and multi-tab Excel reports embedded with KPI summary grids, AI insights, and anomaly logs.
        </p>
      </div>

      <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl space-y-6">
        <h3 className="text-base font-bold text-white border-b border-slate-700/60 pb-3">Report Configuration</h3>

        <div className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-200 mb-1.5">Report Title</label>
            <input
              type="text"
              value={reportTitle}
              onChange={(e) => setReportTitle(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-slate-100 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block font-bold text-slate-200 mb-1.5">Report Template Type</label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-slate-100 focus:outline-none focus:border-blue-500"
            >
              <option value="Daily Operational Report">Daily Operational Report (Yesterday revenue, order count, anomalies)</option>
              <option value="Weekly Performance Report">Weekly Performance Report (Growth trends, top categories)</option>
              <option value="Monthly Management Report">Monthly Management Report (Executive KPIs, full AI insights, forecasts)</option>
            </select>
          </div>
        </div>

        <div className="pt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <button
            onClick={handleGeneratePdf}
            disabled={generatingPdf}
            className="flex items-center justify-center space-x-2 py-3.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 transition-all cursor-pointer"
          >
            <FileText className="w-4 h-4" />
            <span>{generatingPdf ? 'Compiling ReportLab PDF...' : 'Compile Executive PDF Report'}</span>
          </button>

          <button
            onClick={handleGenerateExcel}
            disabled={generatingExcel}
            className="flex items-center justify-center space-x-2 py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-emerald-500/20 transition-all cursor-pointer"
          >
            <FileSpreadsheet className="w-4 h-4" />
            <span>{generatingExcel ? 'Building OpenPyXL Workbook...' : 'Compile Multi-Tab Excel Report'}</span>
          </button>
        </div>

        {lastGenerated && (
          <div className="bg-slate-900/80 p-4 rounded-xl border border-emerald-500/30 flex items-center justify-between text-xs mt-4">
            <div className="flex items-center space-x-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <div>
                <p className="font-bold text-slate-200">{lastGenerated.message}</p>
                <p className="text-[11px] text-slate-400">File: {lastGenerated.filename}</p>
              </div>
            </div>
            <a
              href={lastGenerated.download_url}
              target="_blank"
              rel="noreferrer"
              className="flex items-center space-x-1.5 px-3 py-1.5 bg-emerald-500/20 text-emerald-300 font-bold rounded-lg hover:bg-emerald-500/30 border border-emerald-500/40 transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download File</span>
            </a>
          </div>
        )}
      </div>
    </div>
  );
};
