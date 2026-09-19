import os

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import_line = "import { GenerationCenter } from './features/generation/GenerationCenter';\n"
if "GenerationCenter" not in content:
    content = content.replace("import { TemplateEditor } from './features/templates/editor/TemplateEditor';", "import { TemplateEditor } from './features/templates/editor/TemplateEditor';\n" + import_line)

content = content.replace("<Route path=\"generation\" element={<div className=\"p-8\">Generation placeholder</div>} />", "<Route path=\"generation\" element={<GenerationCenter />} />")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
