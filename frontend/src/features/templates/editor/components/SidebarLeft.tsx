import { useEditorStore } from '../../../../store/editorStore';
import { Type, Image as ImageIcon, Square, Minus, User, Calendar, Tag, Briefcase, Building, Plus, Lock, Eye, GripVertical } from 'lucide-react';

export const SidebarLeft = () => {
  const { elements, selectedElementId, setSelectedElement, addElement } = useEditorStore();

  const handleAddText = (content: string, name: string) => {
    addElement({
      id: Date.now().toString(),
      type: 'text',
      name: name,
      content: content,
      x: 100,
      y: 100,
      width: 100,
      height: 20,
      rotation: 0,
      isLocked: false,
      fontFamily: 'Arial',
      fontSize: 24,
      color: '#000000',
      textAlign: 'center'
    });
  };

  return (
    <div className="w-[280px] bg-white border-r border-slate-200 flex flex-col h-full shrink-0 overflow-y-auto custom-scrollbar">
      <div className="p-5 border-b border-slate-100">
        <h3 className="text-xs font-bold text-slate-900 tracking-wider mb-4 uppercase">Elements</h3>
        <div className="space-y-2">
          <button onClick={() => handleAddText('Double click to edit', 'Text Block')} className="w-full flex items-center px-4 py-2.5 bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded-xl text-sm font-medium transition-colors">
            <Type size={18} className="mr-3 text-slate-400" /> Text
          </button>
          <button className="w-full flex items-center px-4 py-2.5 bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded-xl text-sm font-medium transition-colors">
            <ImageIcon size={18} className="mr-3 text-slate-400" /> Image
          </button>
          <button className="w-full flex items-center px-4 py-2.5 bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded-xl text-sm font-medium transition-colors">
            <Square size={18} className="mr-3 text-slate-400" /> Shape
          </button>
          <button className="w-full flex items-center px-4 py-2.5 bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded-xl text-sm font-medium transition-colors">
            <Minus size={18} className="mr-3 text-slate-400" /> Line
          </button>
        </div>
      </div>

      <div className="p-5 border-b border-slate-100">
        <h3 className="text-xs font-bold text-slate-900 tracking-wider mb-4 uppercase">Dynamic Fields</h3>
        <div className="space-y-2 mb-4">
          <button onClick={() => handleAddText('{{NAME}}', 'Name')} className="w-full flex items-center px-4 py-2.5 bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded-xl text-sm font-medium transition-colors">
            <User size={18} className="mr-3 text-slate-400" /> Name
          </button>
          <button onClick={() => handleAddText('{{EVENT_NAME}}', 'Event Name')} className="w-full flex items-center px-4 py-2.5 bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded-xl text-sm font-medium transition-colors">
            <Calendar size={18} className="mr-3 text-slate-400" /> Event Name
          </button>
          <button onClick={() => handleAddText('{{DATE}}', 'Date')} className="w-full flex items-center px-4 py-2.5 bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded-xl text-sm font-medium transition-colors">
            <Calendar size={18} className="mr-3 text-slate-400" /> Date
          </button>
          <button onClick={() => handleAddText('{{ROLE}}', 'Role / Position')} className="w-full flex items-center px-4 py-2.5 bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded-xl text-sm font-medium transition-colors">
            <Briefcase size={18} className="mr-3 text-slate-400" /> Role / Position
          </button>
          <button onClick={() => handleAddText('{{CERTIFICATE_ID}}', 'Certificate ID')} className="w-full flex items-center px-4 py-2.5 bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded-xl text-sm font-medium transition-colors">
            <Tag size={18} className="mr-3 text-slate-400" /> Certificate ID
          </button>
          <button onClick={() => handleAddText('{{ORGANIZATION}}', 'Organization')} className="w-full flex items-center px-4 py-2.5 bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 rounded-xl text-sm font-medium transition-colors">
            <Building size={18} className="mr-3 text-slate-400" /> Organization
          </button>
        </div>
        <button className="w-full flex items-center justify-center px-4 py-2.5 border border-blue-200 text-blue-600 hover:bg-blue-50 rounded-xl text-sm font-medium transition-colors">
          <Plus size={18} className="mr-2" /> Add Custom Field
        </button>
      </div>

      <div className="p-5 flex-1">
        <h3 className="text-xs font-bold text-slate-900 tracking-wider mb-4 uppercase">Layers</h3>
        <div className="space-y-1">
          {elements.map(el => (
            <div 
              key={el.id}
              onClick={() => setSelectedElement(el.id)}
              className={"flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer text-sm transition-colors " +
                (selectedElementId === el.id ? "bg-blue-50 text-blue-700" : "hover:bg-slate-50 text-slate-700")}
            >
              <div className="flex items-center space-x-3 truncate">
                <Lock size={14} className="text-slate-400 shrink-0" />
                <span className="truncate font-medium">{el.name}</span>
              </div>
              <div className="flex items-center space-x-2 shrink-0 opacity-50 hover:opacity-100">
                <Eye size={14} className="text-slate-400" />
                <GripVertical size={14} className="text-slate-400 cursor-grab" />
              </div>
            </div>
          )).reverse()}
        </div>
      </div>
    </div>
  );
};
