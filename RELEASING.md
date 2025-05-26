# Releasing Raygun4Py

Raygun for Python is published on PyPi as [`raygun4py`](https://pypi.org/project/raygun4py/).

## Semantic versioning

This package follows semantic versioning,

Given a version number MAJOR.MINOR.PATCH (x.y.z), increment the:

- MAJOR version when you make incompatible changes
- MINOR version when you add functionality in a backward compatible manner
- PATCH version when you make backward compatible bug fixes

To learn more about semantic versioning check: https://semver.org/

## Preparing for release

### Release branch

Create a new branch named `release/x.y.z` 
where `x.y.z` is the Major, Minor and Patch release numbers.

### Update version

Update the `version` in the `python3/raygun4py/version.py` file.

### Update CHANGELOG.md

Add a new entry in the `CHANGELOG.md` file.

Obtain a list of changes using the following git command:

```
git log --pretty=format:"- %s (%as)"
```

### Commit and open a PR

Commit all the changes into a commit with the message `chore: Release x.y.z` where `x.y.z` is the Major, Minor and Patch release numbers.

Then push the branch and open a new PR, ask the team to review it.

## Publishing

### PR approval

Once the PR has been approved, you can publish the provider.

### Publish to PyPi 

1. Activate the local environment created in the `CONTRIBUTING.md` guideline.
2. Install release tools: `python3 -m pip install setuptools twine`.
3. Run `python setup.py sdist`.
4. Check that the file `dist/raygun4py-x.y.z.tar.gz` has been created.
5. Run `twine check dist/raygun4py-x.y.z.tar.gz` and fix any warnings. Repeat the `sdist` command if necessary.
5. Run `twine upload dist/raygun4py-x.x.x.tar.gz` to upload the package.
6. Provide the API token when asked.
7. Now the package is available for customers.

### Merge PR to master

With the PR approved and the package published, squash and merge the PR into `master`.

### Tag and create Github Release

Go to https://github.com/MindscapeHQ/raygun4py/releases and create a new Release.

GitHub will create a tag for you, you don't need to create the tag manually.

You can also generate the release notes automatically.
