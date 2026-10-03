import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { ReportSchedule } from '../types';
import { CalendarClock, Plus, Mail, Play, CheckCircle2, Clock } from 'lucide-react';

export const ReportScheduler: React.FC = () => {
  const { activeDataset } = useAuth();
  const [schedules, setSchedules] = useState<ReportSchedule[]>([]);
  const [showModal, setShowModal] = useState(false);

  // Form State
  const [title, setTitle] = useState('Daily Sales Intelligence Email');
  const [reportType, setReportType] = useState('Daily');
  const [frequency, setFrequency] = useState('Daily');
  const [timeOfDay, setTimeOfDay] = useState('09:00');
  const [dayOfWeek, setDayOfWeek] = useState('Monday');
  const [recipients, setRecipients] = useState('executives@acmecorp.com, analytics@acmecorp.com');
  const [format, setFormat] = useState('PDF');
  const [creating, setCreating] = useState(false);

  const fetchSchedules = () => {
    api.get('/schedules')
      .then((res) => setSchedules(res.data))
      .catch((err) => console.error('Failed to fetch schedules:', err));
  };

  useEffect(() => {
    fetchSchedules();
  }, []);

  const handleCreateSchedule = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeDataset) return;
    setCreating(true);

    try {
      await api.post('/schedules', {
        title,
        report_type: reportType,
        frequency,
        time_of_day: timeOfDay,
        day_of_week: dayOfWeek,
        recipients,
        format,
        dataset_id: activeDataset.id,
      });
      setShowModal(false);
      fetchSchedules();
      alert('Report Schedule created successfully!');
    } catch (err) {
      alert('Failed to create schedule');
    } finally {
      setCreating(false);
    }
  };

  const handleTriggerNow = async (id: number) => {
    try {
      await api.post(`/schedules/${id}/trigger`);
      alert('Report job triggered successfully! Report compiled and emailed to distribution list.');
      fetchSchedules();
    } catch (err) {
      alert('Failed to trigger report job');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Automated Report Scheduler & Emailer</h1>
          <p className="text-xs text-slate-400 mt-1">
            Configure background cron jobs to compile PDF/Excel reports automatically and dispatch them via email.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="flex items-center space-x-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20 transition-all cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>New Scheduled Job</span>
        </button>
      </div>

      {/* Active Schedules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {schedules.map((sched) => (
          <div key={sched.id} className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-lg space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-[10px] font-bold uppercase bg-blue-500/10 text-blue-400 px-2 py-0.5 rounded border border-blue-500/20">
                  {sched.frequency} ({sched.format})
                </span>
                <h3 className="text-base font-bold text-white mt-1.5">{sched.title}</h3>
              </div>

              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" title="Active Schedule"></span>
            </div>

            <div className="space-y-2 text-xs text-slate-300">
              <div className="flex items-center space-x-2">
                <Clock className="w-3.5 h-3.5 text-slate-400" />
                <span>Runs at <strong>{sched.time_of_day}</strong> {sched.frequency === 'Weekly' ? `every ${sched.day_of_week}` : ''}</span>
              </div>
              <div className="flex items-start space-x-2">
                <Mail className="w-3.5 h-3.5 text-slate-400 mt-0.5" />
                <span className="truncate max-w-[280px]">Recipients: <strong>{sched.recipients}</strong></span>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-700/60 flex items-center justify-between">
              <span className="text-[11px] text-slate-400">
                Last Run: {sched.last_run_at ? new Date(sched.last_run_at).toLocaleString() : 'Pending Next Schedule'}
              </span>

              <button
                onClick={() => handleTriggerNow(sched.id)}
                className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 hover:bg-slate-700 text-blue-400 text-xs font-bold rounded-lg border border-slate-700 transition-all cursor-pointer"
              >
                <Play className="w-3 h-3" />
                <span>Run Now</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Create Schedule Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-5">
            <h3 className="text-lg font-bold text-white">Create Automated Report Schedule</h3>

            <form onSubmit={handleCreateSchedule} className="space-y-4 text-xs">
              <div>
                <label className="block font-bold text-slate-200 mb-1">Schedule Name</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3.5 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block font-bold text-slate-200 mb-1">Frequency</label>
                  <select
                    value={frequency}
                    onChange={(e) => setFrequency(e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3.5 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
                  >
                    <option value="Daily">Daily</option>
                    <option value="Weekly">Weekly</option>
                    <option value="Monthly">Monthly</option>
                  </select>
                </div>

                <div>
                  <label className="block font-bold text-slate-200 mb-1">Run Time (24h)</label>
                  <input
                    type="text"
                    value={timeOfDay}
                    onChange={(e) => setTimeOfDay(e.target.value)}
                    placeholder="09:00"
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3.5 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-200 mb-1">Email Recipients (comma-separated)</label>
                <textarea
                  required
                  rows={2}
                  value={recipients}
                  onChange={(e) => setRecipients(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3.5 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-200 mb-1">Report Attachment Format</label>
                <select
                  value={format}
                  onChange={(e) => setFormat(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3.5 py-2 text-slate-100 focus:outline-none focus:border-blue-500"
                >
                  <option value="PDF">PDF Report Only</option>
                  <option value="Excel">Excel Report Only</option>
                  <option value="Both">Both PDF & Excel</option>
                </select>
              </div>

              <div className="pt-3 flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 bg-slate-800 text-slate-300 rounded-xl text-xs font-semibold hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={creating}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-500/20"
                >
                  {creating ? 'Creating Schedule...' : 'Save Schedule'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
