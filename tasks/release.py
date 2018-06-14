# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from __future__ import print_function, unicode_literals
import sys

from packaging import version
from invoke import task
from invoke.exceptions import Exit
from colorama import Fore

from .constants import AGENT_BASED_INTEGRATIONS
from .utils.git import (
    get_current_branch, parse_pr_numbers, get_diff, git_tag
)
from .utils.common import (
    get_version_string, get_release_tag_string, update_version_module
)
from .utils.github import get_changelog_types, get_pr
from .changelog import do_update_changelog


@task(help={
    'target': "The check to tag",
    'version': "The desired version, defaults to the one from setup.py",
    'dry-run': "Runs the task without actually doing anything",
})
def release_tag(ctx, target, version=None, dry_run=False, push=True):
    """
    Tag the HEAD of the git repo with the current release number for a
    specific check. The tag is pushed to origin by default.

    Notice: specifying a different version than the one in setup.py is
    a maintainance task that should be run under very specific circumstances
    (e.g. re-align an old release performed on the wrong commit).
    """
    # get the current version
    if version is None:
        version = get_version_string(target)

    # get the tag name
    tag = get_release_tag_string(target, version)
    print("Tagging HEAD with {}".format(tag))
    if dry_run:
        return

    try:
        git_tag(ctx, tag, push)
    except Exception as e:
        print(e)


@task
def print_shippable(ctx, quiet=False):
    """
    Print all the checks that can be released.
    """
    for target in AGENT_BASED_INTEGRATIONS:
        # get the name of the current release tag
        cur_version = get_version_string(target)
        target_tag = get_release_tag_string(target, cur_version)

        # get the diff from HEAD
        diff_lines = get_diff(ctx, target, target_tag)

        # get the number of PRs that could be potentially released
        pr_numbers = parse_pr_numbers(diff_lines)
        if pr_numbers:
            if quiet:
                print(target)
            else:
                print("Check {} has {} merged PRs that could be released".format(target, len(pr_numbers)))


@task(help={
    'target': "List the pending changes for the target check.",
})
def release_show_pending(ctx, target):
    """
    Print all the pending PRs for a given check.

    Example invocation:
        inv release-show-pending mysql
    """
    # sanity check on the target
    if target not in AGENT_BASED_INTEGRATIONS:
        raise Exit("Provided target is not an Agent-based Integration")

    # get the name of the current release tag
    cur_version = get_version_string(target)
    target_tag = get_release_tag_string(target, cur_version)

    # get the diff from HEAD
    diff_lines = get_diff(ctx, target, target_tag)

    # for each PR get the title, we'll use it to populate the changelog
    pr_numbers = parse_pr_numbers(diff_lines)
    print("Found {} PRs merged since tag: {}".format(len(pr_numbers), target_tag))
    for pr_num in pr_numbers:
        try:
            payload = get_pr(pr_num)
        except Exception as e:
            sys.stderr.write("Unable to fetch info for PR #{}\n: {}".format(pr_num, e))
            continue

        changelog_types = get_changelog_types(payload)
        if not changelog_types:
            changelog_status = Fore.RED + 'WARNING! No changelog labels attached.'
        elif len(changelog_types) > 1:
            changelog_status = Fore.RED + 'WARNING! Too many changelog labels attached: {}'.format(','.join(changelog_types))
        else:
            changelog_status = Fore.GREEN + changelog_types[0]

        print(payload.get('title'))
        print(" * Url: {}".format(payload.get('html_url')))
        print(" * Changelog status: {}".format(changelog_status))
        print("")


@task(help={
    'target': "The check to release",
    'new_version': "The new version",
})
def release_prepare(ctx, target, new_version):
    """
    Perform a set of operations needed to release a single check:

     * update the version in __about__.py
     * update the changelog
     * update the AGENT_REQ_FILE file
     * commit the above changes

    Example invocation:
        inv release-prepare redisdb 3.1.1
    """
    # sanity check on the target
    if target not in AGENT_BASED_INTEGRATIONS:
        raise Exit("Provided target is not an Agent-based Integration")

    # don't run the task on the master branch
    if get_current_branch(ctx) == 'master':
        raise Exit("This task will add a commit, you don't want to add it on master directly")

    # sanity check on the version provided
    cur_version = get_version_string(target)
    p_version = version.parse(new_version)
    p_current = version.parse(cur_version)
    if p_version <= p_current:
        raise Exit("Current version is {}, can't bump to {}".format(p_current, p_version))

    # update the version number
    print("Current version of check {}: {}, bumping to: {}".format(target, p_current, p_version))
    update_version_module(target, cur_version, new_version)

    # update the CHANGELOG
    print("Updating the changelog")
    do_update_changelog(ctx, target, cur_version, new_version)

    # done
    print("All done, remember to push to origin and open a PR to merge these changes on master")
