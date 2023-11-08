$PROJECT = 'diffpy.utils'
$ACTIVITIES = [
              'version_bump', # Update version number
              'changelog', # Create a CHANGELOG.rst using news directory
              'tag'  # Creates a tag for the new version number
               ]
$VERSION_BUMP_PATTERNS = [('setup.py', r'FALLBACK_VERSION\s*=.*,', "FALLBACK_VERSION = '$VERSION'")]
$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
$PUSH_TAG_REMOTE = 'git@github.com:diffpy/diffpy.utils.git'  # Repo to push tags to
$GITHUB_ORG = 'diffpy'  # Github org for Github releases and conda-forge
$GITHUB_REPO = 'diffpy.utils'  # Github repo for Github releases  and conda-forge
$GHRELEASE_PREPEND = """See [CHANGELOG.](CHANGELOG.md) for detailed release notes.

The release is also available at [PyPI](https://pypi.org/project/diffpy.utils/) and [Conda](https://anaconda.org/conda-forge/diffpy.utils).
"""  # release message
