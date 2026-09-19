import { EditorToolbar } from './components/EditorToolbar';
import { SidebarLeft } from './components/SidebarLeft';
import { SidebarRight } from './components/SidebarRight';
import { CanvasArea } from './components/CanvasArea';
import { useNavigate } from 'react-router-dom';
import { Eye, FlaskConical, Save } from 'lucide-react';

export const TemplateEditor = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden fixed inset-0 z-50">
      <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 shrink-0 z-10">
        <div className="flex items-center text-sm font-medium text-slate-500 space-x-2">
          <span className="cursor-pointer hover:text-slate-900 transition-colors" onClick={() => navigate('/templates')}>Templates</span>
          <span>›</span>
          <span className="text-slate-900">Workshop Certificate</span>
          <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded-md text-xs ml-3 font-bold">v2</span>
          <span className="flex items-center text-green-600 text-xs ml-4 font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5"></span> Saved
          </span>
        </div>
        
        <div className="flex items-center space-x-3">
          <button className="flex items-center px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors shadow-sm">
            <Eye size={16} className="mr-2 text-slate-400" /> Preview
          </button>
          <button className="flex items-center px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors shadow-sm">
            <FlaskConical size={16} className="mr-2 text-slate-400" /> Generate Test
          </button>
          <button className="flex items-center px-5 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-semibold text-white transition-colors shadow-sm shadow-blue-600/20">
            <Save size={16} className="mr-2" /> Save Template
          </button>
        </div>
      </header>

      <EditorToolbar />

      <div className="flex flex-1 overflow-hidden">
        <SidebarLeft />
        <CanvasArea />
        <SidebarRight />
      </div>
    </div>
  );
};
