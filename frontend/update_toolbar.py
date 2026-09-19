import os

with open('src/features/templates/editor/components/EditorToolbar.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import_line = "import { createTemplate, createTemplateVersion, generateTestCertificate } from '../../../../api/templates';\n"
if "createTemplate" not in content:
    content = import_line + content

save_logic = '''
  const [isSaving, setIsSaving] = React.useState(false);
  const [savedVersionId, setSavedVersionId] = React.useState<number | null>(null);
  const [savedTemplateId, setSavedTemplateId] = React.useState<number | null>(null);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // 1. Create Template (no file for now, assuming white background or already uploaded)
      const tpl = await createTemplate('My Event Template');
      setSavedTemplateId(tpl.id);
      
      // 2. Map Elements
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

      const config = {
        page: { width_mm: 297, height_mm: 210 },
        elements: mappedElements
      };

      // 3. Create Version
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
'''

# Find the start of the component to inject state
if 'handleSave' not in content:
    content = content.replace('export const EditorToolbar = () => {\n  const { zoom, setZoom', save_logic + 'export const EditorToolbar = () => {\n  const { zoom, setZoom, elements } = useEditorStore();')
    
    # Replace the buttons
    content = content.replace('<button className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-sm rounded-lg transition-colors">\n          Generate Test\n        </button>', 
    '<button onClick={handleTest} className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-sm rounded-lg transition-colors">Generate Test</button>')
    
    content = content.replace('<button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm rounded-lg shadow-sm transition-colors">\n          Save Template\n        </button>',
    '<button onClick={handleSave} disabled={isSaving} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold text-sm rounded-lg shadow-sm transition-colors">{isSaving ? "Saving..." : "Save Template"}</button>')

with open('src/features/templates/editor/components/EditorToolbar.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Toolbar updated")
