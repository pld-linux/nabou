%include        /usr/lib/rpm/macros.perl

Summary:	Nabou is a system integrity monitor.
Name:		nabou
Version:	2.1
Release:	0.3
License:	GPL
Group:		Applications/System
Source0:	http://www.nabou.org/%{name}-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-paths.patch
URL:		http://www.nabou.org/
BuildRequires:	perl-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/%{name}.d
%define         _pkglibdir      /var/lib/%{name}

%description
Nabou is a system integrity monitor. That means, it runs every night
and watches for changes on files. If a file has changed in any way, it
will inform you by email(if you prefer that). Beside of this it can
also look for changed or added user accounts, cronjobs, weird
processes and suid files. And you can define your own checks using
inline scriptlets.

%prep
%setup  -q
%patch0 -p1
%patch1	-p1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nabourc
%attr(755,root,root) %{_sbindir}/nabou
%attr(750,root,root) %dir %{_pkglibdir}
%{_mandir}/man1/*
