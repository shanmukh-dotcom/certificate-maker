import os

files = {
    'src/api/generation.ts': '''import { apiClient } from './client';

export const startGeneration = async (eventId: number) => {
  const response = await apiClient.post(/generation/);
  return response.data;
};

export const getGenerationStatus = async (eventId: number) => {
  const response = await apiClient.get(/generation/);
  return response.data;
};
''',

    'src/features/generation/GenerationCenter.tsx': '''import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getEvent } from '../../api/events';
import { getGenerationStatus, startGeneration } from '../../api/generation';
import { 
  ArrowLeft, Calendar, MapPin, Users, CheckCircle2, AlertTriangle, 
  Play, Pause, Square, Zap, Clock, FileText, Timer, Download, Mail, BarChart3, Info
} from 'lucide-react';

export const GenerationCenter = () => {
  const [searchParams] = useSearchParams();
  const eventId = searchParams.get('event');
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  
  const { data: event, isLoading: isEventLoading } = useQuery({ 
    queryKey: ['event', eventId], 
    queryFn: () => getEvent(Number(eventId)),
    enabled: !!eventId
  });

  const { data: jobs, isLoading: isJobsLoading } = useQuery({
    queryKey: ['generation', eventId],
    queryFn: () => getGenerationStatus(Number(eventId)),
    enabled: !!eventId,
    refetchInterval: 3000
  });

  const startMutation = useMutation({
    mutationFn: startGeneration,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['generation', eventId] });
    }
  });

  // Mocking the progress state since the backend doesn't provide fine-grained logs yet
  const [progress, setProgress] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const totalRecords = 498;

  const activeJob = jobs?.[0]; // Assuming latest job
  const isGenerating = activeJob?.status === 'PROCESSING' || activeJob?.status === 'QUEUED';

  useEffect(() => {
    if (isGenerating && isPlaying && progress < totalRecords) {
      const timer = setTimeout(() => {
        setProgress(p => Math.min(p + 15, totalRecords));
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [isGenerating, isPlaying, progress]);

  useEffect(() => {
    if (isGenerating && !isPlaying && progress === 0) {
      setIsPlaying(true);
    }
  }, [isGenerating]);

  if (!eventId) return <div className="p-8 text-center text-slate-500">No event selected. Please go back to the Dashboard.</div>;
  if (isEventLoading) return <div className="p-8 text-center text-slate-500">Loading workspace...</div>;
  if (!event) return <div className="p-8 text-center text-red-500">Event not found.</div>;

  const handleStart = () => {
    startMutation.mutate(Number(eventId));
    setIsPlaying(true);
    setProgress(0);
  };

  const percentage = Math.round((progress / totalRecords) * 100) || 0;

  return (
    <div className="max-w-7xl mx-auto animate-in fade-in duration-500 pb-12">
      <div className="flex items-center text-sm font-medium text-slate-500 mb-6 space-x-2">
        <span className="cursor-pointer hover:text-slate-900 transition-colors" onClick={() => navigate('/events')}>Events</span>
        <span>›</span>
        <span className="cursor-pointer hover:text-slate-900 transition-colors" onClick={() => navigate(/events/)}>{event.name}</span>
        <span>›</span>
        <span className="text-slate-900">Generate Certificates</span>
      </div>

      <div className="flex justify-between items-start mb-10">
        <div className="flex items-start space-x-6">
          <div className="w-20 h-20 rounded-3xl bg-green-50 flex items-center justify-center flex-shrink-0 border border-green-100">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-green-600">
              <path d="M12 22c0-10-8-12-8-12s7 2 8 12c1-10 8-12 8-12s-7 2-8 12z"></path>
            </svg>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 mb-1">{event.name}</h1>
            <p className="text-slate-500 text-sm font-medium mb-3">{event.description || 'AgriTech Innovation for a Sustainable Tomorrow'}</p>
            
            <div className="flex items-center space-x-6 text-xs text-slate-600 font-medium">
              <div className="flex items-center"><Calendar size={14} className="mr-1.5 text-slate-400" /> 05 Sep 2026</div>
              <div className="flex items-center"><MapPin size={14} className="mr-1.5 text-slate-400" /> Presidency University, Bangalore</div>
              <div className="flex items-center"><Users size={14} className="mr-1.5 text-slate-400" /> 500 Participants</div>
            </div>
          </div>
        </div>
        
        <button onClick={() => navigate(/events/)} className="bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 px-4 py-2.5 rounded-xl font-medium transition-colors flex items-center text-sm shadow-sm">
          <ArrowLeft size={16} className="mr-2" />
          Back to Event
        </button>
      </div>

      <div className="flex justify-between items-center mb-10 px-8 relative">
        <div className="absolute top-6 left-16 right-16 h-0.5 bg-slate-200 -z-10"></div>
        <div className="absolute top-6 left-16 h-0.5 bg-blue-600 -z-10" style={{ width: '75%' }}></div>
        
        {[
          { step: 1, label: 'Import Participants', done: true },
          { step: 2, label: 'Validate Data', done: true },
          { step: 3, label: 'Design Template', done: true },
          { step: 4, label: 'Generate Certificates', done: false, current: true },
          { step: 5, label: 'Completed', done: false }
        ].map((s) => (
          <div key={s.step} className="flex flex-col items-center bg-slate-50">
            <div className={"w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold mb-3 border-4 transition-colors " +
              (s.done ? 'border-white bg-green-500 text-white' : s.current ? 'border-white bg-blue-600 text-white' : 'border-slate-200 bg-slate-100 text-slate-400')
            }>
              {s.done ? <CheckCircle2 size={24} className="text-white" /> : s.step}
            </div>
            <p className={"text-xs font-semibold text-center w-24 " + (s.done || s.current ? 'text-slate-900' : 'text-slate-400')}>
              {s.label.split(' ').map((word, i) => <React.Fragment key={i}>{word}<br/></React.Fragment>)}
            </p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
            <Users size={24} />
          </div>
          <div>
            <p className="text-xs font-medium text-slate-500 mb-1">Total Participants</p>
            <p className="text-2xl font-bold text-slate-900">500</p>
          </div>
        </div>
        
        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-green-50 text-green-600 flex items-center justify-center">
            <CheckCircle2 size={24} />
          </div>
          <div>
            <p className="text-xs font-medium text-slate-500 mb-1">Valid Records</p>
            <p className="text-2xl font-bold text-slate-900">498</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-red-50 text-red-500 flex items-center justify-center">
              <AlertTriangle size={24} />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-500 mb-1">Invalid Records</p>
              <p className="text-2xl font-bold text-slate-900">2</p>
            </div>
          </div>
          <a href="#" className="text-xs font-bold text-red-500 flex items-center">View Issues <ArrowLeft className="rotate-180 ml-1" size={12}/></a>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
            <Play size={24} fill="currentColor" />
          </div>
          <div>
            <p className="text-xs font-medium text-slate-500 mb-1">Generation Status</p>
            <p className="text-lg font-bold text-blue-600">Generating...</p>
            <p className="text-[10px] text-slate-400">Please keep this page open.</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-8">
        <div className="col-span-2 space-y-8">
          
          <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
            <div className="flex justify-between items-start mb-8">
              <div>
                <h3 className="text-lg font-bold text-slate-900 mb-1">Generating Certificates</h3>
                <p className="text-slate-500 text-sm">Creating personalized certificates for all valid participants.</p>
              </div>
              <div className="text-right">
                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-green-50 text-green-700 mb-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5 animate-pulse"></span>
                  In Progress
                </span>
                <p className="text-xs font-medium text-slate-400">Started at 10:24 AM</p>
              </div>
            </div>

            <div className="mb-8">
              <div className="flex items-center space-x-3 mb-2">
                <div className="flex-1 h-3 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-600 rounded-full transition-all duration-1000" style={{ width: ${percentage}% }}></div>
                </div>
                <span className="text-lg font-bold text-slate-900 w-12 text-right">{percentage}%</span>
              </div>
              <div className="flex justify-between text-xs font-medium text-slate-500">
                <span>{progress} / {totalRecords} certificates generated</span>
                <span>Estimated time remaining: 2 minutes</span>
              </div>
            </div>

            <div className="grid grid-cols-4 gap-4 mb-8">
              <div className="bg-slate-50 rounded-2xl p-4 flex flex-col justify-center border border-slate-100">
                <div className="flex items-center text-xs text-slate-500 font-medium mb-2"><Zap size={14} className="mr-2 text-blue-500" /> Processing Speed</div>
                <p className="text-lg font-bold text-slate-900">42 <span className="text-sm font-medium text-slate-500">certs/sec</span></p>
              </div>
              <div className="bg-slate-50 rounded-2xl p-4 flex flex-col justify-center border border-slate-100">
                <div className="flex items-center text-xs text-slate-500 font-medium mb-2"><Clock size={14} className="mr-2 text-blue-500" /> Elapsed Time</div>
                <p className="text-lg font-bold text-slate-900">00:01:12</p>
              </div>
              <div className="bg-slate-50 rounded-2xl p-4 flex flex-col justify-center border border-slate-100">
                <div className="flex items-center text-xs text-slate-500 font-medium mb-2"><FileText size={14} className="mr-2 text-blue-500" /> Files Generated</div>
                <p className="text-lg font-bold text-slate-900">{progress}</p>
              </div>
              <div className="bg-slate-50 rounded-2xl p-4 flex flex-col justify-center border border-slate-100">
                <div className="flex items-center text-xs text-slate-500 font-medium mb-2"><Timer size={14} className="mr-2 text-blue-500" /> Estimated Time</div>
                <p className="text-lg font-bold text-slate-900">~ 2 minutes</p>
              </div>
            </div>

            <div className="flex space-x-4">
              <button 
                onClick={() => isGenerating ? setIsPlaying(!isPlaying) : handleStart()}
                className="flex items-center px-6 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-sm rounded-xl transition-colors"
              >
                {isPlaying ? <><Pause size={16} className="mr-2" fill="currentColor" /> Pause Generation</> : <><Play size={16} className="mr-2" fill="currentColor" /> Resume Generation</>}
              </button>
              <button className="flex items-center px-6 py-3 bg-white border border-red-200 hover:bg-red-50 text-red-500 font-bold text-sm rounded-xl transition-colors">
                <Square size={16} className="mr-2" fill="currentColor" /> Stop Generation
              </button>
            </div>
          </div>

          <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h3 className="text-lg font-bold text-slate-900 mb-1">Generation Log</h3>
                <p className="text-slate-500 text-sm">Real-time updates of the certificate generation process.</p>
              </div>
              <select className="border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 focus:outline-none">
                <option>All Logs</option>
              </select>
            </div>
            
            <div className="overflow-hidden">
              <table className="w-full text-left">
                <thead>
                  <tr className="text-xs font-semibold text-slate-400 border-b border-slate-100">
                    <th className="pb-3 w-12">#</th>
                    <th className="pb-3">Participant Name</th>
                    <th className="pb-3">Certificate ID</th>
                    <th className="pb-3">Status</th>
                    <th className="pb-3 text-right">Time</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  {[
                    { id: 306, name: 'Rohan Mehta', cert: 'HARVEST-2026-0306', status: 'Generated', time: '10:25:36 AM' },
                    { id: 307, name: 'Aisha Khan', cert: 'HARVEST-2026-0307', status: 'Generated', time: '10:25:37 AM' },
                    { id: 308, name: 'Nikhil Verma', cert: 'HARVEST-2026-0308', status: 'Generated', time: '10:25:39 AM' },
                    { id: 309, name: 'Priya Sharma', cert: 'HARVEST-2026-0309', status: 'Processing', time: '10:25:40 AM' },
                    { id: 310, name: 'Arjun Nair', cert: 'HARVEST-2026-0310', status: 'Queued', time: '10:25:40 AM' },
                  ].map((log) => (
                    <tr key={log.id} className="border-b border-slate-50 last:border-0">
                      <td className="py-3 text-slate-500">{log.id}</td>
                      <td className="py-3 font-medium text-slate-900">{log.name}</td>
                      <td className="py-3 text-slate-500">{log.cert}</td>
                      <td className="py-3">
                        {log.status === 'Generated' && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-50 text-green-700">
                            <CheckCircle2 size={12} className="mr-1" /> {log.status}
                          </span>
                        )}
                        {log.status === 'Processing' && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700">
                            <span className="w-1.5 h-1.5 rounded-full bg-blue-500 mr-1.5 animate-ping"></span> {log.status}
                          </span>
                        )}
                        {log.status === 'Queued' && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-600">
                            <Clock size={12} className="mr-1" /> {log.status}
                          </span>
                        )}
                      </td>
                      <td className="py-3 text-right text-slate-500 text-xs font-medium">{log.time}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="space-y-8">
          <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm text-center">
            <div className="w-32 h-32 bg-blue-50 rounded-full mx-auto flex items-center justify-center mb-6 relative">
              <FileText size={48} className="text-blue-200 absolute -translate-x-4 -translate-y-4" />
              <FileText size={48} className="text-blue-300 absolute -translate-x-2 -translate-y-2" />
              <FileText size={48} className="text-blue-500 absolute" />
              <div className="absolute bottom-6 right-6 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-sm">
                <CheckCircle2 size={24} className="text-blue-600" fill="currentColor" stroke="white" />
              </div>
            </div>
            <h3 className="text-sm font-bold text-slate-900 mb-2">Generating high-quality certificates...</h3>
            <p className="text-xs text-slate-500 px-4 leading-relaxed">Each certificate is being personalized with participant details and securely saved.</p>
          </div>

          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-4 px-2">Actions After Completion</h3>
            <div className="space-y-3">
              <div className="bg-white border border-slate-100 p-4 rounded-2xl flex items-start space-x-3 shadow-sm hover:border-blue-200 transition-colors cursor-pointer group">
                <Download size={18} className="text-blue-600 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-blue-700 transition-colors">Download All Certificates</h4>
                  <p className="text-xs text-slate-500">Get a ZIP file of all certificates</p>
                </div>
              </div>
              <div className="bg-white border border-slate-100 p-4 rounded-2xl flex items-start space-x-3 shadow-sm hover:border-blue-200 transition-colors cursor-pointer group">
                <Mail size={18} className="text-blue-600 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-blue-700 transition-colors">Send to Participants</h4>
                  <p className="text-xs text-slate-500">Email certificates directly</p>
                </div>
              </div>
              <div className="bg-white border border-slate-100 p-4 rounded-2xl flex items-start space-x-3 shadow-sm hover:border-blue-200 transition-colors cursor-pointer group">
                <BarChart3 size={18} className="text-blue-600 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-blue-700 transition-colors">View Generation Report</h4>
                  <p className="text-xs text-slate-500">See summary and any failed certificates</p>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-blue-50 rounded-2xl p-4 flex items-start space-x-3">
            <Info size={18} className="text-blue-600 shrink-0 mt-0.5" />
            <p className="text-xs text-blue-800 font-medium leading-relaxed">
              You can safely close this page after generation is complete. We'll notify you once it's done.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
'''
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
