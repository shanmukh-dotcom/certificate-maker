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
