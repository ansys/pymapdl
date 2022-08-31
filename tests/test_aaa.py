import os


def test_a_test_server(mapdl):
    assert mapdl.prep7()


def test_kill_server(mapdl):
    mapdl._run("/eof")
    stream = os.popen("docker stop mapdl")
    mapdl.prep7()
