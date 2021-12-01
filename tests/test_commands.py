import os


def test_inquire(mapdl):

    # Testing basic functions (First block: Functions)
    assert 'apdl' in mapdl.inquire('apdl').lower()

    # **Returning the Value of an Environment Variable to a Parameter**
    env = list(os.environ.keys())[0]
    if os.name == 'nt':
        env_value = os.getenv(env).split(';')[0]
    elif os.name == 'posix':
        env_value = os.getenv(env).split(':')[0]
    else:
        raise Exception('Not supported OS.')

    env_ = mapdl.inquire('ENV', env, 0)
    assert env_ == env_value

    # **Returning the Value of a Title to a Parameter**
    title = 'This is the title'
    mapdl.title(title)
    assert title == mapdl.inquire('title')

    # **Returning Information About a File to a Parameter**
    jobname = mapdl.inquire('jobname')
    assert mapdl.inquire('exist', jobname + '.lock')
    assert mapdl.inquire('exist', jobname , 'lock')
    
