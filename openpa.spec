Name:		openpa
Version:	1.0.4
Release:	4%{?dist}

Summary:	OpenPA

Group:		Development/Libraries
License:	ANL
URL:		https://github.com/pmodels/openpa
Source0:	https://github.com/pmodels/%{name}/archive/v%{version}.tar.gz

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool


%description
OpenPA

%define libname libopa1
%package -n %{libname}
Summary:	OpenPA library

%description -n %{libname}
OpenPA library.

%package devel
Summary:	OpenPA devel
Group:		Development/Libraries
Requires: %{libname} = %{version}

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

%files -n %{libname}
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_includedir}
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/

%changelog
* Wed Jul 10 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.4-4
- split out versioned library into a subpackage

* Wed May 01 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.4-3
- change source to use the more consistent "archive" URL

* Mon Mar 11 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.4-2
- update to reflect move to GitHub

* Mon Aug 13 2018 Brian J. Murrell <brian.murrell@intel> - 1.0.4-1
- initial package
