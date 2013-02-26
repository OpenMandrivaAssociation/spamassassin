%define fname Mail-SpamAssassin
%define svn_snap r1128990

Summary:	A spam filter for email which can be invoked from mail delivery agents
Name:		spamassassin
Version:	3.3.2
Release:	4
License:	Apache License
Group:		Networking/Mail
URL:		http://spamassassin.apache.org/
Source0:	http://www.apache.org/dist/spamassassin/source/%{fname}-%{version}.tar.gz
Source1:	http://www.apache.org/dist/spamassassin/source/%{fname}-%{version}.tar.gz.asc
#svn co https://svn.apache.org/repos/asf/spamassassin/branches/3.3 spamassassin-3.3.x
#Source0:	%{fname}-3.3.x.tar.gz
Source2:	spamd.init
Source3:	spamd.sysconfig
Source4:	spamassassin-default.rc
Source5:	spamassassin-spamc.rc
Source6:	sa-update.cron
Source7:	spamd.logrotate
Source8:	spamd.conf
# (fc) 2.60-5mdk don't use version dependent perl call in #!
Patch0:		spamassassin-3.2.0-fixbang.patch
Patch1:		Mail-SpamAssassin-3.1.5-no_spamcop.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	gnupg
BuildRequires:	openssl-devel
BuildRequires:	perl-Apache-Test
BuildRequires:	perl(Archive::Tar)
BuildRequires:	perl-DB_File
BuildRequires:	perl-devel
BuildRequires:	perl(Digest::SHA)
BuildRequires:	perl-Encode-Detect
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.17
BuildRequires:	perl-HTML-Parser
BuildRequires:	perl(IO::Socket::INET6)
BuildRequires:	perl-IO-Socket-SSL
BuildRequires:	perl-IO-Zlib
BuildRequires:	perl-IP-Country
BuildRequires:	perl-libwww-perl
BuildRequires:	perl-Mail-DKIM >= 0.37
BuildRequires:	perl-Mail-SPF
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Net-Ident
BuildRequires:	perl-Socket6
BuildRequires:	perl-Sys-Hostname-Long
BuildRequires:	perl-Time-HiRes
BuildRequires:	perl-version
BuildRequires:	re2c
Requires:	perl-Mail-SpamAssassin >= %{version}
Requires:	perl(Archive::Tar)
Requires:  	perl-DB_File
Requires:	perl(NetAddr::IP)
Requires:	perl-Net-DNS
Requires:	perl(Time::HiRes)
Requires:	spamassassin-rules >= 3.3.0
# (oe) these are not required, but if not it cripples the SpamAssassin functionalities
Suggests:	gnupg perl(Digest::SHA) perl-Encode-Detect perl-IO-Socket-SSL perl-IO-Zlib perl-IP-Country perl-libwww-perl perl-Mail-DKIM >= 0.37 perl-Mail-SPF perl-Net-Ident perl-Sys-Hostname-Long perl-version

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

To enable spamassassin, if you are receiving mail locally, simply add
this line to your ~/.procmailrc:
INCLUDERC=/etc/mail/spamassassin/spamassassin-default.rc
 
To filter spam for all users, add that line to /etc/procmailrc
(creating if necessary).

%package	sa-compile
Summary:	Compiles SpamAssassin rulesets into native perl code
Group:		Networking/Mail
Requires:	gcc make
Requires:	perl-devel
Requires:	re2c
Conflicts:	spamassassin < 3.2.5-3

%description	sa-compile
sa-compile uses re2c to compile the site-wide parts of the SpamAssassin
ruleset. No part of user_prefs or any files included from user_prefs can be
built into the compiled set. This compiled set is then used by the
"Mail::SpamAssassin::Plugin::Rule2XSBody" plugin to speed up SpamAssassin's
operation, where possible, and when that plugin is loaded. re2c can match
strings much faster than perl code, by constructing a DFA to match many simple
strings in parallel, and compiling that to native object code. Not all
SpamAssassin rules are amenable to this conversion, however.

%package	tools
Summary:        Miscleanous tools for SpamAssassin
Group:		Networking/Mail
Requires:	perl-Mail-SpamAssassin >= %{version}

%description	tools
Miscleanous tools from various authors, distributed with SpamAssassin.
See /usr/share/doc/spamassassin-tools-*/.

