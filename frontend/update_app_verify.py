import os

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import_line = "import { PublicVerification } from './features/verification/PublicVerification';\n"
if "PublicVerification" not in content:
    content = content.replace("import { CertificateManager } from './features/certificates/CertificateManager';", "import { CertificateManager } from './features/certificates/CertificateManager';\n" + import_line)

route_line = '''
          <Route path="/verify" element={<PublicVerification />} />
'''
if "/verify" not in content:
    content = content.replace("<Route path=\"/login\" element={<Login />} />", "<Route path=\"/login\" element={<Login />} />" + route_line)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
