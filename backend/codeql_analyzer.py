import subprocess
import tempfile
import shutil
import os

def analyze_with_codeql(code_dir):
    # CodeQL CLI subprocess calls
    db_path = tempfile.mkdtemp()
    subprocess.run(['codeql', 'database', 'create', ...])
    subprocess.run(['codeql', 'database', 'analyze', ...])
    return parse_sarif('results.sarif')
