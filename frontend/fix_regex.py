import os

with open('src/api/generation.ts', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("/generation/", "'/generation/' + eventId")
with open('src/api/generation.ts', 'w', encoding='utf-8') as f:
    f.write(content)

with open('src/features/generation/GenerationCenter.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("navigate(/events/)", "navigate('/events/' + eventId)")
with open('src/features/generation/GenerationCenter.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed")
