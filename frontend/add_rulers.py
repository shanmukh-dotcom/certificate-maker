import os

with open('src/features/templates/editor/components/CanvasArea.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

ruler_code = '''
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
'''

# Find the return statement of CanvasArea to inject rulers
if 'renderTopRuler' not in content:
    content = content.replace('  return (\n    <div className="flex-1 bg-slate-100/50 overflow-auto relative flex items-center justify-center p-12"',
ruler_code + '''
  return (
    <div className="flex-1 bg-slate-100/50 overflow-auto relative flex items-center justify-center p-12"''')

    content = content.replace('<div \n        className="bg-white shadow-xl relative"',
'''
      {/* Rulers Container */}
      <div className="absolute inset-0 pointer-events-none z-10">
        {renderTopRuler()}
        {renderLeftRuler()}
      </div>
      <div 
        className="bg-white shadow-xl relative"''')

with open('src/features/templates/editor/components/CanvasArea.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
