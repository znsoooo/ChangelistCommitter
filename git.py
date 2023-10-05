import subprocess

popen = lambda cmd: subprocess.Popen(cmd, stdout=-1, encoding='u8').stdout.read()


def commit():
    pass


def diff():
    pass


def changelist():
    popen('git config --local core.quotepath false')
    return popen('git diff --name-only')


def otherfiles():
    popen('git config --local core.quotepath false')
    return popen('git ls-files --others')


def toplevel():
    return popen('git rev-parse --show-toplevel')


if __name__ == '__main__':
    print(popen('git --version'))
    print(toplevel())
