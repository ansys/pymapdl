import os


def test_is_running(mapdl):
    mapdl.prep7()
    assert isinstance(mapdl.prep7(), str)


def test_kill_server(mapdl):
    stream = os.popen("docker kill mapdl")
    mapdl.prep7()
