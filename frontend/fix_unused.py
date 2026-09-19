import os

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove unused React imports if any
    content = content.replace("import React, { useState } from 'react';", "import { useState } from 'react';")
    content = content.replace("import React from 'react';\n", "")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('src/components/layout/AppLayout.tsx')
fix_file('src/features/dashboard/Dashboard.tsx')
fix_file('src/features/events/EventList.tsx')

# Fix EventWorkspace specifically
with open('src/features/events/EventWorkspace.tsx', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("(s, idx) =>", "(s) =>")
with open('src/features/events/EventWorkspace.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

