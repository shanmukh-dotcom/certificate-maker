import { useQuery } from '@tanstack/react-query';
import { getEvents } from '../../api/events';
import { getCertificates } from '../../api/certificates';
import { 
  Plus, 
  Calendar, 
  FileCheck, 
  Users, 
  ShieldCheck, 
  ArrowRight,
  MoreVertical,
  PenTool,
  Upload,
  Play
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Dashboard = () => {
  const navigate = useNavigate();
  const { data: events, isLoading } = useQuery({ queryKey: ['events'], queryFn: getEvents });
  const { data: certs } = useQuery({ queryKey: ['certificates'], queryFn: getCertificates });

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500 pb-12">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <p className="text-xs font-bold tracking-[0.15em] text-slate-500 uppercase mb-2">Dashboard</p>
          <h1 className="text-4xl font-bold text-slate-900 mb-2">
            Good morning, Admin <span className="text-3xl">👋</span>
          </h1>
          <p className="text-slate-500 text-lg">Manage your events, create certificates and make an impact.</p>
        </div>
        
        <div className="flex items-center space-x-8">
          <button 
            onClick={() => navigate('/events/new')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-medium shadow-lg shadow-blue-600/20 transition-all flex items-center"
          >
            <Plus size={20} className="mr-2" />
            Create Event
          </button>
          
          <div className="flex items-center space-x-6 border-l border-slate-200 pl-6 h-12">
            <div>
              <p className="text-xs text-slate-500 font-medium">Friday</p>
              <p className="text-sm font-semibold text-slate-900">19 Sep 2026</p>
            </div>
            <p className="text-sm italic text-slate-500 max-w-[180px] leading-snug">
              "Small recognition creates big motivation."
            </p>
          </div>
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-4 gap-6">
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 flex flex-col relative overflow-hidden">
          <div className="flex items-center space-x-4 mb-4">
            <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center">
              <Calendar size={24} strokeWidth={1.5} />
            </div>
            <span className="text-slate-600 font-medium text-sm">Total Events</span>
          </div>
          <div className="text-4xl font-bold text-slate-900 mb-2">
             {isLoading ? <div className="h-10 bg-slate-100 animate-pulse rounded w-16"></div> : (events?.length || 0)}
          </div>
          <p className="text-sm text-green-600 font-medium flex items-center">
             ↑ +0 this month
          </p>
        </div>

        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 flex flex-col relative overflow-hidden bg-gradient-to-br from-white to-emerald-50/30">
          <div className="flex items-center space-x-4 mb-4">
            <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center">
              <FileCheck size={24} strokeWidth={1.5} />
            </div>
            <span className="text-slate-600 font-medium text-sm">Certificates Issued</span>
          </div>
          <div className="text-4xl font-bold text-slate-900 mb-2">
            0
          </div>
          <p className="text-sm text-emerald-600 font-medium flex items-center">
             ↑ +0 this month
          </p>
        </div>

        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 flex flex-col relative overflow-hidden bg-gradient-to-br from-white to-orange-50/30">
          <div className="flex items-center space-x-4 mb-4">
            <div className="w-12 h-12 bg-orange-50 text-orange-500 rounded-xl flex items-center justify-center">
              <Users size={24} strokeWidth={1.5} />
            </div>
            <span className="text-slate-600 font-medium text-sm">Total Participants</span>
          </div>
          <div className="text-4xl font-bold text-slate-900 mb-2">
            0
          </div>
          <p className="text-sm text-orange-500 font-medium flex items-center">
             ↑ +0 this month
          </p>
        </div>

        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 flex flex-col relative overflow-hidden bg-gradient-to-br from-white to-purple-50/30">
          <div className="flex items-center space-x-4 mb-4">
            <div className="w-12 h-12 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center">
              <ShieldCheck size={24} strokeWidth={1.5} />
            </div>
            <span className="text-slate-600 font-medium text-sm">Verified Certificates</span>
          </div>
          <div className="text-4xl font-bold text-slate-900 mb-2">
            0
          </div>
          <p className="text-sm text-emerald-600 font-medium flex items-center">
             ● 0% valid
          </p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Recent Events */}
        <div className="col-span-2 bg-white rounded-3xl shadow-sm border border-slate-100 p-8">
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-xl font-bold text-slate-900">Recent Events</h3>
            <a href="/events" className="text-blue-600 font-medium text-sm flex items-center hover:text-blue-700 transition-colors">
              View All <ArrowRight size={16} className="ml-1" />
            </a>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="text-slate-500 text-sm border-b border-slate-100">
                  <th className="font-medium pb-4 pl-2">Event Name</th>
                  <th className="font-medium pb-4">Date</th>
                  <th className="font-medium pb-4">Participants</th>
                  <th className="font-medium pb-4">Status</th>
                  <th className="font-medium pb-4 w-10"></th>
                </tr>
              </thead>
              <tbody className="text-sm">
                {isLoading ? (
                  <tr><td colSpan={5} className="py-8 text-center text-slate-500">Loading...</td></tr>
                ) : events?.length === 0 ? (
                  <tr><td colSpan={5} className="py-8 text-center text-slate-500">No events found. Create one!</td></tr>
                ) : (
                  events?.slice(0, 4).map((evt: any) => (
                    <tr key={evt.id} className="border-b border-slate-50 last:border-0 hover:bg-slate-50/50 transition-colors">
                      <td className="py-4 pl-2">
                        <div className="flex items-center space-x-4">
                          <div className="w-10 h-10 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0">
                             <Calendar size={18} />
                          </div>
                          <div>
                            <p className="font-semibold text-slate-900">{evt.name}</p>
                            <p className="text-xs text-slate-500 line-clamp-1">{evt.description || 'No description'}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-4 text-slate-600">
                        {new Date(evt.created_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}
                      </td>
                      <td className="py-4 text-slate-600">0</td>
                      <td className="py-4">
                        <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600">
                          {evt.status || 'Draft'}
                        </span>
                      </td>
                      <td className="py-4">
                        <button className="text-slate-400 hover:text-slate-600 p-1">
                          <MoreVertical size={16} />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right Side */}
        <div className="space-y-6">
          {/* Chart Card */}
          <div className="bg-white rounded-3xl shadow-sm border border-slate-100 p-8">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-bold text-slate-900">Certificate Issuance</h3>
              <select className="bg-slate-50 border border-slate-200 text-slate-600 text-xs rounded-lg px-2 py-1 outline-none">
                <option>This Month</option>
              </select>
            </div>
            
            {/* Fake Chart since no data */}
            <div className="h-48 flex items-end justify-between px-2 pb-2 mt-4 space-x-2 border-l border-b border-slate-100 relative">
               <div className="absolute left-[-24px] flex flex-col justify-between h-full text-[10px] text-slate-400 py-1">
                 <span>400</span><span>300</span><span>200</span><span>100</span><span>0</span>
               </div>
               {/* Bars */}
               <div className="w-12 bg-blue-400 rounded-t-sm h-[40%] hover:bg-blue-500 transition-colors mx-auto relative group">
                  <div className="absolute -bottom-6 w-full text-center text-xs text-slate-500">W1</div>
               </div>
               <div className="w-12 bg-blue-400 rounded-t-sm h-[55%] hover:bg-blue-500 transition-colors mx-auto relative group">
                  <div className="absolute -bottom-6 w-full text-center text-xs text-slate-500">W2</div>
               </div>
               <div className="w-12 bg-blue-500 rounded-t-sm h-[70%] hover:bg-blue-600 transition-colors mx-auto relative group">
                  <div className="absolute -bottom-6 w-full text-center text-xs text-slate-500">W3</div>
               </div>
               <div className="w-12 bg-blue-500 rounded-t-sm h-[95%] hover:bg-blue-600 transition-colors mx-auto relative group">
                  <div className="absolute -bottom-6 w-full text-center text-xs text-slate-500">W4</div>
               </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-3xl shadow-sm border border-slate-100 p-8">
            <h3 className="text-lg font-bold text-slate-900 mb-6">Quick Actions</h3>
            <div className="grid grid-cols-2 gap-4">
              <div 
                onClick={() => navigate('/events/new')}
                className="p-4 rounded-2xl bg-slate-50 border border-slate-100 hover:border-blue-200 hover:bg-blue-50/50 cursor-pointer transition-all group"
              >
                <div className="w-10 h-10 rounded-xl bg-white text-blue-600 shadow-sm flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                  <Calendar size={18} />
                </div>
                <p className="font-semibold text-slate-900 text-sm mb-0.5">Create Event</p>
                <p className="text-[11px] text-slate-500 line-clamp-1">Set up a new event</p>
              </div>

              <div 
                onClick={() => navigate('/templates')}
                className="p-4 rounded-2xl bg-slate-50 border border-slate-100 hover:border-blue-200 hover:bg-blue-50/50 cursor-pointer transition-all group"
              >
                <div className="w-10 h-10 rounded-xl bg-white text-blue-600 shadow-sm flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                  <PenTool size={18} />
                </div>
                <p className="font-semibold text-slate-900 text-sm mb-0.5">Design Template</p>
                <p className="text-[11px] text-slate-500 line-clamp-1">Create or edit certificates</p>
              </div>

              <div 
                onClick={() => navigate('/events')}
                className="p-4 rounded-2xl bg-slate-50 border border-slate-100 hover:border-blue-200 hover:bg-blue-50/50 cursor-pointer transition-all group"
              >
                <div className="w-10 h-10 rounded-xl bg-white text-blue-600 shadow-sm flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                  <Users size={18} />
                </div>
                <p className="font-semibold text-slate-900 text-sm mb-0.5">Import</p>
                <p className="text-[11px] text-slate-500 line-clamp-1">Upload CSV / Excel</p>
              </div>

              <div 
                onClick={() => navigate('/generation')}
                className="p-4 rounded-2xl bg-slate-50 border border-slate-100 hover:border-blue-200 hover:bg-blue-50/50 cursor-pointer transition-all group"
              >
                <div className="w-10 h-10 rounded-xl bg-white text-blue-600 shadow-sm flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                  <Play size={18} fill="currentColor" />
                </div>
                <p className="font-semibold text-slate-900 text-sm mb-0.5">Generate</p>
                <p className="text-[11px] text-slate-500 line-clamp-1">Start issuance process</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
