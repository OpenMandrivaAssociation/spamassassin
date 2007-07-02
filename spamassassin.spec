%define fname Mail-SpamAssassin

Summary:	A spam filter for email which can be invoked from mail delivery agents
Name:		spamassassin
Version:	3.2.1
Release:	%mkrel 1
License:	Apache License
Group:		Networking/Mail
URL:		http://spamassassin.org/
Source0:	http://www.apache.org/dist/spamassassin/source/%{fname}-%{version}.tar.gz
Source1:	http://www.apache.org/dist/spamassassin/source/%{fname}-%{version}.tar.gz.asc
Source2:	spamd.init
Source3:	spamd.sysconfig
Source4:	spamassassin-default.rc
Source5:	spamassassin-spamc.rc
Source6:	sa-update.cron
# (fc) 2.60-5mdk don't use version dependent perl call in #!
Patch0:		spamassassin-3.2.0-fixbang.patch
Patch1:		Mail-SpamAssassin-3.1.5-no_spamcop.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	openssl-devel
BuildRequires:	perl-Archive-Tar
BuildRequires:	perl-Digest-SHA1
BuildRequires:	perl-HTML-Parser
BuildRequires:	perl-INET6
BuildRequires:	perl-IO-Socket-SSL
BuildRequires:	perl-IO-Zlib
BuildRequires:	perl-IP-Country
BuildRequires:	perl-Mail-SPF-Query
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Net-Ident
BuildRequires:	perl-Time-HiRes
BuildRequires:	perl-devel
BuildRequires:	perl-DB_File
BuildRequires:	perl-libwww-perl
Requires:	perl-Mail-SpamAssassin = %{version}
Requires:	perl-Net-DNS
Requires:  	perl-DB_File
# (oe) these are not required, but if not it cripples the SpamAssassin functionalities
Requires:	perl-Archive-Tar
Requires:	perl-INET6
Requires:	perl-IO-Socket-SSL
Requires:	perl-IO-Zlib
Requires:	perl-IP-Country
Requires:	perl-Mail-SPF-Query
Requires:	perl-Net-Ident
Requires:	perl-Sys-Hostname-Long 
Requires:	perl-libwww-perl
Requires:	perl-Encode-Detect
Requires:	perl-Mail-SPF
Requires:	gnupg
Buildroot:	%{_tmppath}/%{name}-%{version}-root

%description
SpamAssassin provides you with a way to reduce if not completely eliminate
Unsolicited Commercial Email (SPAM) from your incoming email.  It can
be invoked by a MDA such as sendmail or postfix, or can be called from
a procmail script, .forward file, etc.  It uses a genetic-algorithm
evolved scoring system to identify messages which look spammy, then
adds headers to the message so they can be filtered by the user's mail
reading software.  This distribution includes the spamd/spamc components
which create a server that considerably speeds processing of mail.

SpamAssassin also includes support for reporting spam messages
automatically, and/or manually, to collaborative filtering databases such
as Vipul's Razor, DCC or pyzor. 
Install perl-Razor-Agent package to get Vipul's Razor support. 
Install dcc package to get Distributed Checksum Clearinghouse (DCC) support.
Install pyzor package to get Pyzor support.
Install perl-Mail-SPF-Query package to get SPF support.

To enable spamassassin, if you are receiving mail locally, simply add
this line to your ~/.procmailrc:
INCLUDERC=/etc/mail/spamassassin/spamassassin-default.rc
 
To filter spam for all users, add that line to /etc/procmailrc
(creating if necessary).


%package	tools
Summary:        Miscleanous tools for SpamAssassin
Group:		Networking/Mail
Requires:	perl-Mail-SpamAssassin = %{version}

%description	tools
Miscleanous tools from various authors, distributed with SpamAssassin.
See /usr/share/doc/spamassassin-tools-*/.

%package	spamd
Summary:	Daemonized version of SpamAssassin
Group:		System/Servers
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	spamassassin = %{version}

%description	spamd
The purpose of this program is to provide a daemonized version of the
spamassassin executable. The goal is improving throughput performance
for automated mail checking.

This is intended to be used alongside "spamc", a fast, low-overhead C
client program.

%package	spamc
Summary:	A client for spamd
Group:		Networking/Mail

%description	spamc
Spamc is the client half of the spamc/spamd pair. It should be used in
place of "spamassassin" in scripts to process mail. It will read the
mail from STDIN, and spool it to its connection to spamd, then read
the result back and print it to STDOUT. Spamc has extremely low
overhead in loading, so it should be much faster to load than the
whole spamassassin program.

%package -n	perl-%{fname}
Summary:        Mail::SpamAssassin -- SpamAssassin e-mail filter Perl modules
Group:		Development/Perl

%description -n perl-%{fname}
Mail::SpamAssassin is a module to identify spam using text analysis and
several internet-based realtime blacklists. Using its rule base, it uses a
wide range of heuristic tests on mail headers and body text to identify
``spam'', also known as unsolicited commercial email. Once identified, the
mail can then be optionally tagged as spam for later filtering using the
user's own mail user-agent application.

%prep

%setup -q -n %{fname}-%{version}
%patch0 -p1 -b .fixbang
%patch1 -p0

cp %{SOURCE2} spamd.init
cp %{SOURCE3} spamd.sysconfig
cp %{SOURCE6} sa-update.cron

%build

