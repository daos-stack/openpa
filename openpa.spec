%define libname libopa1

Name:		openpa
Version:	1.0.4
Release:	6%{?dist}

Summary:	OpenPA

Group:		Development/Libraries/C and C++
License:	UChicago Argonne -- OpenPA License
URL:		https://github.com/pmodels/openpa
Source0:	https://github.com/pmodels/%{name}/archive/v%{version}.tar.gz

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool
BuildRequires: pkgconfig


%description
OpenPA
%package -n %{libname}
Summary:	OpenPA library
Obsoletes:	%{name} < 1.0.4-4
Provides:	%{name} = %{version}

%description -n %{libname}
OpenPA library.

%package devel
Summary:	OpenPA devel
Group:		Development/Libraries/C and C++
Requires:	%{libname}%{?_isa} = %{version}-%{release}

%description devel
OpenPA devel

%prep 
%setup -q

%build
if [ ! -f configure ]; then
    ./autogen.sh
fi
%configure --enable-shared
make %{?_smp_mflags}

%install
%make_install

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root,-)
%license COPYRIGHT
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/

%changelog
* Mon Jun 22 2020 Brian J. Murrell <brian.murrell@intel> - 1.0.4-6
- Fix License:
- Add %license

* Sat Aug 17 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.4-5
- Split out versioned library into a subpackage
  - add a Provides: to the new libopa1 package
- Obsoletes: previous openpa packages since it contained the
  library

* Wed May 01 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.4-3
- Change source to use the more consistent "archive" URL

* Mon Mar 11 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.4-2
- Update to reflect move to GitHub

* Mon Aug 13 2018 Brian J. Murrell <brian.murrell@intel> - 1.0.4-1
- Initial package
