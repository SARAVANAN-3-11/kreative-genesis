document.addEventListener('DOMContentLoaded', function() {
    // Load demo first
    updateDemoData();
    
    document.getElementById('analyzeBtn').onclick = function() {
        const code = document.getElementById('codeEditor').value;
        console.log('Analyzing code...'); // Check console
        
        // ANALYZE YOUR CODE
        const lines = code.split('\n');
        const issues = [];
        
        lines.forEach((line, i) => {
            if (line.includes('BadCode') || line.includes('StudentName')) {
                issues.push({line:i+1, message:'Use snake_case naming', severity:'warning'});
            }
            if (line.includes('print(x') && !line.includes('print(x)')) {
                issues.push({line:i+1, message:'Syntax error - missing )', severity:'error'});
            }
            if (line.trim().startsWith('x=')) {
                issues.push({line:i+1, message:'Uninitialized variable x', severity:'error'});
            }
        });
        
        // UPDATE DASHBOARD WITH NEW RESULTS
        const score = Math.max(0, 85 - issues.length * 5);
        document.getElementById('scoreValue').textContent = score;
        document.getElementById('bugs-count').textContent = issues.filter(i=>i.severity=='error').length;
        document.getElementById('style-count').textContent = issues.filter(i=>i.severity=='warning').length;
        
        console.log('✅ NEW RESULTS:', score, issues);
    };
});

function updateDemoData() {
    document.getElementById('scoreValue').textContent = '85';
    document.getElementById('bugs-count').textContent = '2';
    document.getElementById('style-count').textContent = '8';
}
