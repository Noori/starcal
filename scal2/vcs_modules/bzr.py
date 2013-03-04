# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Saeed Rasooli <saeed.gnu@gmail.com> (ilius)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/gpl.txt>.
# Also avalable in /usr/share/common-licenses/GPL on Debian systems
# or /usr/share/licenses/common/GPL3/license.txt on ArchLinux

from scal2.time_utils import getEpochFromJd
from scal2.vcs_modules.common import encodeShortStat

from bzrlib.bzrdir import BzrDir

def prepareObj(obj):
    tree, branch, repository, relpath = \
        BzrDir.open_containing_tree_branch_or_repository(obj.vcsDir)
    obj.branch = branch
    obj.repo = repository


def clearObj(obj):
    obj.branch = None
    obj.repo = None

def getCommitList(obj, startJd, endJd):
    '''
        returns a list of (epoch, rev_id) tuples
    '''
    branch = obj.branch
    if not branch:
        return []
    startEpoch = getEpochFromJd(startJd)
    endEpoch = getEpochFromJd(endJd)
    ###
    data = []
    ## obj.repo.revisions
    for rev_id, depth, revno, end_of_merge in \
    branch.iter_merge_sorted_revisions(direction='forward'):
        rev = obj.repo.get_revision(rev_id)
        epoch = rev.timestamp
        if epoch < startEpoch:
            continue
        if epoch >= endEpoch:
            break
        data.append((epoch, rev_id))
    return data


def getCommitInfo(obj, rev_id):
    rev = obj.repo.get_revision(rev_id)
    lines = rev.message.split('\n')
    return {
        'epoch': rev.timestamp,
        'author': rev.committer,
        'shortHash': rev_id,
        'summary': lines[0],
        'description': '\n'.join(lines[1:]),
    }


#def getShortStat(repo, node1, node2):
#    return files_changed, insertions, deletions


def getCommitShortStat(obj, rev_id):
    '''
        returns (files_changed, insertions, deletions)
    '''
    ## file level only (not code lines)
    delta = obj.repo.get_revision_delta(rev_id)
    #for item in delta.modified:
    #    print 'delta modified:', item
    #print
    return 0, 0, 0

def getCommitShortStatLine(obj, rev_id):
    '''
        returns str
    '''
    #return encodeShortStat(*getCommitShortStat(obj, rev_id))
    return ''


def getTagList(obj, startJd, endJd):
    '''
        returns a list of (epoch, tag_name) tuples
    '''
    if not obj.repo:
        return []
    startEpoch = getEpochFromJd(startJd)
    endEpoch = getEpochFromJd(endJd)
    ###
    data = []
    for tag, rev_id in obj.branch.tags.get_tag_dict().iteritems():
        rev = obj.repo.get_revision(rev_id)
        epoch = rev.timestamp
        if epoch < startEpoch:
            continue
        if epoch >= endEpoch:
            continue
        data.append((
            epoch,
            tag,
        ))
    return data

def getTagShortStat(obj, prevTag, tag):
    return 0, 0, 0


def getTagShortStatLine(obj, prevTag, tag):
    '''
        returns str
    '''
    return encodeShortStat(*getTagShortStat(obj, prevTag, tag))




