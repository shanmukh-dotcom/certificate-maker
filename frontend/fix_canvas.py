import os

with open('src/features/templates/editor/components/CanvasArea.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import { useEditorStore, EditorElement } from", "import { useEditorStore } from '../../../../store/editorStore';\nimport type { EditorElement } from")
content = content.replace("import { useRef, useEffect, useState }", "import { useRef }")

with open('src/features/templates/editor/components/CanvasArea.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
