import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { UploadCloud, FileText, CheckCircle, ShieldCheck, AlertCircle, Database, ArrowRight } from 'lucide-react';

export const UploadData: React.FC<{ onUploadSuccess: () => void }> = ({ onUploadSuccess }) => {
  const { fetchDatasets, setActiveDataset } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post('/datasets/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setUploadResult(res.data);
      await fetchDatasets();
      setActiveDataset(res.data);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white">Upload & Ingest Business Data</h1>
        <p className="text-xs text-slate-400 mt-1">
          Import CSV, Excel (.xlsx/.xls), or JSON data. The engine automatically detects data structures, missing values, date types, and quality metrics.
        </p>
      </div>

      {/* Drag & Drop Upload Zone */}
      <div 
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-2xl p-10 text-center transition-all ${
          dragActive ? 'border-blue-500 bg-blue-500/10' : 'border-slate-700 bg-slate-800/50 hover:border-slate-600'
        }`}
      >
        <div className="w-16 h-16 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 mx-auto flex items-center justify-center mb-4">
          <UploadCloud className="w-8 h-8" />
        </div>
        <h3 className="text-base font-bold text-white">Drag and drop your dataset file here</h3>
        <p className="text-xs text-slate-400 mt-1">Supports CSV, XLSX, XLS, JSON up to 50MB</p>

        <div className="mt-6 flex justify-center items-center space-x-4">
          <label className="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 transition-all cursor-pointer">
            Browse File
            <input type="file" onChange={handleFileChange} accept=".csv,.xlsx,.xls,.json" className="hidden" />
          </label>
          {file && (
            <span className="text-xs font-semibold text-blue-400 bg-slate-800 px-3 py-2 rounded-lg border border-slate-700">
              Selected: {file.name} ({round(file.size / 1024 / 1024, 2)} MB)
            </span>
          )}
        </div>

        {file && (
          <div className="mt-6">
            <button
              onClick={handleUpload}
              disabled={uploading}
              className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl text-xs shadow-xl shadow-blue-500/20 transition-all cursor-pointer"
            >
              {uploading ? 'Processing & Profiling Dataset...' : 'Import & Run Data Quality Engine'}
            </button>
          </div>
        )}
      </div>

      {/* Upload Success Report */}
      {uploadResult && (
        <div className="bg-slate-800/90 border border-emerald-500/30 rounded-2xl p-6 shadow-xl space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
                <CheckCircle className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Dataset Ingested & Profiling Complete</h3>
                <p className="text-xs text-slate-400">File: {uploadResult.name}</p>
              </div>
            </div>

            <div className="flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/30 px-4 py-2 rounded-xl">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <span className="text-sm font-bold text-emerald-400">Quality Score: {uploadResult.data_quality_score}%</span>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-700/60">
              <p className="text-[11px] font-semibold text-slate-400">Total Rows</p>
              <h4 className="text-lg font-bold text-white mt-1">{uploadResult.row_count?.toLocaleString()}</h4>
            </div>
            <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-700/60">
              <p className="text-[11px] font-semibold text-slate-400">Total Columns</p>
              <h4 className="text-lg font-bold text-white mt-1">{uploadResult.col_count}</h4>
            </div>
            <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-700/60">
              <p className="text-[11px] font-semibold text-slate-400">Missing Cell %</p>
              <h4 className="text-lg font-bold text-amber-400 mt-1">{uploadResult.quality_summary?.missing_percentage}%</h4>
            </div>
            <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-700/60">
              <p className="text-[11px] font-semibold text-slate-400">Detected Domain</p>
              <h4 className="text-lg font-bold text-blue-400 mt-1">{uploadResult.domain}</h4>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              onClick={onUploadSuccess}
              className="flex items-center space-x-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 transition-all cursor-pointer"
            >
              <span>View Executive Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

function round(val: number, decimals: number) {
  return Number(Math.round(Number(val + 'e' + decimals)) + 'e-' + decimals);
}
