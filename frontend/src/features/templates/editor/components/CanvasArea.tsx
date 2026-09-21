import { useEditorStore } from '../../../../store/editorStore';
import type { EditorElement } from '../../../../store/editorStore';
import { Stage, Layer, Rect, Text, Image as KonvaImageComponent } from 'react-konva';
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
  

  // Generate ruler ticks (every 10mm, major tick every 50mm)
  const renderTopRuler = () => {
    const ticks = [];
    for (let i = 0; i <= pageSize.width; i += 10) {
      const isMajor = i % 50 === 0;
      ticks.push(
        <div key={i} className={"absolute bottom-0 border-l border-slate-300 " + (isMajor ? "h-3" : "h-1.5")} style={{ left: i * MM_TO_PX * zoom }}>
          {isMajor && <span className="absolute -top-4 -left-2 text-[10px] text-slate-500">{i}</span>}
        </div>
      );
    }
    return <div className="absolute top-0 left-6 right-0 h-6 border-b border-slate-200 bg-white/80 overflow-hidden">{ticks}</div>;
  };

  const renderLeftRuler = () => {
    const ticks = [];
    for (let i = 0; i <= pageSize.height; i += 10) {
      const isMajor = i % 50 === 0;
      ticks.push(
        <div key={i} className={"absolute right-0 border-t border-slate-300 " + (isMajor ? "w-3" : "w-1.5")} style={{ top: i * MM_TO_PX * zoom }}>
          {isMajor && <span className="absolute -left-6 -top-2 text-[10px] text-slate-500 w-5 text-right">{i}</span>}
        </div>
      );
    }
    return <div className="absolute top-6 left-0 bottom-0 w-6 border-r border-slate-200 bg-white/80 overflow-hidden">{ticks}</div>;
  };

  return (
    <div className="flex-1 bg-slate-100/50 overflow-auto relative flex items-center justify-center p-12" ref={containerRef}>
      
      {/* Rulers Container */}
      <div className="absolute inset-0 pointer-events-none z-10">
        {renderTopRuler()}
        {renderLeftRuler()}
      </div>
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

const KonvaImage = ({ el, xPx, yPx, wPx, hPx, isSelected, onSelect, onChange, zoom }: any) => {
  const [img, setImg] = useState<HTMLImageElement | null>(null);

  useEffect(() => {
    if (el.src) {
      const image = new window.Image();
      image.src = el.src;
      image.onload = () => {
        setImg(image);
      };
    }
  }, [el.src]);

  return (
    <>
      {img && (
        <KonvaImageComponent
          image={img}
          x={xPx}
          y={yPx}
          width={wPx}
          height={hPx}
          rotation={el.rotation}
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
      )}
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
};

const EditableElement = ({ el, isSelected, onSelect, onChange, zoom }: { el: EditorElement, isSelected: boolean, onSelect: () => void, onChange: (attrs: any) => void, zoom: number }) => {
  const xPx = el.x * MM_TO_PX * zoom;
  const yPx = el.y * MM_TO_PX * zoom;
  const wPx = el.width * MM_TO_PX * zoom;
  const hPx = el.height * MM_TO_PX * zoom;

  if (el.type === 'image') {
    return (
      <KonvaImage
        el={el}
        xPx={xPx}
        yPx={yPx}
        wPx={wPx}
        hPx={hPx}
        isSelected={isSelected}
        onSelect={onSelect}
        onChange={onChange}
        zoom={zoom}
      />
    );
  }

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
