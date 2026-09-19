import os

files = {
    'src/features/templates/editor/components/CanvasArea.tsx': '''import { useEditorStore, EditorElement } from '../../../../store/editorStore';
import { Stage, Layer, Rect, Text } from 'react-konva';
import { useRef, useEffect, useState } from 'react';

const MM_TO_PX = 3.7795275591; // 96 DPI

export const CanvasArea = () => {
  const { elements, selectedElementId, setSelectedElement, updateElement, zoom, pageSize } = useEditorStore();
  const containerRef = useRef<HTMLDivElement>(null);
  
  const stageWidth = pageSize.width * MM_TO_PX * zoom;
  const stageHeight = pageSize.height * MM_TO_PX * zoom;
  
  const handleSelect = (id: string) => {
    setSelectedElement(id);
  };
  
  return (
    <div className="flex-1 bg-slate-100/50 overflow-auto relative flex items-center justify-center p-12" ref={containerRef}>
      <div 
        className="bg-white shadow-xl relative"
        style={{ width: stageWidth, height: stageHeight }}
      >
        <Stage
          width={stageWidth}
          height={stageHeight}
          onClick={(e) => {
            if (e.target === e.target.getStage()) {
              setSelectedElement(null);
            }
          }}
        >
          <Layer>
            {elements.map((el) => (
              <EditableElement 
                key={el.id} 
                el={el} 
                isSelected={el.id === selectedElementId}
                onSelect={() => handleSelect(el.id)}
                onChange={(newAttrs) => updateElement(el.id, newAttrs)}
                zoom={zoom}
              />
            ))}
          </Layer>
        </Stage>
      </div>
    </div>
  );
};

const EditableElement = ({ el, isSelected, onSelect, onChange, zoom }: { el: EditorElement, isSelected: boolean, onSelect: () => void, onChange: (attrs: any) => void, zoom: number }) => {
  const xPx = el.x * MM_TO_PX * zoom;
  const yPx = el.y * MM_TO_PX * zoom;
  const wPx = el.width * MM_TO_PX * zoom;
  const hPx = el.height * MM_TO_PX * zoom;

  if (el.type === 'text') {
    return (
      <>
        <Text
          x={xPx}
          y={yPx}
          width={wPx}
          height={hPx}
          text={el.content}
          fontSize={(el.fontSize || 24) * zoom}
          fontFamily={el.fontFamily}
          fill={el.color}
          align={el.textAlign}
          fontStyle={el.fontWeight === 'bold' ? 'bold' : 'normal'}
          onClick={onSelect}
          onTap={onSelect}
          draggable={!el.isLocked}
          onDragEnd={(e) => {
            onChange({
              x: e.target.x() / (MM_TO_PX * zoom),
              y: e.target.y() / (MM_TO_PX * zoom)
            });
          }}
        />
        {isSelected && (
          <Rect
            x={xPx}
            y={yPx}
            width={wPx}
            height={hPx}
            stroke="#2563EB"
            strokeWidth={1}
            dash={[4, 4]}
          />
        )}
      </>
    );
  }
  return null;
};
''',

    'src/features/templates/editor/TemplateEditor.tsx': '''import { EditorToolbar } from './components/EditorToolbar';
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
'''
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