%package	spamd
Summary:	Daemonized version of SpamAssassin
Group:		System/Servers
Requires(post): rpm-helper spamassassin-rules >= 3.3.0
Requires(preun): rpm-helper
Requires:	spamassassin >= %{version}

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
Summary:        SpamAssassin e-mail filter Perl modules
Group:		Development/Perl
Requires:       perl(HTML::Parser)

%description -n perl-%{fname}
Mail::SpamAssassin is a module to identify spam using text analysis and
several internet-based realtime blacklists. Using its rule base, it uses a
wide range of heuristic tests on mail headers and body text to identify
``spam'', also known as unsolicited commercial email. Once identified, the
mail can then be optionally tagged as spam for later filtering using the
user's own mail user-agent application.

%package -n	perl-%{fname}-Spamd
Summary:        A mod_perl2 module implementing the spamd protocol
Group:		Development/Perl
Requires:       apache-mod_perl

%description -n	perl-%{fname}-Spamd
This distribution contains a mod_perl2 module, implementing the spamd protocol
from the SpamAssassin (http://spamassassin.apache.org/) project in Apache2.
It's mostly compatible with the original spamd.

%prep

%setup -q -n %{fname}-%{version}
%patch0 -p0 -b .fixbang
%patch1 -p0

cp %{SOURCE2} spamd.init
cp %{SOURCE3} spamd.sysconfig
cp %{SOURCE6} sa-update.cron
cp %{SOURCE7} spamd.logrotate
cp %{SOURCE8} spamd.conf

# svn cleansing...
for i in `find . -type d -name .svn`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
%serverbuild

%{__perl} \
    Makefile.PL \
    INSTALLDIRS=vendor \
    SYSCONFDIR=%{_sysconfdir} \
    DATADIR=%{_datadir}/spamassassin \
    ENABLE_SSL=yes \
    RUN_NET_TESTS=no < /dev/null

%make

pushd spamd-apache2
    %{__perl} Makefile.PL INSTALLDIRS=vendor < /dev/null
    %make
popd

%check
#cat >> t/config.dist << EOF
#run_net_tests=y
#run_spamd_prefork_stress_test=y
#EOF
export LANG=C 
export LC_ALL=C
export LANGUAGE=C
# useless and broken test case
rm -f t/make_install.t
# requires polish locales?!?
rm -f t/lang_pl_tests.t
# probably borked ssl tests or temporary issues
rm -f t/spamd_ssl.t t/spamd_ssl_accept_fail.t t/spamd_ssl_tls.t t/spamd_ssl_v2.t t/spamd_ssl_v23.t t/spamd_ssl_v3.t
make FULLPERL="%{_bindir}/perl" test

%install
%makeinstall_std

pushd spamd-apache2
    %makeinstall_std
popd

install -d %{buildroot}%{_sysconfdir}/mail/%{name}/sa-update-keys
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/cron.daily
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/spool/spamassassin
install -d %{buildroot}/var/log/spamassassin
install -d %{buildroot}/var/lib/spamassassin
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d

cat << EOF >> %{buildroot}%{_sysconfdir}/mail/%{name}/v330.pre

# Mail::SpamAssassin::Plugin::AWL - Normalize scores via auto-whitelist
loadplugin Mail::SpamAssassin::Plugin::AWL
EOF

cat << EOF >> %{buildroot}%{_sysconfdir}/mail/%{name}/local.cf
required_hits 5
rewrite_header Subject [SPAM]
report_safe 0
ifplugin Mail::SpamAssassin::Plugin::AWL
auto_whitelist_path        /var/spool/spamassassin/auto-whitelist
auto_whitelist_file_mode   0666
endif # Mail::SpamAssassin::Plugin::AWL
EOF

install -m0755 spamd.init %{buildroot}%{_initrddir}/spamd
install -m0644 spamd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/spamd
install -m0755 sa-update.cron %{buildroot}%{_sysconfdir}/cron.daily/sa-update
install -m0644 spamd.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/spamd
install -m0644 spamd.conf %{buildroot}/%{_sysconfdir}/httpd/conf/webapps.d/spamd.conf

install -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/mail/spamassassin/

# bork bork
install -m0644 rules/*.pre %{buildroot}%{_sysconfdir}/mail/%{name}/

# cleanup
rm -f %{buildroot}%{_bindir}/apache-spamd.pl
rm -f %{buildroot}%{_mandir}/man1/apache-spamd.pl.1*

# these are not meant to be relased
rm -f %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin/P595Body.pm
rm -f %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin/RabinKarpBody.pm

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
%doc README Changes sample-*.txt procmailrc.example INSTALL TRADEMARK
%doc CREDITS UPGRADE USAGE
%dir %{_sysconfdir}/mail/%{name}
%dir %attr(0700,root,root) %{_sysconfdir}/mail/%{name}/sa-update-keys
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/%{name}/*.cf
%config(noreplace) %{_sysconfdir}/mail/%{name}/*.pre
%config(noreplace) %{_sysconfdir}/mail/%{name}/spamassassin-default.rc
%dir %attr(0777,root,root) /var/spool/spamassassin
%dir /var/lib/spamassassin
%attr(0755,root,root) %{_bindir}/sa-awl
%attr(0755,root,root) %{_bindir}/sa-check_spamd
%attr(0755,root,root) %{_bindir}/sa-learn
%attr(0755,root,root) %{_bindir}/sa-update
%attr(0755,root,root) %{_bindir}/spamassassin
%{_mandir}/man1/sa-learn.1*
%{_mandir}/man1/spamassassin.1*
%{_mandir}/man1/sa-update.1*
%{_mandir}/man1/spamassassin-run.1*
%{_mandir}/man1/sa-awl.1*
%{_datadir}/spamassassin

%files sa-compile
%attr(0755,root,root) %{_bindir}/sa-compile
%{_mandir}/man1/sa-compile.1*

%files tools
%doc sql ldap

%files spamd
%doc spamd/README* spamd/PROTOCOL
%attr(0700,root,root) %{_sysconfdir}/cron.daily/sa-update
%attr(0755,root,root) %{_initrddir}/spamd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/spamd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/spamd
%attr(0755,root,root) %{_bindir}/spamd
%{_mandir}/man1/spamd.1*
%dir %attr(0755,root,root) /var/log/spamassassin

%files spamc
%config(noreplace) %{_sysconfdir}/mail/%{name}/spamassassin-spamc.rc
%attr(0755,root,root) %{_bindir}/spamc
%{_mandir}/man1/spamc.1*

%files -n perl-%{fname}
%dir %{perl_vendorlib}/Mail/SpamAssassin
%{perl_vendorlib}/Mail/SpamAssassin/*.pm
%exclude %{perl_vendorlib}/Mail/SpamAssassin/Spamd.pm
%{perl_vendorlib}/Mail/SpamAssassin.pm
%{perl_vendorlib}/spamassassin-run.pod
%dir %{perl_vendorlib}/Mail/SpamAssassin/Bayes
%dir %{perl_vendorlib}/Mail/SpamAssassin/BayesStore
%dir %{perl_vendorlib}/Mail/SpamAssassin/Conf
%dir %{perl_vendorlib}/Mail/SpamAssassin/Locker
%dir %{perl_vendorlib}/Mail/SpamAssassin/Logger
%dir %{perl_vendorlib}/Mail/SpamAssassin/Message
%dir %{perl_vendorlib}/Mail/SpamAssassin/Message/Metadata
%dir %{perl_vendorlib}/Mail/SpamAssassin/Plugin
%dir %{perl_vendorlib}/Mail/SpamAssassin/Util
%{perl_vendorlib}/Mail/SpamAssassin/Bayes/*.pm
%{perl_vendorlib}/Mail/SpamAssassin/BayesStore/*.pm
%{perl_vendorlib}/Mail/SpamAssassin/Conf/*.pm
%{perl_vendorlib}/Mail/SpamAssassin/Locker/*.pm
%{perl_vendorlib}/Mail/SpamAssassin/Logger/*.pm
%{perl_vendorlib}/Mail/SpamAssassin/Message/Metadata/*.pm
%{perl_vendorlib}/Mail/SpamAssassin/Message/*.pm
%{perl_vendorlib}/Mail/SpamAssassin/Plugin/*.pm
%{perl_vendorlib}/Mail/SpamAssassin/Util/*.pm
%{_mandir}/man3/Mail::SpamAssassin.3pm*
%{_mandir}/man3/Mail::SpamAssassin::AICache.3pm*
%{_mandir}/man3/Mail::SpamAssassin::ArchiveIterator.3pm*
%{_mandir}/man3/Mail::SpamAssassin::AsyncLoop.3pm*
%{_mandir}/man3/Mail::SpamAssassin::AutoWhitelist.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Bayes.3pm*
%{_mandir}/man3/Mail::SpamAssassin::BayesStore.3pm*
%{_mandir}/man3/Mail::SpamAssassin::BayesStore::BDB.3pm*
%{_mandir}/man3/Mail::SpamAssassin::BayesStore::MySQL.3pm*
%{_mandir}/man3/Mail::SpamAssassin::BayesStore::PgSQL.3pm*
%{_mandir}/man3/Mail::SpamAssassin::BayesStore::SQL.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Client.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Conf.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Conf::LDAP.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Conf::Parser.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Conf::SQL.3pm*
%{_mandir}/man3/Mail::SpamAssassin::DnsResolver.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Logger.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Logger::File.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Logger::Stderr.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Logger::Syslog.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Message.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Message::Metadata.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Message::Node.3pm*
%{_mandir}/man3/Mail::SpamAssassin::PerMsgLearner.3pm*
%{_mandir}/man3/Mail::SpamAssassin::PerMsgStatus.3pm*
%{_mandir}/man3/Mail::SpamAssassin::PersistentAddrList.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::AccessDB.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::AntiVirus.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::ASN.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::AutoLearnThreshold.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::AWL.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::Bayes.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::BodyRuleBaseExtractor.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::Check.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::DCC.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::DKIM.3pm*
%{_mandir}/man3/Mail::SpamAssassin::PluginHandler.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::Hashcash.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::MIMEHeader.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::OneLineBodyRuleType.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::PhishTag.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::Pyzor.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::Razor2.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::RelayCountry.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::ReplaceTags.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::Reuse.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::Rule2XSBody.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::Shortcircuit.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::SpamCop.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::SPF.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::Test.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::TextCat.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::URIDetail.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::URIDNSBL.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::VBounce.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Plugin::WhiteListSubject.3pm*
%{_mandir}/man3/Mail::SpamAssassin::SQLBasedAddrList.3pm*
%{_mandir}/man3/Mail::SpamAssassin::SubProcBackChannel.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Timeout.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Util.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Util::DependencyInfo.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Util::Progress.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Util::RegistrarBoundaries.3pm*
%{_mandir}/man3/spamassassin-run.3pm*

%files -n perl-%{fname}-Spamd
%doc spamd-apache2/README.apache
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/spamd.conf
%dir %{perl_vendorlib}/Mail/SpamAssassin/Spamd
%{perl_vendorlib}/Mail/SpamAssassin/Spamd/Apache2.pm
%{perl_vendorlib}/Mail/SpamAssassin/Spamd/Config.pm
%{perl_vendorlib}/Mail/SpamAssassin/Spamd.pm
%dir %{perl_vendorlib}/Mail/SpamAssassin/Spamd/Apache2
%{perl_vendorlib}/Mail/SpamAssassin/Spamd/Apache2/AclRFC1413.pm
%{perl_vendorlib}/Mail/SpamAssassin/Spamd/Apache2/Config.pm
%{perl_vendorlib}/Mail/SpamAssassin/Spamd/Apache2/AclIP.pm
%{_mandir}/man3/Mail::SpamAssassin::Spamd.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Spamd::Apache2.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Spamd::Apache2::AclIP.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Spamd::Apache2::AclRFC1413.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Spamd::Apache2::Config.3pm*
%{_mandir}/man3/Mail::SpamAssassin::Spamd::Config.3pm*


%changelog
* Mon Jan 23 2012 Oden Eriksson <oeriksson@mandriva.com> 3.3.2-3mdv2012.0
+ Revision: 766780
- various fixes
- rebuilt for perl-5.14.2

* Thu Oct 06 2011 Oden Eriksson <oeriksson@mandriva.com> 3.3.2-2
+ Revision: 703222
- bumpd release (stupid bs)
- disable the ssl tests for now...
- svn and release versions differ a bit...
- fix build and deps
- 3.3.2

* Mon May 30 2011 Oden Eriksson <oeriksson@mandriva.com> 3.3.2-0.0.r1128990.1
+ Revision: 681794
- new snap (r1128990)
- use the %%serverbuild macro

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 3.3.2-0.0.r1036809.2
+ Revision: 670005
- mass rebuild

* Wed Nov 24 2010 Michael Scherer <misc@mandriva.org> 3.3.2-0.0.r1036809.1mdv2011.0
+ Revision: 600841
- make is needed to compile the rule, since it use a makefile

* Fri Nov 19 2010 Oden Eriksson <oeriksson@mandriva.com> 3.3.2-0.0.r1036809.0mdv2011.0
+ Revision: 599069
- 3.3.2 (r1036809)
- fixes #60540 (Spamassassin has an error after upgrading the new Perl)
- since %%exclude don't work, add ugly file lists
- note: at least perl-NetAddr-IP-4.36.0-1mdv2011.0 and perl-5.12.2-5mdv2011.0
  is required for it to pass "make test"

  + Thomas Spuhler <tspuhler@mandriva.org>
    - Increased release for rebuild

  + Rémy Clouard <shikamaru@mandriva.org>
    - fix URL as reported by Charles A Edwards

* Fri Apr 09 2010 Funda Wang <fwang@mandriva.org> 3.3.1-3mdv2010.1
+ Revision: 533336
- rebuild

* Mon Mar 22 2010 Ahmad Samir <ahmadsamir@mandriva.org> 3.3.1-2mdv2010.1
+ Revision: 526336
- rebuild for missing packages (on x86_64)

* Sun Mar 21 2010 Funda Wang <fwang@mandriva.org> 3.3.1-1mdv2010.1
+ Revision: 526012
- new version 3.3.1

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 3.3.0-3mdv2010.1
+ Revision: 511639
- rebuilt against openssl-0.9.8m

* Mon Feb 08 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.3.0-2mdv2010.1
+ Revision: 502379
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Wed Jan 27 2010 Oden Eriksson <oeriksson@mandriva.com> 3.3.0-1mdv2010.1
+ Revision: 497064
- 3.3.0

* Tue Jan 26 2010 Oden Eriksson <oeriksson@mandriva.com> 3.3.0-0.2mdv2010.1
+ Revision: 496743
- added some error checking in sa-update.cron

* Sun Jan 24 2010 Oden Eriksson <oeriksson@mandriva.com> 3.3.0-0.1mdv2010.1
+ Revision: 495489
- 3.3.0 (pre-release)
- rediffed one patch
- load the Mail::SpamAssassin::Plugin::AWL to have auto_whitelist* working
- the default rules is packaged separately (spamassassin-rules)
- fix deps
- run sa-update daily per default

* Mon Jan 18 2010 Michael Scherer <misc@mandriva.org> 3.2.5-13mdv2010.1
+ Revision: 493126
- do not send a email each time no new rules were found because we are up to date

* Wed Jan 06 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-12mdv2010.1
+ Revision: 486837
- another install "fix"
- fix borkiness at install
- fix a silly y2k10 rule bug

* Fri Jul 17 2009 Olivier Thauvin <nanardon@mandriva.org> 3.2.5-11mdv2010.0
+ Revision: 396905
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-10mdv2009.1
+ Revision: 326623
- rebuilt due to build system fuckup
- make it backportable

* Sat Dec 27 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-8mdv2009.1
+ Revision: 319972
- fix deps

* Sat Dec 27 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-7mdv2009.1
+ Revision: 319880
- fix #46628 (/etc/cron.daily/sa-update exits uncleanly when sa-update exits with error code 4)
- license the sa-update.cron file
- fix deps

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-6mdv2009.1
+ Revision: 316160
- rebuild

* Thu Sep 11 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-5mdv2009.0
+ Revision: 283817
- fix #41887 (Spamassassin incomplet dependency)

* Fri Sep 05 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-4mdv2009.0
+ Revision: 281088
- reduce deps for evolution by breaking out sa-compile into a subpackage

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-3mdv2009.0
+ Revision: 235812
- perl-devel is needed by sa-compile (ghibo)

* Tue Jul 08 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-2mdv2009.0
+ Revision: 232760
- fix deps with a twist and #41887
- hardcode %%{_localstatedir}

* Thu Jun 12 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.5-1mdv2009.0
+ Revision: 218547
- 3.2.5

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Tue Apr 08 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.4-3mdv2009.0
+ Revision: 192345
- fix #39874 (spamassassin-spamd does not create /var/log/spamassassin)

* Wed Feb 06 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.4-3mdv2008.1
+ Revision: 163124
- fix deps (perl-Apache-Test)
- make spamd use its own logfile (/var/log/spamassassin/spamd.log) to work around a bug in Sys-Syslog-0.22+
- reworked the sa-update cron script, note you should look out for changes in the
  /etc/sysconfig/spamd file to utilize the new sa-update cron script
- fixed the init script (don't start per default)
- added the new apache+mod_perl based spamd sub package (listens on 127.0.0.1:784)

* Mon Jan 21 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.4-2mdv2008.1
+ Revision: 155679
-  drop build deps on perl-INET6 (perl-IO-Socket-INET6) because it and perl-Socket6 are borked
- rebuild

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Add perl-HTML-Parser as Requires on the perl subpackage

* Tue Jan 08 2008 Oden Eriksson <oeriksson@mandriva.com> 3.2.4-1mdv2008.1
+ Revision: 146396
- 3.2.4

* Wed Dec 19 2007 Oden Eriksson <oeriksson@mandriva.com> 4mdv2008.1-current
+ Revision: 134133
- re-add %%buildroot

* Wed Dec 19 2007 Oden Eriksson <oeriksson@mandriva.com> 3.2.3-3mdv2008.1
+ Revision: 133031
- fix #36225 (sa-compile needs re2c)

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix summary

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 3.2.3-2mdv2008.0
+ Revision: 82396
- fix #33304 (spamd missing perl subjection (perl-version))

* Fri Aug 10 2007 Oden Eriksson <oeriksson@mandriva.com> 3.2.3-1mdv2008.0
+ Revision: 61097
- 3.2.3

* Wed Jul 25 2007 Oden Eriksson <oeriksson@mandriva.com> 3.2.2-1mdv2008.0
+ Revision: 55397
- 3.2.2
- fix the correct attributes (700) on the /etc/mail/spamassassin/sa-update-keys directory
- fix deps (perl-Mail-SPF)
- fix deps

* Wed Jun 13 2007 Oden Eriksson <oeriksson@mandriva.com> 3.2.1-1mdv2008.0
+ Revision: 38545
- 3.2.1 (fixes CVE-2007-2873)

* Wed May 02 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 3.2.0-1mdv2008.0
+ Revision: 20772
- Updated to 3.2.0.
- Redid patch fixbang.
- Removed already applied patch sa-learn.


* Wed Apr 04 2007 Oden Eriksson <oeriksson@mandriva.com> 3.1.8-3mdv2007.1
+ Revision: 150579
- added P2 from fedora to fix a regression in sa-learn

* Thu Mar 15 2007 Oden Eriksson <oeriksson@mandriva.com> 3.1.8-2mdv2007.1
+ Revision: 144353
- added pinit LSB stuff to the spamd initscript

* Thu Feb 22 2007 Oden Eriksson <oeriksson@mandriva.com> 3.1.8-1mdv2007.1
+ Revision: 124716
- 3.1.8 (fixes CVE-2007-0451)
- try and enable the test suite

* Tue Jan 23 2007 Oden Eriksson <oeriksson@mandriva.com> 3.1.7-6mdv2007.1
+ Revision: 112640
- correct the auto_whitelist_path path if needed

* Thu Dec 21 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.7-5mdv2007.1
+ Revision: 101076
- fix safer chmod in post for the spamd sub package

* Wed Dec 20 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.7-4mdv2007.1
+ Revision: 100502
- fix build deps (perl-libwww-perl)
- added a cron script to optionally use sa-update daily, set USE_SA_UPDATE=1 in
  the /etc/sysconfig/spamd to activate it

* Fri Dec 08 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.7-3mdv2007.1
+ Revision: 93601
- add directories and deps for sa-update
- bzip2 cleanup

* Thu Oct 12 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.7-2mdv2007.1
+ Revision: 63403
- fix the build (duh!)
- 3.1.7 (Major bugfixes)
- 3.1.6
- bunzip sources
- 3.1.6
- revert the last auto-whitelist change and do some magic in %%post (#25730)
- fix deps (#26350)
- don't run the tests for now (#16535)
- Import spamassassin

* Sat Sep 16 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.5-2mdv2007.0
- fix #25730
- don't use the mafioso spamcop plugin per default (P1)

* Fri Sep 01 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.5-1mdv2007.0
- 3.1.5 (Minor bugfixes)

* Sat Jul 29 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.4-2mdv2007.0
- fix deps so tests passes on x86_64

* Sat Jul 29 2006 Emmanuel Andry <eandry@mandriva.org> 3.1.4-1mdv2007.0
- 3.1.4

* Wed Jun 07 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.3-1mdv2007.0
- 3.1.3 (Major security fixes)

* Sat May 27 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.2-1mdk
- 3.1.2 (Minor bugfixes)

* Sun Mar 12 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.1-1mdk
- 3.1.1 (Major bugfixes)

* Sat Feb 11 2006 Michael Scherer <misc@mandriva.org> 3.1.0-7mdk
- fix check when LANG is not english
- use check

* Tue Feb 07 2006 Frederic Crozat <fcrozat@mandriva.com> 3.1.0-6mdk
- Don't ship auto-whitelist.db anymore (Mdk bug #20823)

* Wed Jan 18 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-5mdk
- fix path to perl in order to attempt to make the test suite work in a chroot

* Tue Jan 10 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-4mdk
- rebuilt due to package loss

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-3mdk
- rebuilt against openssl-0.9.8a

* Tue Oct 18 2005 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-2mdk
- fix deps
- fix one error in the provided local.cf file

* Fri Sep 16 2005 Oden Eriksson <oeriksson@mandriva.com> 3.1.0-1mdk
- 3.1.0
- rediff P1 (now P0)
- drop upstream implemented patches (P2,P3,P4)
- fix deps

* Fri Sep 02 2005 Frederic Crozat <fcrozat@mandriva.com> 3.0.4-3mdk
- Patch4 (CVS): fix utf8 warning (Mdk bug #17456)

* Wed Jun 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.4-2mdk
- added P3 to allow longer lines for non-english locales, 
  reported by Vincent Panel

* Wed Jun 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.4-1mdk
- 3.0.4
- new download url
- sync with the provided init script
- use the %%mkrel macro

* Sun May 01 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.3-1mdk
- 3.0.3
- spec file cleansing
- run the test suite

* Mon Jan 10 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.2-2mdk
- added P1 (prefork stuff as in apache)

* Fri Dec 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.2-1mdk
- 3.0.2

* Sun Nov 28 2004 Guillaume Rousse <guillomovitch@mandrake.org> 3.0.1-2mdk 
- add optional perl-Mail-SPF-Query in description

* Wed Oct 27 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.1-1mdk
- 3.0.1

* Fri Sep 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.0-1mdk
- 3.0.0

* Thu Sep 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.0-0.rc5.1mdk
- 3.0.0-rc5

* Sun Sep 12 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.0-0.rc4.1mdk
- 3.0.0-rc4
- fix the default local.cf file

* Tue Sep 07 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.0-0.rc3.1mdk
- 3.0.0-rc3

* Wed Sep 01 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.0-0.rc2.1mdk
- 3.0.0-rc2

* Sat Aug 21 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 3.0.0-0.rc1.1mdk
-

* Sat Aug 07 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 3.0.0-0.pre4.3mdk
- Release 3.0.0 pre4

* Tue Aug 03 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 3.0.0-0.pre3.3mdk
- Fix buildrequires (found by Christiaan Welvaart)

* Sat Jul 31 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 3.0.0-0.pre3.2mdk
- Fix default permission on local.cf file (found by AAW)

* Tue Jul 27 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 3.0.0-0.pre3.1mdk
- Release 3.0.0 pre3 
- Regenerate patch 1
- Remove patch2 (merged upstream)
- add install script fix from Fedora 
- add procmail sample rules for spamassassin & spamc (Fedora)
- Update source2 to remove deprecated flags
- Build spamc with SSL by default

* Sun Jun 27 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.63-5mdk
- Patch2 (Habeas) : switch from Habeas header + blacklist to
  Habeas header + whitelist, spammers can no longer use the Habeas
  header to bypass SA

* Thu May 20 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.63-4mdk
- fix default location of DCC socket

* Tue Apr 20 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.63-3mdk
- broke out spamd and spamc as PLD does it (thanks PLD!)
- added S1 and S2 (removed the initscript patch)
- provide the ssl aware spamc client (%%{_bindir}/spamc-ssl)

