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
                  onClick={() => navigate('/events/' + evt.id)}
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
