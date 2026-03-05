import json
import os

def parse_sarif(sarif_path):
    """Parse SARIF or return demo data"""
    if not os.path.exists(sarif_path):
        # Demo issues for testing
        return [
            {
                'rule_id': 'naming-convention',
                'severity': 'warning',
                'message': 'Use snake_case for variables (studentName → student_name)',
                'line': 45,
                'file': 'main.py'
            },
            {
                'rule_id': 'uninit-variable',
                'severity': 'error',
                'message': 'Variable not initialized before use',
                'line': 128,
                'file': 'utils.py'
            },
            {
                'rule_id': 'complex-function',
                'severity': 'warning',
                'message': 'Function complexity too high (12 paths)',
                'line': 200,
                'file': 'main.py'
            }
        ]
    
    # Real SARIF parsing
    with open(sarif_path, 'r') as f:
        data = json.load(f)
    issues = []
    for run in data.get('runs', []):
        for result in run.get('results', []):
            issues.append({
                'rule_id': result.get('ruleId', 'unknown'),
                'severity': result.get('level', 'note'),
                'message': result['message']['text'],
                'line': result['locations'][0]['physicalLocation'].get('startLine', 0),
                'file': result['locations'][0]['physicalLocation'].get('artifactLocation', {}).get('uri', 'unknown')
            })
    return issues[:10]  # Limit
