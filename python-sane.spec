# Refer to the comment for Source0 below on how to obtain the source tarball
# The saved file has format python-pillow-Sane-$version-$ahead-g$shortcommit.tar.gz
%global commit 8c4d40d85a915f0dcc6b3177d4d3d70466188d8c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global ahead 0

# If ahead is 0, the tarball corresponds to a release version, otherwise to a git snapshot
%if %{ahead} > 0
%global snap .git%{shortcommit}
%endif

Name:           python-sane
Version:        2.8.1
Release:        2
Summary:        Python SANE interface

License:        MIT
URL:            https://github.com/python-pillow/Sane

# Obtain the tarball for a certain commit via:
#  wget --content-disposition https://github.com/python-pillow/Sane/tarball/$commit
Source0:        https://github.com/python-pillow/Sane/tarball/%{commit}/python-pillow-Sane-v%{version}-%{ahead}-g%{shortcommit}.tar.gz

BuildRequires:  sane-devel

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

Obsoletes:      python-pillow-sane < 2.7.0-1
Provides:       python-pillow-sane = %{version}-%{release}

Requires:       python-imaging

%description
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.

%files
%doc CHANGES.rst sanedoc.txt example.py doc/_build/html COPYING
%{python_sitearch}/*

#----------------------------------------------------------------------------

%prep
%setup -q -n python-pillow-Sane-%{shortcommit}

%build
# Build Python 2 modules
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

pushd doc
make html
rm -f _build/html/.buildinfo
popd

%install
# Install Python 2 modules
%{__python} setup.py install --skip-build --root %{buildroot}

# Fix non-standard-executable-perm
chmod 0755 %{buildroot}%{python_sitearch}/*.so

%if 0%{?with_docs}
pushd doc
make html SPHINXBUILD=sphinx-build-%python3_version
rm -f _build/html/.buildinfo
popd
%endif

