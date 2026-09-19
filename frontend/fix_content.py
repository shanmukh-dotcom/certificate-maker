import os

with open('src/features/templates/editor/components/EditorToolbar.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("el.content.replace", "(el.content || '').replace")

with open('src/features/templates/editor/components/EditorToolbar.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed content undefined error")
