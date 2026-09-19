import os

with open('src/features/generation/GenerationCenter.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("style={{ width: ${percentage}% }}", "style={{ width: percentage + '%' }}")

with open('src/features/generation/GenerationCenter.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
