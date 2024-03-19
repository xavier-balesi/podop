#!/usr/bin/env bash
set -euo pipefail

# Sonar is doing diff coverage on master and develop. For topic it's not working correctly as there is no previous
# versions when pushing for the first time a topic branch. It's possible to use "Reference Branch" option project by
# project but it's not available by default for all projects (https://docs.sonarqube.org/latest/project-administration/new-code-period/).
# To not wait CI result (especially when we need the develop branch result), let's check it locally.

remote_branch=$(git rev-parse --verify origin/develop &>/dev/null && echo origin/develop || echo origin/main)

# NB: `git merge-base HEAD origin/develop` should give:
# - origin/develop from topic branches (features or bug fixes)
# - master from master branch as origin/develop should have all commits of the master branch => no diff
# - develop from master develop => no diff
# - base between masters/X.Y.Z and origin/master for stabilization branches (warning: their names are not standardized at Linxo)
base=$(git merge-base HEAD "${remote_branch}")

# Currently Sonar doesn't fail if there is less than 20 new lines.
# NB: taking into account python comments by simplicity but we could check Sonar behavior
added=$(git diff --numstat "${base}" -- 'src/*.py' | awk '{ added += $1 } END { print added }')
if (( added < 20 )); then
  echo "${added:-0} added lines, not checking the diff coverage."
  exit 0
fi

diff-cover --fail-under 80 --compare-branch "${base}" .coverage_reports/coverage-report.xml
