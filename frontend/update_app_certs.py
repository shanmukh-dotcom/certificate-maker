import os

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import_line = "import { CertificateManager } from './features/certificates/CertificateManager';\n"
if "CertificateManager" not in content:
    content = content.replace("import { GenerationCenter } from './features/generation/GenerationCenter';", "import { GenerationCenter } from './features/generation/GenerationCenter';\n" + import_line)

content = content.replace("<Route path=\"certificates\" element={<div className=\"p-8\">Certificates placeholder</div>} />", "<Route path=\"certificates\" element={<CertificateManager />} />")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
