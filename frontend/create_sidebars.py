import os

files = {
    'src/features/templates/editor/components/EditorToolbar.tsx': '''import { useEditorStore } from '../../../../store/editorStore';
import { Undo, Redo, ZoomOut, ZoomIn, Hand } from 'lucide-react';

export const EditorToolbar = () => {
  const { zoom, setZoom, showGrid, setShowGrid, snapToGrid, setSnapToGrid } = useEditorStore();

  return (
    <div className="h-14 bg-white border-b border-slate-200 flex items-center justify-between px-6 shrink-0">
      <div className="flex items-center space-x-4">
        <button className="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
          <Undo size={18} />
        </button>
        <button className="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
          <Redo size={18} />
        </button>
        
        <div className="h-6 w-px bg-slate-200 mx-2"></div>
        
        <div className="flex items-center border border-slate-200 rounded-lg overflow-hidden h-9 bg-white">
          <button 
            onClick={() => setZoom(Math.max(0.25, zoom - 0.25))}
            className="px-3 text-slate-500 hover:bg-slate-50 hover:text-slate-900 transition-colors"
          >
            <ZoomOut size={16} />
          </button>
          <span className="text-sm font-medium text-slate-700 min-w-[60px] text-center border-x border-slate-200 px-2">
            {Math.round(zoom * 100)}%
          </span>
          <button 
            onClick={() => setZoom(Math.min(3, zoom + 0.25))}
            className="px-3 text-slate-500 hover:bg-slate-50 hover:text-slate-900 transition-colors"
          >
            <ZoomIn size={16} />
          </button>
        </div>
        
        <button className="p-2 ml-4 text-slate-600 bg-slate-100 rounded-lg transition-colors">
          <Hand size={18} />
        </button>
      </div>

      <div className="flex items-center space-x-8">
        <div className="flex items-center space-x-3 text-sm">
          <span className="text-slate-700 font-medium">A4 (297 x 210 mm)</span>
          <span className="text-slate-400">∨</span>
        </div>
        
        <div className="h-6 w-px bg-slate-200"></div>

        <div className="flex items-center space-x-6 text-sm font-medium text-slate-700">
          <label className="flex items-center cursor-pointer select-none">
            <input 
              type="checkbox" 
              className="mr-2 w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500" 
              checked={showGrid}
              onChange={(e) => setShowGrid(e.target.checked)}
            />
            Grid
          </label>
          <label className="flex items-center cursor-pointer select-none">
            <input 
              type="checkbox" 
              className="mr-2 w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500" 
              checked={snapToGrid}
              onChange={(e) => setSnapToGrid(e.target.checked)}
            />
            Snap
          </label>
        </div>
      </div>
    </div>
  );
};
''',

    'src/features/templates/editor/components/SidebarLeft.tsx': '''import { useEditorStore } from '../../../../store/editorStore';
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
''',

    'src/features/templates/editor/components/SidebarRight.tsx': '''import { useEditorStore } from '../../../../store/editorStore';
import { AlignLeft, AlignCenter, AlignRight, Trash2 } from 'lucide-react';

export const SidebarRight = () => {
  const { elements, selectedElementId, updateElement, removeElement } = useEditorStore();
  
  const element = elements.find(el => el.id === selectedElementId);

  if (!element) {
    return (
      <div className="w-[320px] bg-white border-l border-slate-200 flex flex-col items-center justify-center h-full shrink-0 p-8 text-center text-slate-500">
        Select an element to edit its properties.
      </div>
    );
  }

  const handleChange = (updates: any) => {
    updateElement(element.id, updates);
  };

  return (
    <div className="w-[320px] bg-white border-l border-slate-200 flex flex-col h-full shrink-0 overflow-y-auto custom-scrollbar">
      <div className="p-5 pb-0 border-b border-slate-100">
        <h3 className="text-xs font-bold text-slate-900 tracking-wider mb-4 uppercase">Properties</h3>
        <div className="flex space-x-6 border-b border-slate-200">
          <button className="pb-3 text-sm font-semibold text-blue-600 border-b-2 border-blue-600 px-2">Text</button>
          <button className="pb-3 text-sm font-medium text-slate-500 hover:text-slate-900 px-2 transition-colors">Style</button>
          <button className="pb-3 text-sm font-medium text-slate-500 hover:text-slate-900 px-2 transition-colors">Arrange</button>
        </div>
      </div>

      <div className="p-6 space-y-8 flex-1">
        
        {/* Content */}
        {element.type === 'text' && (
          <div>
            <h4 className="text-sm font-bold text-slate-900 mb-3">Content</h4>
            <textarea 
              value={element.content}
              onChange={(e) => handleChange({ content: e.target.value })}
              className="w-full border border-slate-200 rounded-xl p-3 text-sm bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all resize-none"
              rows={3}
            />
          </div>
        )}

        {/* Typography */}
        {element.type === 'text' && (
          <div>
            <h4 className="text-sm font-bold text-slate-900 mb-3">Typography</h4>
            <div className="space-y-4">
              <div>
                <label className="text-xs text-slate-500 mb-1.5 block">Font</label>
                <select 
                  value={element.fontFamily}
                  onChange={(e) => handleChange({ fontFamily: e.target.value })}
                  className="w-full border border-slate-200 rounded-lg p-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Arial">Arial</option>
                  <option value="Playfair Display">Playfair Display</option>
                  <option value="Times New Roman">Times New Roman</option>
                  <option value="Inter">Inter</option>
                </select>
              </div>
              
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-slate-500 mb-1.5 block">Size (pt)</label>
                  <input 
                    type="number" 
                    value={element.fontSize}
                    onChange={(e) => handleChange({ fontSize: Number(e.target.value) })}
                    className="w-full border border-slate-200 rounded-lg p-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-500 mb-1.5 block">Weight</label>
                  <select 
                    value={element.fontWeight}
                    onChange={(e) => handleChange({ fontWeight: e.target.value })}
                    className="w-full border border-slate-200 rounded-lg p-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="normal">Normal</option>
                    <option value="bold">Bold</option>
                  </select>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-xs text-slate-500 mb-1.5 block">Color</label>
                  <div className="flex items-center space-x-2 border border-slate-200 rounded-lg p-2 bg-white w-32">
                    <input 
                      type="color" 
                      value={element.color}
                      onChange={(e) => handleChange({ color: e.target.value })}
                      className="w-6 h-6 rounded cursor-pointer border-0 p-0"
                    />
                    <span className="text-xs text-slate-600 font-medium uppercase">{element.color}</span>
                  </div>
                </div>
              </div>

              <div>
                <label className="text-xs text-slate-500 mb-1.5 block">Text Alignment</label>
                <div className="flex bg-slate-100 p-1 rounded-lg">
                  <button 
                    onClick={() => handleChange({ textAlign: 'left' })}
                    className={"flex-1 flex justify-center p-2 rounded-md transition-colors " + (element.textAlign === 'left' ? "bg-white shadow-sm text-blue-600" : "text-slate-500")}
                  >
                    <AlignLeft size={16} />
                  </button>
                  <button 
                    onClick={() => handleChange({ textAlign: 'center' })}
                    className={"flex-1 flex justify-center p-2 rounded-md transition-colors " + (element.textAlign === 'center' ? "bg-white shadow-sm text-blue-600" : "text-slate-500")}
                  >
                    <AlignCenter size={16} />
                  </button>
                  <button 
                    onClick={() => handleChange({ textAlign: 'right' })}
                    className={"flex-1 flex justify-center p-2 rounded-md transition-colors " + (element.textAlign === 'right' ? "bg-white shadow-sm text-blue-600" : "text-slate-500")}
                  >
                    <AlignRight size={16} />
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Position & Size */}
        <div>
          <h4 className="text-sm font-bold text-slate-900 mb-3">Position & Size</h4>
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center border border-slate-200 rounded-lg p-2 bg-white">
              <span className="text-xs font-semibold text-slate-400 w-6">X</span>
              <input type="number" value={element.x.toFixed(2)} onChange={(e) => handleChange({ x: Number(e.target.value) })} className="w-full text-sm font-medium text-slate-900 focus:outline-none" />
              <span className="text-xs text-slate-400">mm</span>
            </div>
            <div className="flex items-center border border-slate-200 rounded-lg p-2 bg-white">
              <span className="text-xs font-semibold text-slate-400 w-6">Y</span>
              <input type="number" value={element.y.toFixed(2)} onChange={(e) => handleChange({ y: Number(e.target.value) })} className="w-full text-sm font-medium text-slate-900 focus:outline-none" />
              <span className="text-xs text-slate-400">mm</span>
            </div>
            <div className="flex items-center border border-slate-200 rounded-lg p-2 bg-white">
              <span className="text-xs font-semibold text-slate-400 w-6">W</span>
              <input type="number" value={element.width.toFixed(2)} onChange={(e) => handleChange({ width: Number(e.target.value) })} className="w-full text-sm font-medium text-slate-900 focus:outline-none" />
              <span className="text-xs text-slate-400">mm</span>
            </div>
            <div className="flex items-center border border-slate-200 rounded-lg p-2 bg-white">
              <span className="text-xs font-semibold text-slate-400 w-6">H</span>
              <input type="number" value={element.height.toFixed(2)} onChange={(e) => handleChange({ height: Number(e.target.value) })} className="w-full text-sm font-medium text-slate-900 focus:outline-none" />
              <span className="text-xs text-slate-400">mm</span>
            </div>
          </div>
        </div>

        {/* Auto Fit */}
        {element.type === 'text' && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-sm font-bold text-slate-900">Auto-fit</h4>
              <div className="w-10 h-6 bg-blue-600 rounded-full relative cursor-pointer">
                <div className="w-4 h-4 bg-white rounded-full absolute top-1 right-1"></div>
              </div>
            </div>
            <div className="space-y-3 pl-4 border-l-2 border-slate-100">
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-600">Minimum font size</span>
                <div className="flex items-center border border-slate-200 rounded-lg px-2 py-1 w-24">
                  <input type="number" value="24" className="w-full outline-none font-medium text-slate-900 text-right pr-2" readOnly/>
                  <span className="text-xs text-slate-400">pt</span>
                </div>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-600">Maximum width</span>
                <div className="flex items-center border border-slate-200 rounded-lg px-2 py-1 w-24">
                  <input type="number" value="180" className="w-full outline-none font-medium text-slate-900 text-right pr-2" readOnly/>
                  <span className="text-xs text-slate-400">mm</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="p-6 mt-auto">
        <button 
          onClick={() => removeElement(element.id)}
          className="w-full flex items-center justify-center px-4 py-3 bg-red-50 hover:bg-red-100 text-red-600 font-bold text-sm rounded-xl transition-colors"
        >
          <Trash2 size={16} className="mr-2" />
          Delete Element
        </button>
      </div>
    </div>
  );
};
'''
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
