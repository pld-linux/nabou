%include        /usr/lib/rpm/macros.perl
Summary:	Nabou is a system integrity monitor
Summary(pl):	Nabou - narz�dzie monitoruj�ce integralno�� systemu
Name:		nabou
Version:	2.1
Release:	0.91
License:	GPL
Group:		Applications/System
Source0:	http://www.nabou.org/%{name}-%{version}.tar.gz
Source1:	%{name}-check
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-config.patch
URL:		http://www.nabou.org/
Requires:	crondaemon
Requires:	lsof
Requires:	smtpdaemon
BuildRequires:	perl-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautoreq      "perl(ANY_File)"

%define         _sysconfdir     /etc/%{name}
%define         _pkglibdir      /var/lib/%{name}

%description
Nabou is a system integrity monitor. That means, it runs every night
and watches for changes on files. If a file has changed in any way, it
will inform you by email (if you prefer that). Beside of this it can
also look for changed or added user accounts, cronjobs, weird
processes and suid files. And you can define your own checks using
inline scriptlets.

%description -l pl
Nabou jest narz�dziem monitoruj�cym integralno�� systemu. Oznacza to,
�e uruchamia si� ka�dej nocy i szuka zmian w plikach. Je�eli plik
zosta� zmieniony w jakikolwiek spos�b, mo�e poinformowa� o tym poczt�
elektroniczn�. Opr�cz tego mo�e szuka� zmienionych lub dodanych kont
u�ytkownik�w, prac crona, dziwnych proces�w i plik�w z bitem suid.
Pozwala te� zdefiniowa� w�asne testy.

%prep
%setup  -q
%patch0 -p1
%patch1	-p1
%patch2	-p1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/nabou-check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README sample_configs
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nabourc
%attr(700,root,root) %config(noreplace) /etc/cron.daily/nabou-check
%attr(755,root,root) %{_sbindir}/nabou
%attr(750,root,root) %dir %{_pkglibdir}
%{_mandir}/man1/*
