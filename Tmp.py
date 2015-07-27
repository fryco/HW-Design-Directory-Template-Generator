import os
from os.path import join as path_join
import errno

def make_node(node):
    try:
        os.makedirs(node)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise


def create_tree(home, branches, leaves):
    for branch in branches:
        parent = path_join(home, branch)
        make_node(parent)
        children = leaves.get(branch, [])
        for child in children:
            child = os.path.join(parent, child)
            make_node(child)

if __name__ == "__main__":
    PROJECT_HOME = os.getcwd()

    home = os.path.join(PROJECT_HOME, 'test_directory_tree')
    create_tree(home, branches=[], leaves={})

    branches = (
        'docs',
        'scripts',
    )
    leaves = (
        ('rst', 'html', ),
        ('python', 'bash', )
    )
    leaves = dict(list(zip(branches, leaves)))
    create_tree(home, branches, leaves)

    python_home = os.path.join(home, 'scripts', 'python')
    branches = (
        'os',
        'sys',
        'text_processing',
    )
    leaves = {}
    leaves = dict(list(zip(branches, leaves)))
    create_tree(python_home, branches, leaves)

    after_thought_home = os.path.join(home, 'docs', 'after_thought')
    branches = (
        'child_0',
        'child_1',
    )
    leaves = (
        ('sub_0', 'sub_1'),
        (),
    )
    leaves = dict(list(zip(branches, leaves)))
    create_tree(after_thought_home, branches, leaves)
