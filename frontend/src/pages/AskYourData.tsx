import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { NLQueryResponse } from '../types';
import { Sparkles, Send, Terminal, HelpCircle, Table as TableIcon, BarChart2 } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export const AskYourData: React.FC = () => {
  const { activeDataset } = useAuth();
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<NLQueryResponse | null>(null);

  const sampleQuestions = [
    "Show me sales for West region.",
    "Which product generated the highest profit?",
    "Show top 5 products by revenue.",
    "Show breakdown of sales by category.",
    "What is average order value?"
  ];

  const handleAsk = async (textToAsk?: string) => {
    const finalQuery = textToAsk || query;
    if (!finalQuery || !activeDataset) return;

    setQuery(finalQuery);
    setLoading(true);
    try {
      const res = await api.post('/nl-query/ask', {
        dataset_id: activeDataset.id,
        query: finalQuery,
      });
      setResponse(res.data);
    } catch (err) {
      alert('Failed to process natural language query');
    } finally {
      setLoading(false);
    }
  };

  if (!activeDataset) {
    return <p className="text-slate-400 text-sm">Please select a dataset from the top navigation bar.</p>;
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div className="flex items-center space-x-2 text-blue-400 text-xs font-bold uppercase tracking-wider mb-1">
          <Sparkles className="w-4 h-4" />
          <span>Natural Language Business Intelligence</span>
        </div>
        <h1 className="text-2xl font-bold text-white">Ask Your Data</h1>
        <p className="text-xs text-slate-400 mt-1">
          Ask questions in plain English. The engine translates user intent into safe analytical aggregations and renders supporting charts.
        </p>
      </div>

      {/* Query Search Bar */}
      <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-4 shadow-xl">
        <form onSubmit={(e) => { e.preventDefault(); handleAsk(); }} className="flex items-center space-x-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask anything (e.g. 'Show top 5 products by revenue' or 'Show sales for West region')..."
            className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
          <button
            type="submit"
            disabled={loading || !query}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl text-xs flex items-center space-x-2 shadow-lg shadow-blue-500/20 cursor-pointer disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
            <span>{loading ? 'Processing...' : 'Ask Engine'}</span>
          </button>
        </form>

        {/* Suggested Questions */}
        <div className="mt-4 flex flex-wrap items-center gap-2">
          <span className="text-xs text-slate-400 font-semibold flex items-center gap-1">
            <HelpCircle className="w-3.5 h-3.5 text-blue-400" /> Suggestions:
          </span>
          {sampleQuestions.map((sq, i) => (
            <button
              key={i}
              onClick={() => handleAsk(sq)}
              className="text-xs bg-slate-900/80 hover:bg-slate-700/60 text-slate-300 px-3 py-1 rounded-lg border border-slate-700/80 transition-all cursor-pointer"
            >
              {sq}
            </button>
          ))}
        </div>
      </div>

      {/* Query Response Output */}
      {response && (
        <div className="space-y-6">
          {/* Answer Card */}
          <div className="bg-slate-800/90 border border-blue-500/30 rounded-2xl p-6 shadow-xl space-y-4">
            <div className="flex items-center space-x-2 text-blue-400 text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-4 h-4" />
              <span>Calculated Answer & Insight</span>
            </div>
            <p className="text-base text-slate-100 leading-relaxed font-medium" dangerouslySetInnerHTML={{ __html: response.answer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}></p>
            
            {/* Generated Code Transparency */}
            {response.sql_or_pandas_query && (
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 flex items-center space-x-2 font-mono text-xs text-blue-400">
                <Terminal className="w-4 h-4 text-slate-500 shrink-0" />
                <span className="text-slate-500">Executing pandas query:</span>
                <span className="text-emerald-400 font-bold">{response.sql_or_pandas_query}</span>
              </div>
            )}
          </div>

          {/* Generated Chart Visual */}
          {response.chart_data && response.chart_data.length > 0 && (
            <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl">
              <div className="flex items-center space-x-2 mb-4 text-slate-200 font-bold text-sm">
                <BarChart2 className="w-4 h-4 text-blue-400" />
                <span>Supporting Analytical Visualization</span>
              </div>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={response.chart_data}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="name" stroke="#94A3B8" fontSize={11} />
                  <YAxis stroke="#94A3B8" fontSize={11} />
                  <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', borderRadius: '8px', color: '#FFF' }} />
                  <Bar dataKey="value" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Filtered Data Table */}
          {response.table_data && response.table_data.length > 0 && (
            <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl">
              <div className="flex items-center space-x-2 mb-4 text-slate-200 font-bold text-sm">
                <TableIcon className="w-4 h-4 text-blue-400" />
                <span>Relevant Dataset Records ({response.table_data.length} rows)</span>
              </div>
              <div className="overflow-x-auto max-h-[300px]">
                <table className="w-full text-xs text-left text-slate-300">
                  <thead className="text-[11px] uppercase bg-slate-900/80 text-slate-400 sticky top-0">
                    <tr>
                      {Object.keys(response.table_data[0]).map((col) => (
                        <th key={col} className="py-2.5 px-3">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {response.table_data.map((row, idx) => (
                      <tr key={idx} className="hover:bg-slate-700/30">
                        {Object.values(row).map((val: any, cIdx) => (
                          <td key={cIdx} className="py-2 px-3">{String(val)}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
