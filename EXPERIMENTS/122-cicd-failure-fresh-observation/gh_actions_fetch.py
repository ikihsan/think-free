"""GitHub Actions fetch, split out of the CI/CD experiment's runner.

Moved verbatim so `run_experiment.py` fits the 300-line cap in
`docs/policy/doc-standards.md`. It is the only function that touches the
network in E122, which is why it is separable.
"""

import json
import os
import subprocess
import time

def fetch_github_actions_failures(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Fetch failed workflow runs from GitHub Actions API.
    
    Uses GitHub REST API to search for failed workflow runs.
    Requires GITHUB_TOKEN environment variable for authenticated requests.
    """
    print("=" * 60)
    print("Fetching real failed GitHub Actions runs...")
    print("=" * 60)
    
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("WARNING: GITHUB_TOKEN not set. Using unauthenticated requests (rate limited).")
        auth_header = []
    else:
        auth_header = ['-H', f'Authorization: token {token}']
    
    # Search for failed workflow runs across popular repositories
    # We'll sample from a few well-known repos across different languages
    repos = [
        "python/cpython",
        "nodejs/node",
        "rust-lang/rust",
        "golang/go",
        "tensorflow/tensorflow",
        "pytorch/pytorch",
        "kubernetes/kubernetes",
        "microsoft/vscode",
        "facebook/react",
        "django/django",
    ]
    
    all_runs = []
    
    for repo in repos:
        if len(all_runs) >= limit:
            break
            
        print(f"  Fetching from {repo}...")
        
        # Get workflow runs for this repo
        url = f"https://api.github.com/repos/{repo}/actions/runs?status=failure&per_page=20"
        
        try:
            cmd = ['curl', '-s', '-H', 'Accept: application/vnd.github.v3+json'] + auth_header + [url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"    Error: {result.stderr}")
                continue
            
            data = json.loads(result.stdout)
            runs = data.get('workflow_runs', [])
            
            for run in runs:
                if len(all_runs) >= limit:
                    break
                    
                # Get the failed job logs
                run_id = run['id']
                logs_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/logs"
                
                log_cmd = ['curl', '-s', '-H', 'Accept: application/vnd.github.v3+json'] + auth_header + [logs_url]
                log_result = subprocess.run(log_cmd, capture_output=True, text=True, timeout=60)
                
                if log_result.returncode == 0:
                    # Logs are returned as a zip file, but GitHub API returns raw text for small logs
                    # For simplicity, we'll use the conclusion and try to get job details
                    jobs_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs"
                    jobs_cmd = ['curl', '-s', '-H', 'Accept: application/vnd.github.v3+json'] + auth_header + [jobs_url]
                    jobs_result = subprocess.run(jobs_cmd, capture_output=True, text=True, timeout=30)
                    
                    if jobs_result.returncode == 0:
                        jobs_data = json.loads(jobs_result.stdout)
                        jobs = jobs_data.get('jobs', [])
                        
                        for job in jobs:
                            if job['conclusion'] == 'failure':
                                # Build log text from job steps
                                log_text = f"Repository: {repo}\n"
                                log_text += f"Workflow: {run['name']}\n"
                                log_text += f"Job: {job['name']}\n"
                                log_text += f"Conclusion: {job['conclusion']}\n"
                                
                                steps = job.get('steps', [])
                                for step in steps:
                                    if step['conclusion'] == 'failure':
                                        log_text += f"\nFailed step: {step['name']}\n"
                                        # Note: Full logs require downloading zip, which is complex
                                        # We'll use what we have from the API
                                
                                all_runs.append({
                                    'repo': repo,
                                    'run_id': run_id,
                                    'workflow_name': run['name'],
                                    'job_name': job['name'],
                                    'log_text': log_text,
                                    'html_url': run['html_url'],
                                })
                
                time.sleep(0.5)  # Rate limiting
                
        except Exception as e:
            print(f"    Error fetching {repo}: {e}")
            continue
    
    print(f"Fetched {len(all_runs)} failed runs with logs")
    return all_runs
