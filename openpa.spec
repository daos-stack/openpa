Name:		openpa
Version:	1.0.4
Release:	1%{?dist}

Summary:	OpenPA

Group:		Development/Libraries
License:	ANL
URL:		http://mercury-hpc.github.io/documentation/
Source0:	https://trac.mpich.org/projects/openpa/raw-attachment/wiki/Downloads/openpa-1.0.4.tar.gz

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
find /home/brian/daos/openpa/_topdir/BUILDROOT/openpa-1.0.4-1.el7.centos.x86_64 | xargs ls -ld

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
* Mon Aug 13 2018 Brian J. Murrell <brian.murrell@intel> - 1.0.4-1
- initial package

