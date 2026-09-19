import os

with open('src/features/templates/editor/components/EditorToolbar.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's completely rewrite EditorToolbar.tsx safely instead of replace matching.
full_content = """import React from 'react';
import { ZoomIn, ZoomOut, Save, Download, Grid, Maximize, MousePointer2 } from 'lucide-react';
import { useEditorStore } from '../../../../store/editorStore';
import { createTemplate, createTemplateVersion, generateTestCertificate } from '../../../../api/templates';

export const EditorToolbar = () => {
  const { zoom, setZoom, elements } = useEditorStore();
  const [isSaving, setIsSaving] = React.useState(false);
  const [savedVersionId, setSavedVersionId] = React.useState<number | null>(null);
  const [savedTemplateId, setSavedTemplateId] = React.useState<number | null>(null);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const tpl = await createTemplate('My Event Template');
      setSavedTemplateId(tpl.id);
      const mappedElements = elements.map(el => ({
        type: 'text',
        field: el.content.replace('{{', '').replace('}}', ''),
        x_mm: el.x,
        y_mm: el.y,
        width_mm: el.width,
        font_family: el.fontFamily,
        font_size: el.fontSize,
        alignment: el.textAlign,
        auto_fit: el.autoFit || true
      }));
      const config = { page: { width_mm: 297, height_mm: 210 }, elements: mappedElements };
      const version = await createTemplateVersion(tpl.id, config);
      setSavedVersionId(version.id);
      alert('Template saved successfully!');
    } catch (err) {
      console.error(err);
      alert('Failed to save template');
    } finally {
      setIsSaving(false);
    }
  };

  const handleTest = async () => {
    if (!savedTemplateId || !savedVersionId) {
      alert('Please save the template first.');
      return;
    }
    try {
      const blob = await generateTestCertificate(savedTemplateId, savedVersionId);
      const url = window.URL.createObjectURL(blob);
      window.open(url);
    } catch (err) {
      console.error(err);
      alert('Failed to generate test certificate');
    }
  };

  return (
    <div className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between shrink-0 shadow-sm z-20">
      <div className="flex items-center space-x-4">
        <h1 className="font-bold text-slate-900 flex items-center">
          <span className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center mr-3 text-white text-xs">A4</span>
          Certificate Layout
        </h1>
        <div className="h-6 w-px bg-slate-200 mx-2"></div>
        <div className="flex items-center bg-slate-100 rounded-lg p-1">
          <button className="p-1.5 bg-white text-slate-900 rounded-md shadow-sm text-xs font-bold flex items-center"><MousePointer2 size={14} className="mr-1.5"/> Select</button>
          <button className="p-1.5 text-slate-500 hover:text-slate-900 rounded-md text-xs font-bold flex items-center px-3"><Maximize size={14} className="mr-1.5"/> Pan</button>
        </div>
      </div>
      
      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-2 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200">
          <button onClick={() => setZoom(Math.max(0.25, zoom - 0.25))} className="p-1 text-slate-500 hover:text-blue-600 transition-colors"><ZoomOut size={16} /></button>
          <span className="text-xs font-bold text-slate-700 w-12 text-center">{Math.round(zoom * 100)}%</span>
          <button onClick={() => setZoom(Math.min(3, zoom + 0.25))} className="p-1 text-slate-500 hover:text-blue-600 transition-colors"><ZoomIn size={16} /></button>
        </div>
        
        <div className="flex items-center space-x-2">
          <button onClick={handleTest} className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-sm rounded-lg transition-colors flex items-center"><Download size={16} className="mr-2"/> Generate Test</button>
          <button onClick={handleSave} disabled={isSaving} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold text-sm rounded-lg shadow-sm transition-colors flex items-center"><Save size={16} className="mr-2"/> {isSaving ? 'Saving...' : 'Save Template'}</button>
        </div>
      </div>
    </div>
  );
};
"""

with open('src/features/templates/editor/components/EditorToolbar.tsx', 'w', encoding='utf-8') as f:
    f.write(full_content)

print("EditorToolbar rewritten")
