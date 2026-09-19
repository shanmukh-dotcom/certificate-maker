import sqlite3
conn = sqlite3.connect('certificate.db')
c = conn.cursor()
c.execute("UPDATE users SET role = 'ADMIN' WHERE email = 'admin@certify.com'")
conn.commit()
conn.close()
print('SQL update done')