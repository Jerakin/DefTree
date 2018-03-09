#!/usr/bin/env bash
BUMP_VERSION=$1

# ------------------------------------------------------------------------------------------------------------
# CHECK THAT GIT IS CLEAN

if ! git diff-index --quiet HEAD --;
then
    echo "GIT IS DIRTY"
    exit 1
fi

branch=$(git rev-parse --abbrev-ref HEAD)

if ! [ $branch == "master" ];
then
    echo "Releases are only allowed on master"
    exit 1
fi


# ------------------------------------------------------------------------------------------------------------
# UPDATE THE VERSION NUMBER

# Grep the version number
STRING_VERSION=$(grep --regexp='__version__\s=\s".*"' ../deftree.py)

#remove __version__
VERSION=${STRING_VERSION/"__version__ = "/}

# Remove quotation marks before and after
VERSION=${VERSION##\"}
VERSION=${VERSION%%\"}

echo "OLD VERSION: ${VERSION}"

# Split the version on dot
a=( ${VERSION//./ } )

# Update the version number
if [ "$BUMP_VERSION" == "mayor" ]
then
    ((a[0]++))
    a[1]=0
    a[2]=0

elif [ "$BUMP_VERSION" == "minor" ]
then
    ((a[1]++))
    a[2]=0

elif [ "$BUMP_VERSION" == "patch" ]
then
    ((a[2]++))

else
    echo "NO VERSION SPECIFIED"
    exit 1
fi

NEW_VERSION="${a[0]}.${a[1]}.${a[2]}"


echo "Updating from ${VERSION} to ${NEW_VERSION}"

# Update the __version__
sed -i '' "s/$STRING_VERSION/__version__ = \"${NEW_VERSION}\"/" ../CHANGELOG.rst

# ------------------------------------------------------------------------------------------------------------
# UPDATE THE CHANGELOG

UNRELEASED_TAG=$(grep -e UNRELEASED ../deftree.py)

if [ UNRELEASED_TAG ]
then
    CHANGLOG_TITLE="\`${NEW_VERSION} <https://github.com/Jerakin/DefTree/compare/release/${VERSION}...release/${NEW_VERSION}>\`_"
    sed -i '' "s#UNRELEASED#$CHANGLOG_TITLE#" ../CHANGELOG.rst
fi

# ------------------------------------------------------------------------------------------------------------
# COMMIT CHANGES AND ADD TAG

git add ../CHANGELOG.rst
git add ../deftree.py

git commit -m "release ${NEW_VERSION}"

git push origin master

git tag "release/${NEW_VERSION}"

git push origin "release/${NEW_VERSION}"


# ------------------------------------------------------------------------------------------------------------
# PyPi

python ../setup.py bdist_wheel
twine upload "../dist/deftree-${NEW_VERSION}-py3-none-any.whl"


# ------------------------------------------------------------------------------------------------------------
# Trigger Document build
# TOKEN=$(cat token.txt)
# curl -X POST -d "branches=master" -d "token=${TOKEN}" http://www.readthedocs.org/api/v2/webhook/deftree/29031/