%include        /usr/lib/rpm/macros.perl
Summary:	Nabou is a system integrity monitor
Summary(pl):	Nabou - narzêdzie monitoruj±ce integralno¶æ systemu
Name:		nabou
Version:	2.4
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	ftp://ftp.daemon.de/scip/Apps/nabou/%{name}-%{version}.tar.gz
# Source0-md5:	508fc306ff5816970986f5d8a320483d
Source1:	%{name}-check
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-config.patch
URL:		http://www.daemon.de/Nabou
BuildRequires:	rpm-perlprov
Requires:	crondaemon
Requires:	lsof
Requires:	perl-Config-General
Requires:	perl-Crypt-Blowfish
Requires:	perl-Crypt-CBC
Requires:	perl-Crypt-OpenSSL-RSA
Requires:	perl-Crypt-OpenSSL-Random
Requires:	perl-Crypt-Primes
Requires:	sh-utils
Requires:	smtpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautoreq      'perl(ANY_File)'

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
Nabou jest narzêdziem monitoruj±cym integralno¶æ systemu. Oznacza to,
¿e uruchamia siê ka¿dej nocy i szuka zmian w plikach. Je¿eli plik
zosta³ zmieniony w jakikolwiek sposób, mo¿e poinformowaæ o tym poczt±
elektroniczn±. Oprócz tego mo¿e szukaæ zmienionych lub dodanych kont
u¿ytkowników, prac crona, dziwnych procesów i plików z bitem suid.
Pozwala te¿ zdefiniowaæ w³asne testy.

%prep
%setup -q
%patch0 -p1
%patch1	-p1
%patch2	-p1

%build
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_pkglibdir}
install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/nabou-check

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install sample_configs/linuxrc $RPM_BUILD_ROOT%{_sysconfdir}/nabourc

rm $RPM_BUILD_ROOT%{_mandir}/man1/{nabou,nabourc}.pod

%clean
rm -rf $RPM_BUILD_ROOT

%post
%banner %{name} -e << EOF

IMPORTANT:
After generating a public/private keypair (nabou -k), according to the info, 
copy both block into your nabourc, BUT WITHOUT "sign 1" from <db> block, which 
already exists. In your config file in <db> block, change existing "sign 1" to "sign 0"

EOF

%files
%defattr(644,root,root,755)
%doc Changelog README README.modules sample_configs
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nabourc
%attr(700,root,root) %config(noreplace) /etc/cron.daily/nabou-check
%attr(755,root,root) %{_sbindir}/nabou
%attr(750,root,root) %dir %{_pkglibdir}
%{_mandir}/man1/*
