#!/usr/bin/python

from github import Github
import sys

REPO = "CentOS-PaaS-SIG/linchpin"
NIGHTLY = False


def get_doc_fixes(pulls):
    doc_fixes = []
    # iterate over pulls backward so that list can be removed in place
    for i in range(len(pulls) - 1, -1, -1):
        labels = pulls[i].get_labels()
        for label in labels:
            if label.name == "documentation":
                doc_fixes.append(pulls[i])
                pulls.pop(i)
                break
    return doc_fixes


def get_bug_fixes(pulls):
    bug_fixes = []
    # iterate over pulls backward so that list can be removed in place
    for i in range(len(pulls) - 1, -1, -1):
        labels = pulls[i].get_labels()
        for label in labels:
            if label.name == "bug":
                bug_fixes.append(pulls[i])
                pulls.pop(i)
                break
    return bug_fixes


def get_enhancements(pulls):
    enhancements = []
    # iterate over pulls backward so that list can be removed in place
    for i in range(len(pulls) - 1, -1, -1):
        labels = pulls[i].get_labels()
        for label in labels:
            if label.name == "rfe":
                enhancements.append(pulls[i])
                pulls.pop(i)
                break
    return enhancements


def get_test_enhancements(pulls):
    test_enhancements = []
    # iterate over pulls backward so that list can be removed in place
    for i in range(len(pulls) - 1, -1, -1):
        labels = pulls[i].get_labels()
        for label in labels:
            if label.name == "ci" or "testing":
                test_enhancements.append(pulls[i])
                pulls.pop(i)
                break
    return test_enhancements


# get all issues in the milestone that are not the release PR
def get_remaining_changes(pulls):
    changes = []
    # iterate over pulls backward so that list can be removed in place
    for i in range(len(pulls) - 1, -1, -1):
        labels = pulls[i].get_labels()
        for label in labels:
            if label.name == "release":
                continue
            else:
                changes.append(pulls[i])
                pulls.pop(i)
                break
    return changes


def get_pulls(milestone):
    pulls = []
    issues = repo.get_issues(milestone=milestone, state='closed')
    for i in issues:
        if i.pull_request is not None:
            pulls.append(i.as_pull_request())
    return pulls


def get_milestone_tasks(repo, milestone_title):
    milestones = repo.get_milestones(sort="due_on", direction="desc")
    for m in milestones:
        if m.title == milestone_title:
            return get_pulls(m)
    return []


def get_repo(token, name):
    g = Github(token)
    return g.get_repo(name)


def format_body(tasks):
    body = {}
    body_str = "This release contains the following updates:\n\n"
    body['Documentation'] = get_doc_fixes(tasks)
    body['Bug Fixes'] = get_bug_fixes(tasks)
    body['Enhancements'] = get_enhancements(tasks)
    body['CI, Test Enhancements'] = get_test_enhancements(tasks)
    body['Other Changes'] = get_remaining_changes(tasks)

    for title, items in body.items():
        if not items:
            continue

        body_str += title + "\n"
        for item in items:
            body_str += "* {0} #{1} by {2}\n".format(item.title, item.number,
                                                     item.user.login)
        body_str += "\n"
    return body_str


# code starts here

# get API token
token = sys.argv[1]
milestone = sys.argv[2]
if len(sys.argv) == 4 and sys.argv[3] == "nightly":
    NIGHTLY = True

repo = get_repo(token, REPO)

tasks = get_milestone_tasks(repo, milestone)
release_body = format_body(tasks)
release_name = milestone

if not NIGHTLY:
    repo.create_git_release(milestone, release_name, release_body,
                            target_commitish="master")
