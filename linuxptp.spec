Name:		linuxptp
Version:	2.0
Release:        4
Summary:	Linuxptp is an implementation of the Precision Time Protocol (PTP)
Group:		System Environment/Base
License:	GPLv2+
URL:		http://linuxptp.sourceforge.net/
Source0:	https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tgz
Source1:	phc2sys.service
Source2:	ptp4l.service

Patch0001:      CVE-2021-3570.patch

BuildRequires:	gcc gcc-c++ systemd git net-tools


%description
Linuxptp is an implementation of the Precision Time Protocol (PTP) according to
IEEE standard 1588 for Linux. The dual design goals are to provide a robust
implementation of the standard and to use the most relevant and modern Application
Programming Interfaces (API) offered by the Linux kernel. Supporting legacy APIs
and other platforms is not a goal.


%package        help
Summary:        Help files for %{name}
BuildArch:      noarch


%description    help
Help files for %{name}


%prep
%autosetup -n %{name}-%{version}

%build
%make_build EXTRA_CFLAGS="$RPM_OPT_FLAGS" \
	    EXTRA_LDFLAGS="$RPM_LD_FLAGS"


%install
%makeinstall

mkdir -p %{buildroot}{%{_sysconfdir}/sysconfig,%{_unitdir}}
install -m 644 -p configs/default.cfg %{buildroot}%{_sysconfdir}/ptp4l.conf
install -m 644 -p %{SOURCE1} %{SOURCE2} %{buildroot}%{_unitdir}

echo 'OPTIONS="-f /etc/ptp4l.conf -i eth0"' > \
	%{buildroot}%{_sysconfdir}/sysconfig/ptp4l
echo 'OPTIONS="-a -r"' > %{buildroot}%{_sysconfdir}/sysconfig/phc2sys
%post
%systemd_post phc2sys.service ptp4l.service

%preun
%systemd_preun phc2sys.service ptp4l.service

%postun
%systemd_postun_with_restart phc2sys.service ptp4l.service


%files
%doc README.org configs
%license COPYING
%config(noreplace) %{_sysconfdir}/ptp4l.conf
%config(noreplace) %{_sysconfdir}/sysconfig/phc2sys
%config(noreplace) %{_sysconfdir}/sysconfig/ptp4l
%{_unitdir}/phc2sys.service
%{_unitdir}/ptp4l.service
%{_sbindir}/hwstamp_ctl
%{_sbindir}/nsm
%{_sbindir}/phc2sys
%{_sbindir}/phc_ctl
%{_sbindir}/pmc
%{_sbindir}/ptp4l
%{_sbindir}/timemaster


%files  help
%{_mandir}/man8/*.8*

%changelog
* Wed Sep 22 2021 yaoxin <yaoxin30@huawei.com> 2.0-4
- Fix CVE-2021-3570

* Thu Nov 28 2019 openEuler BuildTeam<buildteam@openeuler.org> 2.0-3
- Package Init

