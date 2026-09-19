import os

files = {
    'src/api/events.ts': '''import { apiClient } from './client';

export const getEvents = async () => {
  const response = await apiClient.get('/events/');
  return response.data;
};

export const getEvent = async (id: number) => {
  const response = await apiClient.get(/events/);
  return response.data;
};

export const createEvent = async (data: any) => {
  const response = await apiClient.post('/events/', data);
  return response.data;
};

export const updateEvent = async (id: number, data: any) => {
  const response = await apiClient.put(/events/, data);
  return response.data;
};
''',

    'src/features/events/EventCreate.tsx': '''import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createEvent } from '../../api/events';
import { ArrowLeft } from 'lucide-react';

export const EventCreate = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');

  const mutation = useMutation({
    mutationFn: createEvent,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['events'] });
      navigate(/events/);
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to create event');
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Event name is required');
      return;
    }
    mutation.mutate({ name, description });
  };

  return (
    <div className="max-w-3xl mx-auto animate-in fade-in duration-500">
      <button 
        onClick={() => navigate('/events')}
        className="flex items-center text-sm font-medium text-slate-500 hover:text-slate-900 mb-8 transition-colors"
      >
        <ArrowLeft size={16} className="mr-2" />
        Back to Events
      </button>

      <div className="bg-white rounded-3xl p-10 shadow-sm border border-slate-100">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Create New Event</h1>
        <p className="text-slate-500 mb-8">Set up a new workspace for your upcoming certificates.</p>

        {error && <div className="mb-6 p-4 bg-red-50 text-red-600 rounded-xl text-sm">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-slate-900 mb-2">Event Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all text-sm text-slate-900 bg-slate-50 focus:bg-white"
              placeholder="e.g. HARVEST Workshop 2026"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-900 mb-2">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={4}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all text-sm text-slate-900 bg-slate-50 focus:bg-white resize-none"
              placeholder="A brief description of the event..."
            />
          </div>

          <div className="flex justify-end pt-4">
            <button
              type="submit"
              disabled={mutation.isPending}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-medium shadow-lg shadow-blue-600/20 transition-all disabled:opacity-50"
            >
              {mutation.isPending ? 'Creating...' : 'Create Event Workspace'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
''',

    'src/features/events/EventList.tsx': '''import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getEvents } from '../../api/events';
import { useNavigate } from 'react-router-dom';
import { Plus, Calendar, MoreVertical } from 'lucide-react';

export const EventList = () => {
  const navigate = useNavigate();
  const { data: events, isLoading } = useQuery({ queryKey: ['events'], queryFn: getEvents });

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500 pb-12">
      <div className="flex justify-between items-center">
        <div>
          <p className="text-xs font-bold tracking-[0.15em] text-slate-500 uppercase mb-2">Events</p>
          <h1 className="text-3xl font-bold text-slate-900">Manage Events</h1>
        </div>
        <button 
          onClick={() => navigate('/events/new')}
          className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-xl font-medium shadow-lg shadow-blue-600/20 transition-all flex items-center"
        >
          <Plus size={18} className="mr-2" />
          Create Event
        </button>
      </div>

      <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-50/50">
            <tr className="text-slate-500 text-sm border-b border-slate-100">
              <th className="font-medium py-4 px-6">Event Name</th>
              <th className="font-medium py-4 px-6">Date</th>
              <th className="font-medium py-4 px-6">Status</th>
              <th className="font-medium py-4 px-6 w-10"></th>
            </tr>
          </thead>
          <tbody className="text-sm">
            {isLoading ? (
              <tr><td colSpan={4} className="py-8 text-center text-slate-500">Loading...</td></tr>
            ) : events?.length === 0 ? (
              <tr><td colSpan={4} className="py-16 text-center text-slate-500">No events found. Create your first event!</td></tr>
            ) : (
              events?.map((evt: any) => (
                <tr 
                  key={evt.id} 
                  onClick={() => navigate(/events/)}
                  className="border-b border-slate-50 last:border-0 hover:bg-slate-50/50 cursor-pointer transition-colors"
                >
                  <td className="py-4 px-6">
                    <div className="flex items-center space-x-4">
                      <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0">
                         <Calendar size={18} />
                      </div>
                      <div>
                        <p className="font-semibold text-slate-900">{evt.name}</p>
                        <p className="text-xs text-slate-500 line-clamp-1">{evt.description || 'No description'}</p>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-6 text-slate-600">
                    {new Date(evt.created_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}
                  </td>
                  <td className="py-4 px-6">
                    <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700">
                      <span className="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5"></span>
                      Active
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <button className="text-slate-400 hover:text-slate-600 p-1" onClick={(e) => e.stopPropagation()}>
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
  );
};
''',

    'src/components/layout/AppLayout.tsx': '''import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  CalendarDays, 
  LayoutTemplate, 
  Users, 
  FileBadge, 
  PlayCircle, 
  ShieldCheck, 
  Settings, 
  HelpCircle,
  Search,
  Bell,
  ChevronDown
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

export const AppLayout = () => {
  const logout = useAuthStore(state => state.logout);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Events', path: '/events', icon: CalendarDays },
    { name: 'Templates', path: '/templates', icon: LayoutTemplate },
    { name: 'Participants', path: '/participants', icon: Users },
    { name: 'Certificates', path: '/certificates', icon: FileBadge },
    { name: 'Generation', path: '/generation', icon: PlayCircle },
    { name: 'Verification', path: '/verification', icon: ShieldCheck },
  ];

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden">
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col justify-between flex-shrink-0 relative z-20">
        <div>
          <div className="p-6">
            <h1 className="text-xl font-black tracking-widest text-slate-900 mb-1">CERTIFY</h1>
            <p className="text-[11px] font-medium text-slate-500 tracking-wide">Certificate Management Platform</p>
          </div>
          
          <nav className="px-4 mt-2 space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.name}
                to={item.path}
                className={({ isActive }) => 
                  "flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-colors " +
                  (isActive 
                    ? 'bg-blue-50 text-blue-700' 
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900')
                }
              >
                {({ isActive }) => (
                  <>
                    <item.icon 
                      size={20} 
                      className={"mr-3 " + (isActive ? 'text-blue-700' : 'text-slate-400')} 
                      strokeWidth={isActive ? 2 : 1.5}
                    />
                    {item.name}
                  </>
                )}
              </NavLink>
            ))}
          </nav>
        </div>

        <div>
          <div className="px-4 mb-2 space-y-1">
            <div className="border-t border-slate-100 my-4 mx-4"></div>
            <a href="#" className="flex items-center px-4 py-3 text-sm font-medium rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
              <Settings size={20} className="mr-3 text-slate-400" strokeWidth={1.5} />
              Settings
            </a>
            <a href="#" className="flex items-center px-4 py-3 text-sm font-medium rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
              <HelpCircle size={20} className="mr-3 text-slate-400" strokeWidth={1.5} />
              Help
            </a>
          </div>
          
          <div className="p-4 border-t border-slate-200 cursor-pointer hover:bg-slate-50 transition-colors flex items-center justify-between group" onClick={handleLogout}>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-sm">
                AD
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-900">Admin</p>
                <p className="text-xs text-slate-500">Core Member</p>
              </div>
            </div>
            <ChevronDown size={16} className="text-slate-400 group-hover:text-slate-600" />
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col min-w-0 overflow-hidden relative z-10">
        <header className="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200/50 flex items-center justify-between px-8 flex-shrink-0 sticky top-0 z-10">
          <div className="w-full max-w-xl">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Search size={18} className="text-slate-400" />
              </div>
              <input
                type="text"
                placeholder="Search events, certificates, participants..."
                className="w-full pl-11 pr-4 py-2.5 bg-slate-100/50 border border-transparent focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200 rounded-2xl text-sm transition-all outline-none"
              />
            </div>
          </div>
          
          <div className="flex items-center space-x-6">
            <button className="relative text-slate-400 hover:text-slate-600 transition-colors">
              <Bell size={22} strokeWidth={1.5} />
              <span className="absolute top-0 right-0 block w-2 h-2 rounded-full bg-blue-500 ring-2 ring-white"></span>
            </button>
            <button className="text-slate-400 hover:text-slate-600">
              <ChevronDown size={20} />
            </button>
          </div>
        </header>

        <div className="flex-1 overflow-auto p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
''',
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
print("Files fixed.")
