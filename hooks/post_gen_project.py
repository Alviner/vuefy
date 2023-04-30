import subprocess

subprocess.check_call(['git', 'init'])
subprocess.check_call(['git', 'add', 'README.md'])
subprocess.check_call(['git', 'commit', '-m', 'Initial'])
subprocess.check_call(['git', 'tag', '--annotate', '-m', 'v0.0', 'v0.0'])
subprocess.check_call(['poetry', 'env', 'use', '3.11'])
subprocess.check_call(['make', 'develop'])
subprocess.check_call(['make', 'build-vendor'])
subprocess.check_call(['make', 'format'])

