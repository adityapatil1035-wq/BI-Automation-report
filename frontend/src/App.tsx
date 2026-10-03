import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';
import { ExecutiveDashboard } from './pages/ExecutiveDashboard';
import { UploadData } from './pages/UploadData';
import { DataQualityManager } from './pages/DataQualityManager';
import { DashboardBuilder } from './pages/DashboardBuilder';
import { AIInsightsCenter } from './pages/AIInsightsCenter';
import { AskYourData } from './pages/AskYourData';
import { ForecastingStudio } from './pages/ForecastingStudio';
import { ReportGenerator } from './pages/ReportGenerator';
import { ReportScheduler } from './pages/ReportScheduler';
import { Settings } from './pages/Settings';
import { Login } from './pages/Login';
import { Register } from './pages/Register';

const MainApp: React.FC = () => {
  const [activeTab, setActiveTab] = useState('executive');

  const renderTabContent = () => {
    switch (activeTab) {
      case 'executive':
        return <ExecutiveDashboard />;
      case 'upload':
        return <UploadData onUploadSuccess={() => setActiveTab('executive')} />;
      case 'quality':
        return <DataQualityManager />;
      case 'builder':
        return <DashboardBuilder />;
      case 'insights':
      case 'anomalies':
        return <AIInsightsCenter />;
      case 'ask':
        return <AskYourData />;
      case 'forecasting':
        return <ForecastingStudio />;
      case 'reports':
        return <ReportGenerator />;
      case 'scheduler':
        return <ReportScheduler />;
      case 'settings':
        return <Settings />;
      default:
        return <ExecutiveDashboard />;
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 overflow-hidden text-slate-100">
      {/* Sidebar Navigation */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Navbar onOpenNLQuery={() => setActiveTab('ask')} />

        <main className="flex-1 overflow-y-auto p-6 md:p-8 space-y-6">
          {renderTabContent()}
        </main>
      </div>
    </div>
  );
};

export function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
}

export default App;
