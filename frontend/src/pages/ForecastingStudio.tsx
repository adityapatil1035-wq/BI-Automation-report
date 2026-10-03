import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { ForecastData } from '../types';
import { TrendingUp, Calendar, Cpu, Activity, CheckCircle } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';

export const ForecastingStudio: React.FC = () => {
  const { activeDataset } = useAuth();
  const [horizon, setHorizon] = useState<number>(30);
  const [modelType, setModelType] = useState<string>('auto');
  const [forecastData, setForecastData] = useState<ForecastData | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchForecast = () => {
    if (!activeDataset) return;
    setLoading(true);
    api.post('/forecasting/predict', {
      dataset_id: activeDataset.id,
      horizon_days: horizon,
      model_type: modelType,
    })
      .then((res) => setForecastData(res.data))
      .catch((err) => console.error('Failed to run forecast:', err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchForecast();
  }, [activeDataset, horizon, modelType]);

  if (!activeDataset) {
    return <p className="text-slate-400 text-sm">Please select a dataset from the top navigation bar.</p>;
  }

  // Combine historical and forecast arrays for timeline chart
  const combinedChartData = forecastData ? [
    ...forecastData.historical.map(h => ({ date: h.date, Historical: h.actual, Forecast: null, Upper: null, Lower: null })),
    ...forecastData.forecast.map(f => ({ date: f.date, Historical: null, Forecast: f.forecast, Upper: f.upper_bound, Lower: f.lower_bound }))
  ] : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white">Time-Series Forecasting Studio</h1>
        <p className="text-xs text-slate-400 mt-1">
          Predict future revenue, sales, or demand trajectories with confidence interval boundaries using statistical machine learning models.
        </p>
      </div>

      {/* Forecasting Control Panel */}
      <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-5 shadow-lg flex flex-wrap items-center justify-between gap-4 text-xs">
        {/* Horizon Selector */}
        <div className="flex items-center space-x-2">
          <Calendar className="w-4 h-4 text-blue-400" />
          <span className="font-bold text-slate-200">Forecast Horizon:</span>
          <div className="flex items-center bg-slate-900 rounded-lg p-1 border border-slate-700">
            {[7, 30, 90, 180].map((h) => (
              <button
                key={h}
                onClick={() => setHorizon(h)}
                className={`px-3 py-1 rounded-md text-xs font-semibold transition-all cursor-pointer ${
                  horizon === h ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {h} Days
              </button>
            ))}
          </div>
        </div>

        {/* Model Selector */}
        <div className="flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-indigo-400" />
          <span className="font-bold text-slate-200">Model Engine:</span>
          <select
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
            className="bg-slate-900 text-slate-100 font-semibold px-3 py-1.5 rounded-lg border border-slate-700 focus:outline-none cursor-pointer"
          >
            <option value="auto">Linear Trend (Auto Baseline)</option>
            <option value="ridge">Ridge Regression</option>
            <option value="random_forest">Random Forest Regressor</option>
          </select>
        </div>

        {/* Evaluation Metrics Badge */}
        {forecastData?.metrics && (
          <div className="flex items-center space-x-3 bg-slate-900/80 px-3.5 py-1.5 rounded-lg border border-slate-700">
            <span className="text-slate-400">R² Score: <strong className="text-emerald-400">{forecastData.metrics.r2_score}</strong></span>
            <span className="text-slate-400">RMSE: <strong className="text-blue-400">₹{forecastData.metrics.rmse}</strong></span>
            <span className="text-slate-400">MAE: <strong className="text-indigo-400">₹{forecastData.metrics.mae}</strong></span>
          </div>
        )}
      </div>

      {/* Main Forecast Chart View */}
      <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-blue-400" />
              <span>Historical Performance & {horizon}-Day Forecast Horizon</span>
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">Model: {forecastData?.model_name || 'Linear Model'}</p>
          </div>

          <div className="flex items-center space-x-4 text-xs">
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-blue-500"></span> Historical</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-emerald-400"></span> Forecast</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-emerald-500/30"></span> 95% Confidence Band</span>
          </div>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center h-80 space-y-3">
            <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-xs font-medium text-slate-400">Fitting time-series regression and computing forecast...</p>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={380}>
            <AreaChart data={combinedChartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="date" stroke="#94A3B8" fontSize={11} />
              <YAxis stroke="#94A3B8" fontSize={11} tickFormatter={(v) => `₹${v >= 1000 ? (v/1000).toFixed(0) + 'k' : v}`} />
              <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', borderRadius: '8px', color: '#FFF' }} />
              
              <Area type="monotone" dataKey="Upper" stroke="none" fill="#10B981" fillOpacity={0.15} name="Upper Bound" />
              <Area type="monotone" dataKey="Historical" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.2} strokeWidth={2.5} name="Historical Actual" />
              <Area type="monotone" dataKey="Forecast" stroke="#10B981" fill="#10B981" fillOpacity={0.3} strokeWidth={2.5} strokeDasharray="5 5" name="Forecast Projection" />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};
