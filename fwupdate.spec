%global efivar_version 0.16

Name:           fwupdate
Version:        0.1
Release:        2%{?dist}
Summary:        Tools to manage UEFI firmware updates
License:        GPLv2+
URL:            https://github.com/rhinstaller/fwupdate
Requires:       %{name}-libs = %{version}-%{release}
Requires:	efibootmgr >= 0.11.0-2
BuildRequires:	efivar-devel >= %{efivar_version}
ExclusiveArch:	x86_64 %{ix86} aarch64

BuildRequires:  popt-devel git

%ifarch x86_64
%global efiarch x64
%endif
%ifarch %{ix86}
%global efiarch ia32
%endif
%ifarch aarch64
%global efiarch aa64
%endif

# Figure out the right file path to use
%if 0%{?rhel}
%global efidir redhat
%endif
%if 0%{?fedora}
%global efidir fedora
%endif

Source0:        https://github.com/rhinstaller/fwupdate/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2

%description
fwupdate provides a simple command line interface to the UEFI firmware updates.

%package libs
Summary: Library to manage UEFI firmware updates.

%description libs
Library to allow for the simple manipulation of UEFI firmware updates.

%package devel
Summary: Development headers for linfwup
Requires: %{name}-libs = %{version}-%{release}
Requires: efivar-devel >= %{efivar_version}

%description devel
development headers required to use libfwup.

%prep
%setup -q -n %{name}-%{version}
git init
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null

%build
make OPT_FLAGS="$RPM_OPT_FLAGS" libdir=%{_libdir} bindir=%{_bindir} \
	EFIDIR=%{efidir}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall EFIDIR=%{efidir} DESTDIR=${RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
efibootmgr -b 1337 -B || :
efibootmgr -C -b 1337 -d /dev/sda -p 1 -l /efi/%{efidir}/fwupdate.efi -L "Firmware Update"

%postun libs -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
# %%doc README
%{_bindir}/fwupdate
/boot/efi/EFI/%{efidir}/fwupdate.efi
%{_datadir}/locale/en/*.po
#%{_mandir}/man1/*

%files devel
#%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files libs
%{_libdir}/*.so.*

%changelog
* Fri Feb 27 2015 Peter Jones <pjones@redhat.com> - 0.1-1
- Here we go again.


