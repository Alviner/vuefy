import subprocess


def test_lint(project):
    subprocess.check_output(
        ["make", 'lint'], cwd=project
    )


def test_tests(project):
    subprocess.check_output(
        ["make", 'pytest'], cwd=project
    )