%{__perl} \
    Makefile.PL \
    INSTALLDIRS=vendor \
    SYSCONFDIR=%{_sysconfdir} \
    DATADIR=%{_datadir}/spamassassin \
    ENABLE_SSL=yes \
    RUN_NET_TESTS=no < /dev/null

%make OPTIMIZE="%{optflags}" 

#cat >> t/config.dist << EOF
#run_net_tests=y
#run_spamd_prefork_stress_test=y
#EOF

%check
export LANG=C 
export LC_ALL=C
export LANGUAGE=C
make FULLPERL="%{_bindir}/perl" test

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_sysconfdir}/mail/%{name}/sa-update-keys
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/cron.daily
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/spool/spamassassin
install -d %{buildroot}%{_localstatedir}/spamassassin

cat << EOF >> %{buildroot}%{_sysconfdir}/mail/%{name}/local.cf
required_hits 5
rewrite_header Subject [SPAM]
report_safe 0
auto_whitelist_path        /var/spool/spamassassin/auto-whitelist
auto_whitelist_file_mode   0666
EOF

install -m0755 spamd.init %{buildroot}%{_initrddir}/spamd
install -m0644 spamd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/spamd
install -m0755 sa-update.cron %{buildroot}%{_sysconfdir}/cron.daily/sa-update

install -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/mail/spamassassin/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
[ -f %{_sysconfdir}/spamassassin.cf ] && %{__mv} %{_sysconfdir}/spamassassin.cf %{_sysconfdir}/mail/spamassassin/migrated.cf || true
[ -f %{_sysconfdir}/mail/spamassassin.cf ] && /bin/mv %{_sysconfdir}/mail/spamassassin.cf %{_sysconfdir}/mail/spamassassin/migrated.cf || true

%post spamd
# -a and --auto-whitelist options were removed from 3.0.0
# prevent service startup failure
perl -p -i -e 's/(["\s]-\w+)a/$1/ ; s/(["\s]-)a(\w+)/$1$2/ ; s/(["\s])-a\b/$1/' /etc/sysconfig/spamd
perl -p -i -e 's/ --auto-whitelist//' /etc/sysconfig/spamd

# fix permissions
if [ -f %{_sysconfdir}/mail/%{name}/local.cf ]; then

    auto_whitelist_path="`grep "^auto_whitelist_path" %{_sysconfdir}/mail/%{name}/local.cf | awk '{ print $2 }'`"
    auto_whitelist_file_mode="`grep "^auto_whitelist_file_mode" %{_sysconfdir}/mail/%{name}/local.cf | awk '{ print $2 }'`"

    if [ "${auto_whitelist_path}" == "/var/spool/%{name}" ]; then
	echo "Correcting \"auto_whitelist_path\" (#27424) in the %{_sysconfdir}/mail/%{name}/local.cf file..."
	perl -pi -e "s|/var/spool/%{name}\b|/var/spool/%{name}/auto-whitelist|g" %{_sysconfdir}/mail/%{name}/local.cf
	auto_whitelist_path="/var/spool/%{name}/auto-whitelist"
    fi

    if ! [ -z "${auto_whitelist_path}" ]; then
        touch ${auto_whitelist_path}
        if [ -z "${auto_whitelist_file_mode}" ]; then
            auto_whitelist_file_mode="0666"
        fi
        chmod ${auto_whitelist_file_mode} ${auto_whitelist_path}
    fi

fi

%_post_service spamd

%preun spamd
%_preun_service spamd

%files
%defattr(-,root,root)
%doc README Changes sample-*.txt procmailrc.example INSTALL TRADEMARK
%doc CREDITS UPGRADE USAGE
%dir %{_sysconfdir}/mail/%{name}
%dir %{_sysconfdir}/mail/%{name}/sa-update-keys
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/%{name}/*.cf
%config(noreplace) %{_sysconfdir}/mail/%{name}/*.pre
%config(noreplace) %{_sysconfdir}/mail/%{name}/spamassassin-default.rc
%dir %attr(0777,root,root) /var/spool/spamassassin
%dir %{_localstatedir}/spamassassin
%attr(0755,root,root) %{_bindir}/sa-compile
%attr(0755,root,root) %{_bindir}/sa-learn
%attr(0755,root,root) %{_bindir}/spamassassin
%attr(0755,root,root) %{_bindir}/sa-update
%{_mandir}/man1/sa-compile.1*
%{_mandir}/man1/sa-learn.1*
%{_mandir}/man1/spamassassin.1*
%{_mandir}/man1/sa-update.1*
%{_mandir}/man1/spamassassin-run.1*
%{_datadir}/spamassassin

%files tools
%defattr(-,root,root)
%doc sql ldap

%files spamd
%defattr(-,root,root)
%doc spamd/README* spamd/PROTOCOL
%attr(0755,root,root) %{_sysconfdir}/cron.daily/sa-update
%attr(0755,root,root) %{_initrddir}/spamd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/spamd
%attr(0755,root,root) %{_bindir}/spamd
%{_mandir}/man1/spamd.1*

%files spamc
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/mail/%{name}/spamassassin-spamc.rc
%attr(0755,root,root) %{_bindir}/spamc
%{_mandir}/man1/spamc.1*

%files -n perl-%{fname}
%defattr(644,root,root,755)
%dir %{perl_vendorlib}/Mail
%{perl_vendorlib}/Mail/SpamAssassin*
%{perl_vendorlib}/spamassassin-run.pod
%{_mandir}/man3*/*


