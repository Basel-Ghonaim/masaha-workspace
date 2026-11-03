# Stage given content (from a file) as the index version of a path: python stagetext.py <path> <contentfile>
import subprocess, sys
ROOT = 'C:/dev/masaha/app-lane-w4'
path, src = sys.argv[1], sys.argv[2]
data = open(src, 'rb').read()
sha = subprocess.run(['git', 'hash-object', '-w', '--stdin'], cwd=ROOT, input=data, capture_output=True).stdout.decode().strip()
r = subprocess.run(['git', 'update-index', '--cacheinfo', f'100644,{sha},{path}'], cwd=ROOT, capture_output=True, text=True)
print('staged', path, r.returncode, r.stderr)
