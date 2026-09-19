import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getEvent } from '../../api/events';
import { 
  Calendar, MapPin, Users, Edit2, MoreVertical, CheckSquare, 
  ShieldCheck, Play, Award, FileText, Upload, Check, Eye, ArrowRight, Settings
} from 'lucide-react';

export const EventWorkspace = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('Overview');

  const { data: event, isLoading } = useQuery({ 
    queryKey: ['event', id], 
    queryFn: () => getEvent(Number(id)),
    enabled: !!id
  });

  if (isLoading) return <div className="p-8 text-center text-slate-500">Loading workspace...</div>;
  if (!event) return <div className="p-8 text-center text-red-500">Event not found.</div>;

  const tabs = [
    { name: 'Overview', icon: CheckSquare },
    { name: 'Participants', icon: Users },
    { name: 'Certificate', icon: ShieldCheck },
    { name: 'Generate', icon: Play },
    { name: 'Issued', icon: Award },
  ];

  return (
    <div className="max-w-7xl mx-auto animate-in fade-in duration-500 pb-12">
      {/* Breadcrumbs */}
      <div className="flex items-center text-sm font-medium text-slate-500 mb-6 space-x-2">
        <span className="cursor-pointer hover:text-slate-900 transition-colors" onClick={() => navigate('/events')}>Events</span>
        <span>›</span>
        <span className="text-slate-900">{event.name}</span>
      </div>

      {/* Header */}
      <div className="flex justify-between items-start mb-8">
        <div className="flex items-start space-x-6">
          <div className="w-24 h-24 rounded-3xl bg-green-50 flex items-center justify-center flex-shrink-0 border border-green-100">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-green-600">
              <path d="M12 22c0-10-8-12-8-12s7 2 8 12c1-10 8-12 8-12s-7 2-8 12z"></path>
            </svg>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-slate-900 mb-1">{event.name}</h1>
            <p className="text-slate-500 font-medium mb-4">{event.description || 'No description provided'}</p>
            
            <div className="flex items-center space-x-6 text-sm text-slate-600 font-medium">
              <div className="flex items-center"><Calendar size={16} className="mr-2 text-slate-400" /> 05 Sep 2026</div>
              <div className="flex items-center"><MapPin size={16} className="mr-2 text-slate-400" /> Presidency University, Bangalore</div>
              <div className="flex items-center"><Users size={16} className="mr-2 text-slate-400" /> 500 Participants</div>
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-green-50 text-green-700">
                <span className="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5"></span>
                Active
              </span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          <button className="bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 px-4 py-2.5 rounded-xl font-medium transition-colors flex items-center text-sm shadow-sm">
            <Edit2 size={16} className="mr-2" />
            Edit Event
          </button>
          <button className="bg-white border border-slate-200 hover:bg-slate-50 text-slate-500 p-2.5 rounded-xl transition-colors shadow-sm">
            <MoreVertical size={16} />
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-8 border-b border-slate-200 mb-8">
        {tabs.map(tab => (
          <button
            key={tab.name}
            onClick={() => setActiveTab(tab.name)}
            className={"pb-4 flex items-center space-x-2 text-sm font-medium transition-colors relative " +
              (activeTab === tab.name ? 'text-blue-600' : 'text-slate-500 hover:text-slate-900')}
          >
            <tab.icon size={18} />
            <span>{tab.name}</span>
            {activeTab === tab.name && (
              <div className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-600 rounded-t-full"></div>
            )}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'Overview' && (
        <div className="grid grid-cols-3 gap-8">
          <div className="col-span-2 space-y-8">
            <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
              <div className="flex justify-between items-start mb-10">
                <div>
                  <h3 className="text-lg font-bold text-slate-900 mb-1">Event Setup Progress</h3>
                  <p className="text-slate-500 text-sm">Complete the steps to generate and issue certificates.</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-slate-900 mb-2">4 of 5 completed</p>
                  <div className="flex items-center space-x-3">
                    <div className="w-32 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full bg-blue-600 rounded-full" style={{ width: '80%' }}></div>
                    </div>
                    <span className="text-xs font-bold text-slate-500">80%</span>
                  </div>
                </div>
              </div>
              
              <div className="flex justify-between relative px-4">
                <div className="absolute top-4 left-10 right-10 h-0.5 bg-slate-100 z-0"></div>
                <div className="absolute top-4 left-10 h-0.5 bg-blue-600 z-0" style={{ width: '75%' }}></div>
                
                {[
                  { step: 1, label: 'Event Details', done: true },
                  { step: 2, label: 'Participants Imported', done: true },
                  { step: 3, label: 'Certificate Designed', done: true },
                  { step: 4, label: 'Generation Ready', done: false, current: true },
                  { step: 5, label: 'Certificates Issued', done: false }
                ].map((s) => (
                  <div key={s.step} className="relative z-10 flex flex-col items-center">
                    <div className={"w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold mb-3 border-2 transition-colors bg-white " +
                      (s.done ? 'border-green-500 bg-green-500 text-white' : s.current ? 'border-blue-600 bg-blue-600 text-white' : 'border-slate-200 text-slate-400')
                    }>
                      {s.done ? <Check size={16} strokeWidth={3} /> : s.step}
                    </div>
                    <p className={"text-xs font-semibold text-center w-20 " + (s.done || s.current ? 'text-slate-900' : 'text-slate-400')}>
                      {s.label.split(' ').map((word, i) => <React.Fragment key={i}>{word}<br/></React.Fragment>)}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-bold text-slate-900 mb-4">Quick Actions</h3>
              <div className="grid grid-cols-4 gap-4">
                <div onClick={() => navigate('/participants?event=' + event.id)} className="bg-blue-50/50 hover:bg-blue-50 border border-blue-100 rounded-3xl p-5 cursor-pointer transition-colors group">
                  <div className="w-10 h-10 rounded-xl bg-white text-blue-600 shadow-sm flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <Users size={20} />
                  </div>
                  <h4 className="font-bold text-slate-900 text-sm mb-1">Manage Participants</h4>
                  <p className="text-xs text-slate-500 mb-4 h-8">View, import or edit participant data.</p>
                  <ArrowRight size={16} className="text-blue-600 ml-auto" />
                </div>
                
                <div onClick={() => navigate('/templates/new?event=' + event.id)} className="bg-purple-50/50 hover:bg-purple-50 border border-purple-100 rounded-3xl p-5 cursor-pointer transition-colors group">
                  <div className="w-10 h-10 rounded-xl bg-white text-purple-600 shadow-sm flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <FileText size={20} />
                  </div>
                  <h4 className="font-bold text-slate-900 text-sm mb-1">Design Certificate</h4>
                  <p className="text-xs text-slate-500 mb-4 h-8">Create or edit the certificate template.</p>
                  <ArrowRight size={16} className="text-purple-600 ml-auto" />
                </div>

                <div onClick={() => navigate('/generation?event=' + event.id)} className="bg-green-50/50 hover:bg-green-50 border border-green-100 rounded-3xl p-5 cursor-pointer transition-colors group">
                  <div className="w-10 h-10 rounded-xl bg-white text-green-600 shadow-sm flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <Play size={20} fill="currentColor" />
                  </div>
                  <h4 className="font-bold text-slate-900 text-sm mb-1">Generate Certificates</h4>
                  <p className="text-xs text-slate-500 mb-4 h-8">Start the issuance process.</p>
                  <ArrowRight size={16} className="text-green-600 ml-auto" />
                </div>

                <div onClick={() => navigate('/certificates?event=' + event.id)} className="bg-orange-50/50 hover:bg-orange-50 border border-orange-100 rounded-3xl p-5 cursor-pointer transition-colors group">
                  <div className="w-10 h-10 rounded-xl bg-white text-orange-500 shadow-sm flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <Eye size={20} />
                  </div>
                  <h4 className="font-bold text-slate-900 text-sm mb-1">View Issued</h4>
                  <p className="text-xs text-slate-500 mb-4 h-8">See and manage issued certificates.</p>
                  <ArrowRight size={16} className="text-orange-500 ml-auto" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-bold text-slate-900">Recent Activity</h3>
                <a href="#" className="text-sm font-semibold text-blue-600 flex items-center">View All <ArrowRight size={16} className="ml-1"/></a>
              </div>
              <div className="space-y-6">
                {[
                  { icon: Upload, color: 'text-green-600', bg: 'bg-green-50', title: 'Participants imported (500 records)', time: '19 Sep 2026, 10:24 AM', user: 'Shanmukh' },
                  { icon: FileText, color: 'text-purple-600', bg: 'bg-purple-50', title: 'Certificate template updated', time: '18 Sep 2026, 06:15 PM', user: 'Shanmukh' },
                  { icon: Settings, color: 'text-blue-600', bg: 'bg-blue-50', title: 'Event details created', time: '18 Sep 2026, 05:40 PM', user: 'Shanmukh' },
                  { icon: Users, color: 'text-orange-500', bg: 'bg-orange-50', title: 'Team member added', time: '17 Sep 2026, 11:12 AM', user: 'Admin' },
                ].map((activity, i) => (
                  <div key={i} className="flex items-center justify-between group">
                    <div className="flex items-center space-x-4">
                      <div className={"w-10 h-10 rounded-xl " + activity.bg + " " + activity.color + " flex items-center justify-center"}>
                        <activity.icon size={18} />
                      </div>
                      <div>
                        <p className="font-semibold text-slate-900 text-sm">{activity.title}</p>
                        <p className="text-xs text-slate-500">{activity.time}</p>
                      </div>
                    </div>
                    <p className="text-xs text-slate-400 font-medium">By {activity.user}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-8">
            <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-bold text-slate-900">Event Details</h3>
                <a href="#" className="text-sm font-semibold text-blue-600">Edit</a>
              </div>
              <div className="space-y-4">
                <div className="flex text-sm">
                  <span className="w-1/3 text-slate-500">Event Name</span>
                  <span className="w-2/3 text-slate-900 font-medium">{event.name}</span>
                </div>
                <div className="flex text-sm">
                  <span className="w-1/3 text-slate-500">Description</span>
                  <span className="w-2/3 text-slate-900 font-medium">{event.description || 'N/A'}</span>
                </div>
                <div className="flex text-sm">
                  <span className="w-1/3 text-slate-500">Date</span>
                  <span className="w-2/3 text-slate-900 font-medium">05 September 2026</span>
                </div>
                <div className="flex text-sm">
                  <span className="w-1/3 text-slate-500">Venue</span>
                  <span className="w-2/3 text-slate-900 font-medium">Presidency University, Bangalore</span>
                </div>
                <div className="flex text-sm">
                  <span className="w-1/3 text-slate-500">Organized by</span>
                  <span className="w-2/3 text-slate-900 font-medium">HARVEST AgriTech Innovation Club</span>
                </div>
                <div className="flex text-sm">
                  <span className="w-1/3 text-slate-500">Certificate Type</span>
                  <span className="w-2/3 text-slate-900 font-medium">Participation Certificate</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-bold text-slate-900">Team Members</h3>
                <a href="#" className="text-sm font-semibold text-blue-600">Manage</a>
              </div>
              <div className="space-y-5">
                {[
                  { initials: 'SC', name: 'Shanmukh', role: 'Event Manager' },
                  { initials: 'AR', name: 'Aditya Reddy', role: 'Coordinator' },
                  { initials: 'PK', name: 'Pranavi K', role: 'Design Lead' },
                  { initials: 'VR', name: 'Varun R', role: 'Core Member' },
                ].map((user, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 rounded-full bg-blue-50 text-blue-700 flex items-center justify-center font-bold text-sm">
                        {user.initials}
                      </div>
                      <div>
                        <p className="font-semibold text-slate-900 text-sm">{user.name}</p>
                        <p className="text-xs text-slate-500">{user.role}</p>
                      </div>
                    </div>
                    <div className="flex items-center text-xs text-slate-500 font-medium">
                      <span className="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5"></span>
                      Active
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
      
      {activeTab !== 'Overview' && (
        <div className="bg-white rounded-3xl p-12 text-center border border-slate-100 shadow-sm">
          <p className="text-slate-500">The {activeTab} view will be implemented in the respective phases.</p>
        </div>
      )}
    </div>
  );
};
