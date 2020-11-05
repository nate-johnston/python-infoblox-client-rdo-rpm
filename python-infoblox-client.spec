%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global client python-infoblox-client
%global sclient infoblox-client
# If a executable is provided by the package uncomment following line
#%global executable infoblox

Name:       %{client}
Version:    XXX
Release:    XXX
Summary:    Infoblox Client
License:    ASL 2.0
URL:        https://github.com/infobloxopen/infoblox-client

Source0:    http://tarballs.openstack.org/%{client}/%{client}-master.tar.gz

BuildArch:  noarch

%package -n python2-%{sclient}
Summary:    Infoblox client
%{?python_provide:%python_provide python2-%{sclient}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
# Test requirements should be added here as BuildRequires for tests in %check

Requires:   python-oslo-config >= 2:3.4.0

%description -n python2-%{sclient}
Infoblox client


%package -n python2-%{sclient}-tests
Summary:    Infoblox client tests
Requires:   python2-%{sclient} = %{version}-%{release}

# Test requirements should be added here as Requires.

%description -n python2-%{sclient}-tests
Infoblox client tests

This package contains the infoblox client test files.


%package -n python-%{sclient}-doc
Summary:    Infoblox client documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{sclient}-doc
Infoblox client documentation

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{sclient}
Summary:    Infoblox client
%{?python_provide:%python_provide python3-%{sclient}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git
# Test requirements should be added here as BuildRequires if adding tests in %check

Requires:   python3-oslo-config >= 2:3.4.0

%description -n python3-%{sclient}
Infoblox client


%package -n python3-%{sclient}-tests
Summary:    Infoblox client tests
Requires:   python3-%{sclient} = %{version}-%{release}

# Test requirements should be added here as Requires.

%description -n python3-%{sclient}-tests
Infoblox client tests

This package contains the example client test files.

%endif # with_python3


%description
Infoblox library.


%prep
%autosetup -n %{client}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

# If the client has man page uncomment following line
# %{__python2} setup.py build_sphinx --builder man

%install
%if 0%{?with_python3}
# If an executable is provided by the package uncomment following lines
#mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python3_version}
#ln -s ./%{executable}-%{python3_version} %{buildroot}%{_bindir}/%{executable}-3
%py3_install
# If an executable is provided by the package uncomment following lines
#mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python2_version}
#ln -s %{_bindir}/%{executable}-%{python2_version} %{buildroot}%{_bindir}/%{executable}-2
#ln -s %{_bindir}/%{executable}-2 %{buildroot}%{_bindir}/%{executable}
%endif

%py2_install
# If the client has man page uncomment following line
# install -p -D -m 644 man/%{executable}.1 %{buildroot}%{_mandir}/man1/%{executable}.1

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{sclient}
%license LICENSE
%{python2_sitelib}/%{sclient}
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/%{sclient}/tests
# If the client has man page uncomment
#%{_mandir}/man1/%{executable}.1
# If an executable is provided by the package uncomment following lines
#%{_bindir}/%{executable}
#%{_bindir}/%{executable}-2
#%{_bindir}/%{executable}-%{python2_version}
#%endif

%files -n python2-%{sclient}-tests
%license LICENSE
%{python2_sitelib}/%{sclient}/tests

%files -n python-%{sclient}-doc
%license LICENSE
%doc html README.rst

%if 0%{?with_python3}
%files python3-%{sclient}
%license LICENSE
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{sclient}/tests
# If the client has man page uncomment
#%{_mandir}/man1/%{executable}.1
# If an executable is provided by the package uncomment following lines
#%{_bindir}/%{executable}-3
#%{_bindir}/%{executable}-%{python3_version}
#%endif


%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{sclient}/tests
%endif # with_python3

%changelog
