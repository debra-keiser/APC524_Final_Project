import nox

nox.options.sessions = ["tests"]


@nox.session
def tests(session):
    """
    Run all defined tests.
    """
    session.install(".[test]", "tabulate")
    session.run("pytest", *session.posargs)
