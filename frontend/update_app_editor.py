import os

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
import_line = "import { TemplateEditor } from './features/templates/editor/TemplateEditor';\n"
if "TemplateEditor" not in content:
    content = content.replace("import { EventWorkspace } from './features/events/EventWorkspace';", "import { EventWorkspace } from './features/events/EventWorkspace';\n" + import_line)

# Add route
route_line = '''
          <Route path="/templates/new" element={<ProtectedRoute><TemplateEditor /></ProtectedRoute>} />
'''
if "/templates/new" not in content:
    content = content.replace("<Route path=\"/login\" element={<Login />} />", "<Route path=\"/login\" element={<Login />} />" + route_line)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
