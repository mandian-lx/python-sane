%global name3 python3-sane
%global py3dir ../py3

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

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx

Obsoletes:      python-pillow-sane < 2.7.0-1
Provides:       python-pillow-sane = %{version}-%{release}

Requires:       python-imaging

%description
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.

%files
%doc CHANGES.rst sanedoc.txt example.py doc/_build/html COPYING
%{python2_sitearch}/*

#----------------------------------------------------------------------------

%package -n %{name3}
Summary:        Python module for using scanners
Provides:       python2-pillow-sane = %{version}-%{release}
Requires:       python2-numpy

%description -n %{name3}
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.

%files -n %{name3}
%doc CHANGES.rst sanedoc.txt example.py doc/_build/html COPYING
%{python3_sitearch}/*

#----------------------------------------------------------------------------

%prep
%setup -q -n python-pillow-Sane-%{shortcommit}

# Create Python 3 source tree
rm -rf %{py3dir}
mkdir %{py3dir}
cp -a . %{py3dir}

%build
# Build Python 2 modules
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python2}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build

pushd doc
make html
rm -f _build/html/.buildinfo
popd

# Build Python 3 modules
pushd %{py3dir}
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python3}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd

pushd doc SPHINXBUILD=sphinx-build-%py3_ver
make html
rm -f _build/html/.buildinfo
popd

%install
# Install Python 2 modules
%{__python} setup.py install --skip-build --root %{buildroot}

# Fix non-standard-executable-perm
chmod 0755 %{buildroot}%{python_sitearch}/*.so

# Install Python 3 modules
pushd %{py2dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd

# Fix non-standard-executable-perm
chmod 0755 %{buildroot}%{python3_sitearch}/*.so

%if 0%{?with_docs}
pushd doc
make html SPHINXBUILD=sphinx-build-%python3_version
rm -f _build/html/.buildinfo
popd
%endif

