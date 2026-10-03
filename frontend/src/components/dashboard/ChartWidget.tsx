import React from 'react';
import { Widget } from '../../types';
import { 
  ResponsiveContainer, 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid, 
  Legend 
} from 'recharts';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#06B6D4'];

export const ChartWidget: React.FC<{ widget: Widget }> = ({ widget }) => {
  if (widget.type === 'kpi_cards') return null;

  const renderChart = () => {
    switch (widget.type) {
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={widget.data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={widget.x_axis as string || 'date'} stroke="#94A3B8" fontSize={11} />
              <YAxis stroke="#94A3B8" fontSize={11} tickFormatter={(v) => `₹${v >= 1000 ? (v/1000).toFixed(0) + 'k' : v}`} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', borderRadius: '8px', color: '#FFF' }}
                formatter={(val: any) => [`₹${Number(val).toLocaleString()}`, '']}
              />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              {Array.isArray(widget.y_axis) ? (
                widget.y_axis.map((key, idx) => (
                  <Line key={key} type="monotone" dataKey={key} stroke={COLORS[idx % COLORS.length]} strokeWidth={2.5} dot={{ r: 3 }} />
                ))
              ) : (
                <Line type="monotone" dataKey={widget.y_axis as string || 'Sales'} stroke="#3B82F6" strokeWidth={2.5} dot={{ r: 3 }} />
              )}
            </LineChart>
          </ResponsiveContainer>
        );

      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={widget.data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={widget.x_axis as string || 'category'} stroke="#94A3B8" fontSize={11} />
              <YAxis stroke="#94A3B8" fontSize={11} tickFormatter={(v) => `₹${v >= 1000 ? (v/1000).toFixed(0) + 'k' : v}`} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', borderRadius: '8px', color: '#FFF' }}
                formatter={(val: any) => [`₹${Number(val).toLocaleString()}`, '']}
              />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              {Array.isArray(widget.y_axis) ? (
                widget.y_axis.map((key, idx) => (
                  <Bar key={key} dataKey={key} fill={COLORS[idx % COLORS.length]} radius={[4, 4, 0, 0]} />
                ))
              ) : (
                <Bar dataKey={widget.y_axis as string || 'Sales'} fill="#3B82F6" radius={[4, 4, 0, 0]} />
              )}
            </BarChart>
          </ResponsiveContainer>
        );

      case 'donut':
        return (
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={widget.data}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={4}
                dataKey="value"
                nameKey="name"
              >
                {widget.data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', borderRadius: '8px', color: '#FFF' }}
                formatter={(val: any) => [`₹${Number(val).toLocaleString()}`, 'Sales']}
              />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
            </PieChart>
          </ResponsiveContainer>
        );

      case 'area':
        return (
          <ResponsiveContainer width="100%" height={280}>
            <AreaChart data={widget.data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={widget.x_axis as string || 'segment'} stroke="#94A3B8" fontSize={11} />
              <YAxis stroke="#94A3B8" fontSize={11} />
              <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', borderRadius: '8px', color: '#FFF' }} />
              <Area type="monotone" dataKey="Sales" stroke="#10B981" fill="#10B981" fillOpacity={0.2} />
            </AreaChart>
          </ResponsiveContainer>
        );

      case 'table':
        return (
          <div className="overflow-x-auto max-h-[280px]">
            <table className="w-full text-xs text-left text-slate-300">
              <thead className="text-[11px] uppercase bg-slate-900/60 text-slate-400 sticky top-0">
                <tr>
                  <th className="py-2.5 px-3">Item / Product</th>
                  <th className="py-2.5 px-3 text-right">Sales</th>
                  {widget.data[0]?.units !== undefined && <th className="py-2.5 px-3 text-right">Units</th>}
                  {widget.data[0]?.profit !== undefined && <th className="py-2.5 px-3 text-right">Profit</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {widget.data.map((row, i) => (
                  <tr key={i} className="hover:bg-slate-700/30">
                    <td className="py-2 px-3 font-medium text-slate-200">{row.product || row.name || `Row ${i+1}`}</td>
                    <td className="py-2 px-3 text-right font-semibold text-blue-400">₹{Number(row.sales || row.value || 0).toLocaleString()}</td>
                    {row.units !== undefined && <td className="py-2 px-3 text-right text-slate-400">{row.units}</td>}
                    {row.profit !== undefined && <td className="py-2 px-3 text-right text-emerald-400 font-medium">₹{Number(row.profit).toLocaleString()}</td>}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );

      default:
        return <p className="text-xs text-slate-400">Widget chart type not supported</p>;
    }
  };

  return (
    <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-5 shadow-lg flex flex-col justify-between">
      <div className="flex justify-between items-center mb-3">
        <h4 className="text-sm font-bold text-slate-100">{widget.title}</h4>
        <span className="text-[10px] bg-slate-700/60 text-slate-400 px-2 py-0.5 rounded font-mono uppercase">
          {widget.type}
        </span>
      </div>
      <div>
        {renderChart()}
      </div>
    </div>
  );
};
