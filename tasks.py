from invoke import task
from subprocess import call
from sys import platform

@task
def build(ctx):
    if platform == "win32":
        ctx.run("python3 src/build.py")
    else:
        ctx.run("python3 src/build.py", pty=True)


@task(build)
def build_start(ctx):
    if platform == "win32":
        ctx.run("python3 src/index.py")
    else:
        ctx.run("python3 src/index.py", pty=True)

@task
def start(ctx):
    if platform == "win32":
        ctx.run("python3 src/index.py")
    else:
        ctx.run("python3 src/index.py", pty=True)

@task
def test(ctx):
    if platform == "win32":
        ctx.run("pytest src")
    else:
        ctx.run("pytest src", pty=True)

@task
def coverage(ctx):
    if platform == "win32":
        ctx.run("coverage run --branch -m pytest src")
    else:
        ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    if platform == "win32":
        ctx.run("coverage html")
        ctx.run("start htmlcov/index.html")
    else:
        ctx.run("coverage html", pty=True)
        call(("xdg-open", "htmlcov/index.html"))

@task
def format(ctx):
    if platform == "win32":
        ctx.run("autopep8 --in-place --recursive src")
    else:
        ctx.run("autopep8 --in-place --recursive src", pty=True)

@task
def lint(ctx):
    if platform == "win32":
        ctx.run("pylint src")
    else:
        ctx.run("pylint src", pty=True)
