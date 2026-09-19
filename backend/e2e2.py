import requests
import json
import time
import os

API_URL = 'http://localhost:8001'
test_results = {}

def report(test_name, success, error=''):
    test_results[test_name] = {'success': success, 'error': error}
    if success:
        print(f'[PASS] {test_name}')
    else:
        print(f'[FAIL] {test_name}: {error}')

try:
    # 5. AUTHENTICATION TEST
    print('\n--- AUTHENTICATION TEST ---')
    resp = requests.post(f'{API_URL}/login', data={'username': 'admin@certify.com', 'password': 'securepassword123'})
    if resp.status_code == 200:
        token = resp.json().get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        report('Login', True)
    else:
        report('Login', False, resp.text)
        exit(1)
        
    resp = requests.get(f'{API_URL}/events/', headers=headers)
    if resp.status_code == 200:
        report('Protected Route Access', True)
    else:
        report('Protected Route Access', False, resp.text)

    # 6. EVENT CREATION TEST
    print('\n--- EVENT CREATION TEST ---')
    event_payload = {
        'name': 'CERTIFY E2E VALIDATION ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 2026',
        'date': '2026-09-19',
        'location': 'Test Environment',
        'description': 'E2E Validation Event'
    }
    resp = requests.post(f'{API_URL}/events/', json=event_payload, headers=headers)
    if resp.status_code == 200:
        event_id = resp.json().get('id')
        report('Create Event', True)
    else:
        report('Create Event', False, resp.text)
        exit(1)

    # 7. PARTICIPANT IMPORT TEST
    print('\n--- PARTICIPANT IMPORT TEST ---')
    import csv, io
    csv_data = io.StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['Name', 'Email', 'Role'])
    participants = [
        'Aarav Sharma', 'Ananya Rao', 'Rohan Mehta', 'Priya Sharma',
        'Nikhil Verma', 'Aishwarya Krishnan', 'Shanmukha Chennuboina',
        'Very Long Participant Name For Layout Testing', 'Dr. R. K. Sharma',
        'International Student Certificate Test'
    ]
    for p in participants:
        writer.writerow([p, f"{p.replace(' ', '').lower()}@test.com", 'Attendee'])
        
    files = {'file': ('participants.csv', csv_data.getvalue(), 'text/csv')}
    resp = requests.post(f'{API_URL}/participants/{event_id}/upload', files=files, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data.get('valid') == 10:
            report('Participant Import', True)
        else:
            report('Participant Import', False, f"Expected 10, got {data.get('valid')}")
    else:
        report('Participant Import', False, resp.text)
        
    resp = requests.get(f'{API_URL}/participants/{event_id}', headers=headers)
    if len(resp.json()) == 10:
        report('Participant Count Match', True)
    else:
        report('Participant Count Match', False, 'Count != 10')

    # 8. TEMPLATE CREATION
    print('\n--- TEMPLATE CREATION TEST ---')
    resp = requests.post(f'{API_URL}/templates/', data={'name': 'A4 Landscape E2E'}, headers=headers)
    if resp.status_code == 200:
        template_id = resp.json().get('id')
        report('Create Template', True)
    else:
        report('Create Template', False, resp.text)
        exit(1)

    elements = [
        {'type': 'text', 'field': 'NAME', 'x_mm': 148, 'y_mm': 105, 'font_family': 'Helvetica', 'font_size': 24, 'alignment': 'center', 'auto_fit': True, 'width_mm': 150},
        {'type': 'text', 'field': 'EVENT_NAME', 'x_mm': 148, 'y_mm': 130, 'font_family': 'Helvetica', 'font_size': 16, 'alignment': 'center', 'auto_fit': True, 'width_mm': 150},
        {'type': 'text', 'field': 'DATE', 'x_mm': 50, 'y_mm': 180, 'font_family': 'Helvetica', 'font_size': 12, 'alignment': 'left', 'auto_fit': False, 'width_mm': 50},
        {'type': 'text', 'field': 'CERTIFICATE_ID', 'x_mm': 250, 'y_mm': 180, 'font_family': 'Helvetica', 'font_size': 10, 'alignment': 'right', 'auto_fit': False, 'width_mm': 40}
    ]
    config = {'page': {'width_mm': 297, 'height_mm': 210}, 'elements': elements}
    
    resp = requests.post(f'{API_URL}/templates/{template_id}/versions', json={'configuration': config}, headers=headers)
    if resp.status_code == 200:
        version_id = resp.json().get('id')
        report('Save Template Version', True)
    else:
        report('Save Template Version', False, resp.text)
        
    # 9. TEST CERTIFICATE GENERATION
    print('\n--- TEST CERTIFICATE GENERATION ---')
    resp = requests.post(f'{API_URL}/templates/{template_id}/versions/{version_id}/test', headers=headers)
    if resp.status_code == 200 and resp.headers.get('content-type') == 'application/pdf':
        report('Test Certificate PDF', True)
    else:
        report('Test Certificate PDF', False, f'Status: {resp.status_code}')
        
    # 10. BULK GENERATION
    print('\n--- BULK GENERATION TEST ---')
    resp = requests.post(f'{API_URL}/generation/{event_id}', headers=headers)
    if resp.status_code == 200:
        job_id = resp.json().get('job_id')
        report('Start Generation Job', True)
    else:
        report('Start Generation Job', False, resp.text)
        
    completed = False
    for i in range(15):
        resp = requests.get(f'{API_URL}/generation/{event_id}', headers=headers)
        if resp.status_code == 200:
            jobs = resp.json()
            if jobs and jobs[0]['status'] == 'COMPLETED':
                completed = True
                break
        time.sleep(1)
        
    if completed:
        report('Celery Processing', True)
    else:
        report('Celery Processing', False, 'Job did not complete within 15 seconds')

    # 11. DATABASE CONSISTENCY
    print('\n--- DATABASE CONSISTENCY TEST ---')
    resp = requests.get(f'{API_URL}/certificates/', headers=headers)
    if resp.status_code == 200:
        certs = [c for c in resp.json() if c.get('event_name') == 'CERTIFY E2E VALIDATION ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 2026']
        if len(certs) == 10:
            report('Database Consistency (10 certs)', True)
            test_cert_id = certs[0]['certificate_id']
        else:
            report('Database Consistency (10 certs)', False, f'Found {len(certs)} certs')
    else:
        report('Database Consistency', False, resp.text)

    # 12. IDEMPOTENCY
    print('\n--- IDEMPOTENCY TEST ---')
    resp = requests.post(f'{API_URL}/generation/{event_id}', headers=headers)
    if resp.status_code == 400 and 'already in progress' in resp.text:
        pass
    
    time.sleep(2)
    resp = requests.get(f'{API_URL}/certificates/', headers=headers)
    certs_after = [c for c in resp.json() if c.get('event_name') == 'CERTIFY E2E VALIDATION ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 2026']
    if len(certs_after) == 10:
        report('Idempotency (No Duplicates)', True)
    else:
        report('Idempotency (No Duplicates)', False, f'Found {len(certs_after)} certs instead of 10')
        
    # 13. CERTIFICATE DOWNLOAD
    print('\n--- CERTIFICATE DOWNLOAD TEST ---')
    resp = requests.get(f'{API_URL}/certificates/{test_cert_id}/download', headers=headers)
    if resp.status_code == 200 and resp.headers.get('content-type') == 'application/pdf':
        report('Certificate Download', True)
    else:
        report('Certificate Download', False, str(resp.status_code))

    # 14. PUBLIC VERIFICATION
    print('\n--- PUBLIC VERIFICATION TEST ---')
    resp = requests.get(f'{API_URL}/certificates/verify/{test_cert_id}')
    if resp.status_code == 200 and resp.json().get('status') == 'VALID':
        report('Public Verification (Valid)', True)
    else:
        report('Public Verification (Valid)', False, resp.text)

    # 15. REVOCATION
    print('\n--- REVOCATION TEST ---')
    resp = requests.post(f'{API_URL}/certificates/{test_cert_id}/revoke', json={'reason': 'E2E revocation test'}, headers=headers)
    if resp.status_code == 200:
        report('Revocation API', True)
    else:
        report('Revocation API', False, resp.text)
        
    resp = requests.get(f'{API_URL}/certificates/verify/{test_cert_id}')
    if resp.status_code == 400 and 'REVOKED' in resp.text:
        report('Public Verification (Revoked)', True)
    else:
        report('Public Verification (Revoked)', False, resp.text)

    # 16. INVALID CERTIFICATE
    print('\n--- INVALID CERTIFICATE TEST ---')
    resp = requests.get(f'{API_URL}/certificates/verify/CERTIFY-E2E-NOT-REAL-999999')
    if resp.status_code == 404:
        report('Public Verification (Invalid)', True)
    else:
        report('Public Verification (Invalid)', False, str(resp.status_code))

except Exception as e:
    print(f'Exception during tests: {e}')