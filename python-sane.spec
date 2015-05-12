%global name3 python3-sane

# RHEL-7 doesn't have python 3
%if 0%{?rhel} == 7
  %global with_python3 0
%else
  %global with_python3 1
%endif

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
Release:        1%{?snap}%{?dist}
Summary:        Python SANE interface

License:        MIT
URL:            https://github.com/python-pillow/Sane

# Obtain the tarball for a certain commit via:
#  wget --content-disposition https://github.com/python-pillow/Sane/tarball/$commit
Source0:        https://github.com/python-pillow/Sane/tarball/%{commit}/python-pillow-Sane-v%{version}-%{ahead}-g%{shortcommit}.tar.gz

BuildRequires:  sane-backends-devel

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

%if %{with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
%endif

Obsoletes:      python-pillow-sane < 2.7.0-1
Provides:       python-pillow-sane = %{version}-%{release}

Requires:       python-pillow

%filter_provides_in %{python_sitearch}
%filter_provides_in %{python3_sitearch}
%filter_setup

%description
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.


%if %{with_python3}
%package -n %{name3}
Summary:        Python module for using scanners
Obsoletes:      python3-pillow-sane <= 2.6.1-2
Provides:       python3-pillow-sane = %{version}-%{release}
Requires:       python3-pillow
Requires:       python3-numpy

%description -n %{name3}
This package contains the sane module for Python which provides access to
various raster scanning devices such as flatbed scanners and digital cameras.
%endif


%prep
%setup -q -n python-pillow-Sane-%{shortcommit}

%if %{with_python3}
# Create Python 3 source tree
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
# Build Python 2 modules
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

pushd doc
make html
rm -f _build/html/.buildinfo
popd

%if %{with_python3}
# Build Python 3 modules
pushd %{py3dir}
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python3}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

pushd doc
make html SPHINXBUILD=sphinx-build-%python3_version
rm -f _build/html/.buildinfo
popd
%endif


%install
# Install Python 2 modules
%{__python} setup.py install --skip-build --root %{buildroot}

# Fix non-standard-executable-perm
chmod 0755 %{buildroot}%{python_sitearch}/*.so

%if %{with_python3}
# Install Python 3 modules
pushd %{py3dir}
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
%endif


%files
%doc CHANGES.rst sanedoc.txt example.py doc/_build/html
%license COPYING
%{python2_sitearch}/*

%if %{with_python3}
%files -n %{name3}
%doc CHANGES.rst sanedoc.txt example.py doc/_build/html
%license COPYING
%{python3_sitearch}/*
%endif

%changelog
* Fri Mar 27 2015 Sandro Mani <manisandro@gmail.com> - 2.8.1-1
- Update to 2.8.1

* Sat Mar 07 2015 Sandro Mani <manisandro@gmail.com> - 2.8.0-1
- Update to 2.8.0

* Fri Jan 02 2015 Sandro Mani <manisandro@gmail.com> - 2.7.0-1
- Initial package
