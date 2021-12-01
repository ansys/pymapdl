import os


def test_inquire(mapdl):

    # Testing basic functions (First block: Functions)
    assert 'apdl' in mapdl.inquire('apdl').lower()

    # test returning the value of an environment variable to a parameter
    env = list(os.environ.keys())[0]
    if os.name == 'nt':
        env_value = os.getenv(env).split(';')[0]
    elif os.name == 'posix':
        env_value = os.getenv(env).split(':')[0]
    else:
        raise Exception('Not supported OS.')

    env_ = mapdl.inquire('ENV', env, 0)
    assert env_ == env_value

    # returning the value of a title to a parameter
    title = 'This is the title'
    mapdl.title(title)
    assert title == mapdl.inquire('title')

    # return information about a file to a parameter
    jobname = mapdl.inquire('jobname')
    assert mapdl.inquire('exist', jobname + '.lock')
    assert mapdl.inquire('exist', jobname , 'lock')
