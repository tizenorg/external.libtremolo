Name:       libtremolo
Summary:    Audio Library
Version:    0.0.12
Release:    0
Group:      System/Libraries
License:    BSD-2.0 and Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%ifarch armv7el armv7l
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(mm-common)
BuildRequires: pkgconfig(mm-log)
%endif

BuildRoot:  %{_tmppath}/%{name}-%{version}-build

%description


%package devel
Summary:    Multimedia Framework Utility Library (DEV)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel

%prep
%setup -q

%build
./autogen.sh

CFLAGS="$CFLAGS -DEXPORT_API=\"__attribute__((visibility(\\\"default\\\")))\" -D_MM_PROJECT_FLOATER" \
LDFLAGS+="-Wl,--rpath=%{_prefix}/lib -Wl,--hash-style=both -Wl,--as-needed,-z,noexecstack" \
./configure --prefix=%{_prefix}
make %{?jobs:-j%jobs}

sed -i -e "s#@TREMOLO_REQPKG@#$TREMOLO_REQPKG#g" tremolo/libtremolo.pc

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/license
cp COPYING %{buildroot}/usr/share/license/%{name}
%make_install
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
/usr/share/license/%{name}
%manifest libtremolo.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so*
/usr/share/license/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*
