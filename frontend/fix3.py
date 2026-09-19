import os

with open('src/features/events/EventWorkspace.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace template literals with string concatenation
content = content.replace("navigate(/participants?event=)", "navigate('/participants?event=' + event.id)")
content = content.replace("navigate(/templates/new?event=)", "navigate('/templates/new?event=' + event.id)")
content = content.replace("navigate(/generation?event=)", "navigate('/generation?event=' + event.id)")
content = content.replace("navigate(/certificates?event=)", "navigate('/certificates?event=' + event.id)")

with open('src/features/events/EventWorkspace.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

with open('src/features/events/EventList.tsx', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("navigate(/events/)", "navigate('/events/' + evt.id)")
with open('src/features/events/EventList.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

with open('src/features/events/EventCreate.tsx', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("navigate(/events/)", "navigate('/events/' + data.id)")
with open('src/features/events/EventCreate.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

with open('src/api/events.ts', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("/events/", "'/events/' + id")
with open('src/api/events.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed template strings")
