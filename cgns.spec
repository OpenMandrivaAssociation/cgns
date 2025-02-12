# Can't mix clang LTO with gcc (gfortran) LTO
%define _disable_lto 1

%define major           3.3
%define libname         %mklibname %{name} %{major}
%define libname_devel   %mklibname %{name} -d

%define srcname         CGNS

Name:    cgns
Version: 4.5.0
Release: 2
Summary: Computational fluid dynamics notation system
License: zlib
Group:   Sciences/Physics
URL:     https://cgns.github.io
Source0: https://github.com/CGNS/CGNS/archive/refs/tags/v%{version}.tar.gz

Patch1:  cgns-3.3.1-libdir.patch
Patch2:  cgns-4.5.0-buildfix.patch

BuildRequires: cmake
BuildRequires: gcc-gfortran
BuildRequires: hdf5-devel
BuildRequires: pkgconfig(x11)
BuildRequires: tcl
BuildRequires: pkgconfig(tcl)
BuildRequires: pkgconfig(tk)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glu)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xmu)

%description
The CFD General Notation System (CGNS) provides a general, portable,
and extensible standard for the storage and retrieval of computational
fluid dynamics (CFD) analysis data. It consists of a collection of
conventions, and free and open software implementing those
conventions. It is self-descriptive, machine-independent,
well-documented, and administered by an international steering
committee.

%package -n %{libname}
Summary:        Libraries for CGNS
Group:          System/Libraries
Obsoletes:	%{_lib}cgns3 < 3.3.1-2

%description -n %{libname}
%{summary}.

%package -n %{libname_devel}
Summary:        Development files for CGNS
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}cgns-static-devel < 3.3.1-2

%description -n %{libname_devel}
This package provides the CGNS header and module files required to
compile C and Fortran programs that use CNGS.

%prep
%setup -q -n %{srcname}-%{version}
%autopatch -p1

%build
%cmake                                                              \
        -DCGNS_ENABLE_FORTRAN:BOOL=ON                               \
	-DCGNS_BUILD_CGNSTOOLS:BOOL=ON                              \
	-DCGNS_ENABLE_HDF5:BOOL=ON                                  \
	-DCGNS_BUILD_SHARED:BOOL=ON                                 \
	-DHDF5_NEED_ZLIB:BOOL=ON                                    \
%ifarch %{x86_64} %{aarch64}
        -DCGNS_ENABLE_64BIT:BOOL=ON
%endif

%make_build

%install
%make_install -C build

# drop static build
rm -rf %{buildroot}%{_libdir}/libcgns.a

%files
%doc README.md license.txt
%{_bindir}/*
%{_datadir}/cgnstools

%files -n %{libname}
%{_libdir}/libcgns.so.%{major}

%files -n %{libname_devel}
%{_includedir}/*
%{_libdir}/libcgns.so
