#! /usr/bin/env python
# -*- encoding: utf-8 -*-
from config import conf
from os import path, makedirs
import git
from git import Repo
from bzrlib.plugin import load_plugins
load_plugins()
from bzrlib.branch import Branch

remote_branch_url = 'lp:launchpad'



def _update_version(version):
    # Create version folder if not exist
    if not path.isdir(version):
        makedirs(version)
    lst_repo = conf.get(version, 'list_repository').split(',')

    for item in lst_repo:
        repo_dir = './%s/%s' % (version, item)
        if not path.isdir(repo_dir):
            if conf.get(version, item):
                print "Getting %s" % (conf.get(version, item))
                if conf.get(version, item)[0:4] == 'git:':
                    my_repo = conf.get(version, item).split(' -b ')
                    Repo.clone_from(
                        my_repo[0],
                        repo_dir,
                        branch=my_repo[1],
                        depth=1)
                elif conf.get(version, item)[0:3] == 'lp:':
                    remote_branch = Branch.open(conf.get(version, item))
                    local_branch = remote_branch.bzrdir.sprout(repo_dir).open_branch()
                else:
                    raise 'Unavailable to get %s. Non Implemented' % (conf.get(version, item))
            else:
                pass

        else:
            pass
            # TODO Update repository


def update_both_version():
    version_from = conf.get('general', 'version_from')
    version_to = conf.get('general', 'version_to')
    _update_version(version_from)
    _update_version(version_to)


update_both_version()
