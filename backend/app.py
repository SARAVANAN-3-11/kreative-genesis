from flask import Flask, request, jsonify
from flask_cors import CORS
import ast
import re
import time
from collections import Counter

app = Flask(__name__)
CORS(app)

def analyze_code(code):
    start_time = time.time()
    bugs, style, security, complexity, dupe = 0, 0, 0, 0, 0
    issues = []
    
    # 1. SYNTAX CHECK
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            'score': 20, 'bugs': 1, 'style': 0, 'security': 0, 
            'complexity': 0, 'dupe': 0, 'issues': [f'🐛 Syntax Error: {str(e)[:100]}'], 'time': 50
        }
    
    # 2. COMPLEXITY ANALYSIS (Real cyclomatic-style)
    def count_complexity(node):
        complexity = 1  # Base complexity
        if isinstance(node, (ast.If, ast.While, ast.For, ast.Try)):
            complexity += 1
        if isinstance(node, ast.BoolOp):
            complexity += len(node.values)
        return complexity
    
    total_complexity = 0
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
            func_complexity = sum(count_complexity(child) for child in ast.walk(node))
            total_complexity += func_complexity
            
            # Function name style
            if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                style += 1
                issues.append(f"Line {node.lineno}: ❌ '{node.name}' → use snake_case")
            
            if func_complexity > 5:
                complexity += 1
                issues.append(f"Line {node.lineno}: ⚠️ '{node.name}' complexity={func_complexity}")
    
    # 3. SECURITY CHECKS
    if re.search(r'input\s*\(', code) and not re.search(r'int\s*\(\s*input|input\s*\(\s*.*\)\s*\.strip', code):
        security += 1
        issues.append("🔒 Unvalidated input() detected")
    
    if re.search(r'eval\s*\(|exec\s*\(', code):
        security += 2
        issues.append("🚨 DANGEROUS: eval() or exec() found")
    
    # 4. DUPLICATION DETECTION
    lines = [line.strip() for line in code.split('\n') if line.strip()]
    if lines:
        line_counts = Counter(lines)
        dupe_lines = sum(count - 1 for count in line_counts.values() if count > 1)
        dupe = min(50, (dupe_lines / len(lines)) * 100)
    else:
        dupe = 0
    
    # 5. BUGS (Simple patterns)
    if 'print(' in code and code.count('print') > 5:
        bugs += 1
        issues.append("🐛 Too many print statements")
    
    # 6. STYLE CHECKS
    if len([line for line in code.split('\n') if len(line) > 88]) > 3:
        style += 1
        issues.append("🎨 Lines longer than 88 chars")
    
    # FINAL SCORE
    score = max(0, 100 - bugs*20 - style*10 - security*25 - complexity*15 - int(dupe))
    
    return {
        'score': int(score),
        'bugs': bugs,
        'style': style,
        'security': security,
        'complexity': total_complexity,  # NOW SHOWS REAL NUMBER
        'dupe': int(dupe),
        'issues': issues[:8],
        'time': int((time.time() - start_time) * 1000)
    }

@app.route('/api/analyze', methods=['POST'])
def analyze():
    code = request.json.get('code', '')
    return jsonify(analyze_code(code))

if __name__ == '__main__':
    print("🚀 Code Quality Analyzer API - http://localhost:5000")
    print("📊 Now with REAL complexity + duplication analysis!")
    app.run(debug=True, port=5000)
