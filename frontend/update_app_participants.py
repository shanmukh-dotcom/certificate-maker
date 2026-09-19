import os

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import_line = "import { ParticipantsManager } from './features/participants/ParticipantsManager';\n"
if "ParticipantsManager" not in content:
    content = content.replace("import { CertificateManager } from './features/certificates/CertificateManager';", "import { CertificateManager } from './features/certificates/CertificateManager';\n" + import_line)

content = content.replace("<Route path=\"participants\" element={<div className=\"p-8\">Participants placeholder</div>} />", "<Route path=\"participants\" element={<ParticipantsManager />} />")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
