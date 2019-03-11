Name:		openpa
Version:	1.0.4
Release:	2%{?dist}

Summary:	OpenPA

Group:		Development/Libraries
License:	ANL
URL:		https://github.com/pmodels/openpa
Source0:	https://github.com/pmodels/openpa/releases/download/v%{version}/openpa-%{version}.tar.gz

%description
OpenPA

%package devel
Summary:	OpenPA devel

Group:		Development/Libraries

%description devel
OpenPA devel

%prep 
%setup -q

%build
%configure --enable-shared
make %{?_smp_mflags}

%install
%make_install
find /home/brian/daos/openpa/_topdir/BUILDROOT/openpa-%{version}-1.el7.centos.x86_64 | xargs ls -ld

%files
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_includedir}
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/

%changelog
* Mon Mar 11 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.4-2
- update to reflect move to GitHub
* Mon Aug 13 2018 Brian J. Murrell <brian.murrell@intel> - 1.0.4-1
- initial package
