%global logmsg logger -t %{name}/rpm

%global apacheuser apache
%global apachegroup apache
%global apachedir httpd

%global naemonuser naemon
%global naemongroup naemon

# Add some security hardening
%global _hardened_build 1

# Setup some debugging options in case we build with --with debug
%if %{defined _with_debug}
  %global mycflags -O0 -pg -ggdb3
%else
  %global mycflags %{nil}
%endif

Summary: Open Source Host, Service And Network Monitoring Program
Name: naemon
Version: 0.8.0
Release: 1%{?dist}
License: GPLv2
Group: Applications/System
URL: http://www.naemon.org/
Source0: http://labs.consol.de/%{name}/release/v%{version}/src/%{name}-%{version}.tar.gz
BuildRequires: gd-devel > 1.8
BuildRequires: zlib-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: mysql-devel
BuildRequires: gperf
BuildRequires: perl
BuildRequires: perl-Module-Install
BuildRequires: logrotate
BuildRequires: gd
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: help2man
BuildRequires: rsync
BuildRequires: expat-devel
# rhel6 specific requirements
%if 0%{?el6}
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl(Module::Install)
%endif
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
BuildRequires: perl-autodie
BuildRequires: systemd
%endif

Requires(pre): shadow-utils
Requires: %{name}-core            = %{version}-%{release}
Requires: %{name}-tools           = %{version}-%{release}
Requires: %{name}-livestatus      = %{version}-%{release}
Requires: %{name}-thruk           = %{version}-%{release}
Requires: %{name}-thruk-reporting = %{version}-%{release}
# https://fedoraproject.org/wiki/Packaging:DistTag
# http://stackoverflow.com/questions/5135502/rpmbuild-dist-not-defined-on-centos-5-5

%description
Naemon is an application, system and network monitoring application.
It can escalate problems by email, pager or any other medium. It is
also useful for incident or SLA reporting. It is originally a fork
of Nagios, but with extended functionality, stability and performance.

It is written in C and is designed as a background process,
intermittently running checks on various services that you specify.

The actual service checks are performed by separate "plugin" programs
which return the status of the checks to Naemon. The plugins are
compatible with Nagios, and can be found in the monitoring-plugins package.

Naemon ships the Thruk gui with extended reporting and dashboard features.


%package core
Summary:   Naemon Monitoring Core
Group:     Applications/System
Requires:  logrotate


%description core
contains the %{name} core


%package tools
Summary:   Naemon Monitoring Tools
Group:     Applications/System

%description tools
contains tools for %{name}.
 - naemonstats:  display statistics
 - oconfsplit:   divide configurations by groups
 - shadownaemon: shadow a remote naemon core over livestatus


%package livestatus
Summary:        Naemon Livestatus Eventbroker Module
Group:          Applications/System
Requires:       %{name}-core = %{version}-%{release}
Requires(post): %{name}-core = %{version}-%{release}

%description livestatus
contains the %{name} livestatus eventbroker module


%package thruk
Summary:     Thruk Gui For Naemon
Group:       Applications/System
Requires:    %{name}-thruk-libs = %{version}-%{release}
Requires(preun): %{name}-thruk-libs = %{version}-%{release}
Requires(post): %{name}-thruk-libs = %{version}-%{release}
Requires:    perl logrotate gd wget
Requires:    httpd mod_fcgid
%global __provides_exclude_from %{_datadir}/%{name}/plugins|%{_datadir}/%{name}/lib
%global __requires_exclude_from %{_datadir}/%{name}/plugins|%{_datadir}/%{name}/lib

%description thruk
This package contains the thruk gui for %{name}


%package thruk-libs
Summary:     Perl Librarys For Naemons Thruk Gui
Group:       Applications/System
Requires:    %{name}-thruk = %{version}-%{release}
Requires:    perl(parent), perl(JSON::XS), perl(Config::General), perl(Config::Any), perl(Class::Data::Inheritable), perl(MRO::Compat)
Requires:    perl(LWP::UserAgent), perl(Net::HTTP), perl(Class::C3::Adopt::NEXT), perl(Class::C3::XS), perl(URI::Escape), perl(Moose)
Requires:    perl(Socket), perl(GD), perl(Template), perl(Template::Plugin::Date), perl(Date::Calc)
Requires:    perl(Data::Page), perl(File::Slurp), perl(Date::Manip), perl(Class::Accessor::Fast), perl(Catalyst)
Requires:    perl(Catalyst::Runtime), perl(Catalyst::Utils), perl(Catalyst::Controller), perl(Catalyst::Exception), perl(Catalyst::ScriptRunner)
Requires:    perl(Catalyst::Authentication::User::Hash), perl(Catalyst::View), perl(Catalyst::View::TT), perl(Catalyst::View::JSON)
Requires:    perl(Catalyst::Plugin::ConfigLoader), perl(Catalyst::Plugin::Static::Simple)
Requires:    perl(Catalyst::Plugin::Authorization::Roles)
Requires:    perl(Log::Log4perl), perl(Log::Dispatch::File), perl(namespace::autoclean), perl(Plack::Handler::CGI)
Requires:    perl(Storable), perl(threads), perl(Thread::Queue), perl(Thread::Semaphore), perl(List::Compare), perl(List::MoreUtils)
Requires:    perl(MIME::Lite), perl(Class::Inspector), perl(LWP::Protocol::https), perl(DBI), perl(DBD::mysql)
#Requires:    perl(LWP::Protocol::connect), perl(Catalyst::Plugin::Compress), perl(Excel::Template::Plus), perl(Date::Calc::XS), perl(Catalyst::View::Excel::Template::Plus), perl(Catalyst::Plugin::CustomErrorMessage), perl(Catalyst::View::GD), perl(Catalyst::Plugin::Redirect)
BuildRequires: perl(Config::Any), perl(Date::Calc), perl(File::Slurp)
%{?perl_default_filter}
%global __provides_exclude_from %{_datadir}/%{name}/plugins|%{_datadir}/%{name}/lib
%global __requires_exclude_from %{_datadir}/%{name}/plugins|%{_datadir}/%{name}/lib|%{_bindir}/thruk|%{_datadir}/%{name}/thruk_auth|%{_datadir}/%{name}/script/thruk_fastcgi.pl

%description thruk-libs
This package contains the library files for the thruk gui


%package thruk-reporting
Summary:     Thruk Gui For Naemon Reporting Addon
Group:       Applications/System
Requires:    %{name}-thruk = %{version}-%{release}
Requires:    xorg-x11-server-Xvfb libXext dejavu-fonts-common

%description thruk-reporting
This package contains the reporting addon for naemons thruk gui useful for sla
and event reporting.


%package devel
Summary: Development Files For Naemon
Group: Development/Libraries

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you are a NEB-module author or wish to
write addons for Naemon using Naemons own APIs, you should install
this package.


%prep
%setup -q

%build
# Cleanup the environment, will cause autoreconf to get run
rm -f %{name}-core/configure
rm -f %{name}-livestatus/configure

CFLAGS="%{mycflags} -Wformat" LDFLAGS="$CFLAGS" %configure \
    --datadir="%{_datadir}/%{name}" \
    --libdir="%{_libdir}/%{name}" \
    --localstatedir="%{_localstatedir}/lib/%{name}" \
    --sysconfdir="%{_sysconfdir}/%{name}" \
    --enable-event-broker \
    --with-pluginsdir="%{_libdir}/%{name}/plugins" \
    --with-tempdir="%{_localstatedir}/cache/%{name}" \
    --with-checkresultdir="%{_localstatedir}/cache/%{name}/checkresults" \
    --with-logdir="%{_localstatedir}/log/%{name}" \
    --with-initdir="%{_initrddir}" \
    --with-logrotatedir="%{_sysconfdir}/logrotate.d" \
    --with-naemon-user="%{naemonuser}" \
    --with-naemon-group="%{naemongroup}" \
    --with-lockfile="%{_localstatedir}/run/%{name}/%{name}.pid" \
    --with-thruk-user="%{apacheuser}" \
    --with-thruk-group="%{naemongroup}" \
    --with-thruk-libs="%{_libdir}/%{name}/perl5" \
    --with-thruk-tempdir="%{_localstatedir}/cache/%{name}/thruk" \
    --with-thruk-vardir="%{_localstatedir}/lib/%{name}/thruk" \
    --with-httpd-conf="%{_sysconfdir}/%{apachedir}/conf.d" \
    --with-htmlurl="/%{name}"

make %{?_smp_mflags} all

%install
make install \
    DESTDIR="%{buildroot}" \
    INSTALL_OPTS="" \
    COMMAND_OPTS="" \
    INIT_OPTS=""

mv %{buildroot}%{_sysconfdir}/logrotate.d/thruk %{buildroot}%{_sysconfdir}/logrotate.d/%{name}-thruk
mv %{buildroot}%{_sysconfdir}/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}-core

# Put the new RC sysconfig in place
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig/
install -m 0644 -p %{name}-core/sample-config/%{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}

mkdir -p -m 0755 %{buildroot}%{_libdir}/%{name}/
ln -s %{_libdir}/nagios/plugins %{buildroot}%{_libdir}/%{name}/plugins

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
# Install systemd entry
install -D -m 0644 -p %{name}-core/daemon-systemd %{buildroot}%{_unitdir}/%{name}.service
install -D -m 0644 -p %{name}-core/%{name}.tmpfiles.conf %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d -m 0755 %{buildroot}/%{_localstatedir}/run/%{name}/
# Move SystemV init-script
mv -f %{buildroot}%{_initrddir}/%{name} %{buildroot}%{_bindir}/%{name}-ctl
%endif

%pre core
getent group %{naemongroup} >/dev/null || groupadd -r %{naemongroup}
getent passwd %{naemonuser} >/dev/null || \
    useradd -r -g %{naemongroup} -d %{_localstatedir}/lib/%{name} \
    -c "%{name} user" %{naemonuser}

%post core
if [ "$1" = "2" ]; then
    %if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
      %systemd_postun
      systemctl condrestart %{name}.service
    %else
      %{_initrddir}/%{name} condrestart &>/dev/null ||
    %endif
elif [ "$1" = "1" ]; then
    %if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
      %systemd_post %{name}.service
    %else
      chkconfig --add %{name}
    %endif
  ;;
fi

if /usr/bin/id %{apacheuser} &>/dev/null; then
    if ! /usr/bin/id -Gn %{apacheuser} 2>/dev/null | grep -q %{naemongroup} ; then
        /usr/sbin/usermod -a -G %{naemongroup} %{apacheuser} >/dev/null
    fi
else
    %logmsg "User \"%{apacheuser}\" does not exist and is not added to group \"%{naemongroup}\". Sending commands to naemon from the CGIs is not possible."
fi
touch %{_localstatedir}/log/%{name}/%{name}.log
chmod 0664 %{_localstatedir}/log/%{name}/%{name}.log
chown %{naemonuser}:%{naemongroup} %{_localstatedir}/log/%{name}/%{name}.log

%preun core
if [ "$1" = "0" ]; then
    # Uninstall, go ahead and stop before removing
    %if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
      %systemd_preun %{name}.service
    %else
      service %{name} stop >/dev/null 2>&1 || :
      chkconfig --del %{name} || :
    %endif
    #rm -f /var/lib/naemon/status.dat
    rm -f /var/lib/naemon/naemon.qh
    rm -f /var/lib/naemon/naemon.tmp*
fi

%postun core
if [ "$1" = "0" ]; then
    rm -f %{_localstatedir}/cache/%{name}/%{name}.configtest \
          %{_localstatedir}/lib/%{name}/objects.cache \
          %{_localstatedir}/lib/%{name}/objects.precache \
          %{_localstatedir}/lib/%{name}/retention.dat \
          #%{_localstatedir}/log/%{name}/%{name}.log \
          %{_localstatedir}/log/%{name}/archives \
          %{_localstatedir}/lib/%{name}/%{name}.cmd
    %{insserv_cleanup}
    chkconfig --del %{name} >/dev/null 2>&1 || :
    systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%post livestatus
if [ "$1" = "2" ]; then
    # Upgrading so try and restart if already running
    %if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
      systemctl condrestart %{name}.service
    %else
      %{_initrddir}/%{name} condrestart &>/dev/null || :
    %endif
elif [ "$1" = "1" ]; then
    # New install, enable module
    if [ -e %{_sysconfdir}/%{name}/%{name}.cfg ]; then
      sed -i %{_sysconfdir}/%{name}/%{name}.cfg -e 's~#\(broker_module=/usr/lib[0-9]*/%{name}/livestatus.so.*\)~\1~'
    fi
fi

#%preun livestatus
#if [ "$1" = "0" ]; then
#    rm -f %{_localstatedir}/log/%{name}/livestatus.log
#fi

%postun livestatus
if [ "$1" = "0" ]; then
    # POSTUN
    if [ -e %{_sysconfdir}/%{name}/%{name}.cfg ]; then
      sed -i %{_sysconfdir}/%{name}/%{name}.cfg -e 's~\(broker_module=/usr/lib[0-9]*/%{name}/livestatus.so.*\)~#\1~'
    fi
fi


%pre thruk
getent group %{naemongroup} >/dev/null || groupadd -r %{naemongroup}
getent passwd %{naemonuser} >/dev/null || \
    useradd -r -g %{naemongroup} -d %{_localstatedir}/lib/%{name} \
    -c "%{name} user" %{naemonuser}

# save themes, plugins so we don't reenable them on every update
rm -rf %{_localstatedir}/cache/%{name}/thruk_update
if [ -d %{_sysconfdir}/%{name}/themes/themes-enabled/. ]; then
  mkdir -p %{_localstatedir}/cache/%{name}/thruk_update/themes
  cp -rp %{_sysconfdir}/%{name}/themes/themes-enabled/* %{_localstatedir}/cache/%{name}/thruk_update/themes/ 2>/dev/null
fi
if [ -d %{_sysconfdir}/%{name}/plugins/plugins-enabled/. ]; then
  mkdir -p %{_localstatedir}/cache/%{name}/thruk_update/plugins
  cp -rp %{_sysconfdir}/%{name}/plugins/plugins-enabled/* %{_localstatedir}/cache/%{name}/thruk_update/plugins/ 2>/dev/null
fi

%post thruk
chkconfig --add thruk
mkdir -p %{_localstatedir}/lib/%{name}/thruk %{_localstatedir}/cache/%{name}/thruk %{_sysconfdir}/%{name}/bp %{_localstatedir}/log/%{name} %{_sysconfdir}/%{name}/conf.d
touch %{_localstatedir}/log/%{name}/thruk.log
chown -R %{apacheuser}:%{apachegroup} %{_localstatedir}/cache/%{name}/thruk %{_localstatedir}/log/%{name}/thruk.log %{_sysconfdir}/%{name}/plugins/plugins-enabled %{_sysconfdir}/%{name}/thruk_local.conf %{_sysconfdir}/%{name}/bp %{_localstatedir}/lib/%{name}/thruk
crontab -l -u %{apacheuser} 2>/dev/null | crontab -u %{apacheuser} -

# add webserver user to group naemon
if /usr/bin/id %{apacheuser} &>/dev/null; then
    if ! /usr/bin/id -Gn %{apacheuser} 2>/dev/null | grep -q %{naemongroup} ; then
        /usr/sbin/usermod -a -G %{naemongroup} %{apacheuser} >/dev/null
    fi
else
    %logmsg "User \"%{apacheuser}\" does not exist and is not added to group \"%{naemongroup}\". Sending commands to %{name} from the CGIs is not possible."
fi

service httpd condrestart
if [ "$(getenforce 2>/dev/null)" = "Enforcing" ]; then
  echo "******************************************";
  echo "Thruk will not work when SELinux is enabled";
  echo "SELinux: "$(getenforce);
  echo "******************************************";
fi
if [ -d %{_libdir}/%{name}/perl5 ]; then
  /usr/bin/thruk -a clearcache,installcron --local > /dev/null
fi

#echo "Naemon/Thruk have been configured for http://$(hostname)/naemon/."
#echo "The default user is 'admin' with password 'admin'. You can usually change that by 'htpasswd /etc/naemon/htpasswd admin'. And you really should change that!"

%posttrans thruk
# restore themes and plugins
if [ -d %{_localstatedir}/cache/%{name}/thruk_update/themes/. ]; then
  rm -f %{_sysconfdir}/%{name}/themes/themes-enabled/*
  cp -rp %{_localstatedir}/cache/%{name}/thruk_update/themes/* %{_sysconfdir}/%{name}/themes/themes-enabled/ 2>/dev/null  # might fail if no themes are enabled
fi
if [ -d %{_localstatedir}/cache/%{name}/thruk_update/plugins/. ]; then
  rm -f %{_sysconfdir}/%{name}/plugins/plugins-enabled/*
  cp -rp %{_localstatedir}/cache/%{name}/thruk_update/plugins/* %{_sysconfdir}/%{name}/plugins/plugins-enabled/ 2>/dev/null  # might fail if no plugins are enabled
fi
#echo "thruk plugins enabled:" $(ls %{_sysconfdir}/%{name}/plugins/plugins-enabled/)
rm -rf %{_localstatedir}/cache/%{name}/thruk_update

%preun thruk
if [ "$1" = "0" ]; then
  # last version will be deinstalled
  if [ -d %{_libdir}/%{name}/perl5 ]; then
    /usr/bin/thruk -a uninstallcron --local
  fi
fi

%{_initrddir}/thruk stop
chkconfig --del thruk >/dev/null 2>&1
rmdir %{_sysconfdir}/%{name}/bp 2>/dev/null
rmdir %{_sysconfdir}/%{name} 2>/dev/null

%postun thruk
if [ "$1" = "0" ]; then
    rm -rf %{_localstatedir}/cache/%{name}/thruk \
           %{_datadir}/%{name}/root/thruk/plugins \
           %{_localstatedir}/lib/%{name}/thruk
    # try to clean some empty folders
    rmdir %{_sysconfdir}/%{name}/plugins/plugins-available 2>/dev/null
    rmdir %{_sysconfdir}/%{name}/plugins/plugins-enabled 2>/dev/null
    rmdir %{_sysconfdir}/%{name}/plugins 2>/dev/null
    rmdir %{_sysconfdir}/%{name} 2>/dev/null
    %{insserv_cleanup}
    ;;
elif [ "$1" = "1" ]; then
    rm -rf %{_localstatedir}/cache/%{name}/thruk/*
    mkdir -p %{_localstatedir}/cache/%{name}/thruk/reports
    chown -R %{apacheuser}:%{apachegroup} %{_localstatedir}/cache/%{name}/thruk
fi


%preun thruk-libs
if [ "$1" = "0" ]; then
  # last version will be deinstalled
  if [ -e /usr/bin/thruk ]; then
    /usr/bin/thruk -a uninstallcron --local
  fi
fi


%post thruk-libs
if [ -e /usr/bin/thruk ]; then
  /usr/bin/thruk -a clearcache,installcron --local > /dev/null
fi

%post thruk-reporting
rm -f %{_sysconfdir}/%{name}/plugins/plugins-enabled/reports2
ln -s ../plugins-available/reports2 %{_sysconfdir}/%{name}/plugins/plugins-enabled/reports2
%{_initrddir}/thruk condrestart &>/dev/null || :

%preun thruk-reporting
rm -f %{_sysconfdir}/%{name}/plugins/plugins-enabled/reports2
%{_initrddir}/thruk condrestart &>/dev/null || :

%postun thruk-reporting
if [ "$1" = "0" ]; then
    # try to clean some empty folders
    rmdir %{_sysconfdir}/%{name}/plugins/plugins-available 2>/dev/null
    rmdir %{_sysconfdir}/%{name}/plugins/plugins-enabled 2>/dev/null
    rmdir %{_sysconfdir}/%{name}/plugins 2>/dev/null
    rmdir %{_sysconfdir}/%{name} 2>/dev/null
fi



%files

%files core
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0755,root,root) %{_bindir}/naemonstats
%attr(0755,root,root) %{_bindir}/oconfsplit
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
  %attr(0644,root,root) %{_unitdir}/%{name}.service
  %attr(0644,root,root) %{_tmpfilesdir}/%{name}.conf
  %attr(0755,root,root) %{_bindir}/%{name}-ctl
  %attr(0755,%{naemonuser},%{naemongroup}) %dir %{_localstatedir}/run/%{name}
%else
  %attr(0755,root,root) %{_initrddir}/%{name}
%endif
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-core
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}/
%attr(2775,%{naemonuser},%{naemongroup}) %dir %{_sysconfdir}/%{name}/conf.d
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.cfg
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/resource.cfg
%attr(0664,%{naemonuser},%{naemongroup}) %config(noreplace) %{_sysconfdir}/%{name}/conf.d/*.cfg
%attr(0664,%{naemonuser},%{naemongroup}) %config(noreplace) %{_sysconfdir}/%{name}/conf.d/templates/*.cfg
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(2775,%{naemonuser},%{apachegroup}) %dir %{_localstatedir}/cache/%{name}/checkresults
%attr(2775,%{naemonuser},%{naemongroup}) %dir %{_localstatedir}/cache/%{name}
%attr(0755,%{naemonuser},%{naemongroup}) %dir %{_localstatedir}/lib/%{name}
%attr(0755,%{naemonuser},%{naemongroup}) %dir %{_localstatedir}/log/%{name}
%attr(0755,%{naemonuser},%{naemongroup}) %dir %{_localstatedir}/log/%{name}/archives
%attr(-,root,root) %{_libdir}/%{name}/libnaemon.so*
%attr(-,root,root) %{_libdir}/%{name}/plugins
%{_mandir}/man8/%{name}.8*

%files tools
%attr(0755,root,root) %{_bindir}/naemonstats
%attr(0755,root,root) %{_bindir}/oconfsplit
%attr(0755,root,root) %{_bindir}/shadownaemon
%{_mandir}/man8/naemonstats.8*
%{_mandir}/man8/oconfsplit.8*
%{_mandir}/man8/shadownaemon.8*

%files devel
%attr(-,root,root) %{_includedir}/%{name}/
%attr(-,root,root) %{_libdir}/%{name}/libnaemon.a
%attr(-,root,root) %{_libdir}/%{name}/libnaemon.la

%files livestatus
%attr(0755,root,root) %{_bindir}/%{name}-unixcat
%attr(0644,root,root) %{_libdir}/%{name}/%{name}-livestatus/livestatus.so
%attr(0755,%{naemonuser},%{naemongroup}) %dir %{_localstatedir}/log/%{name}

%files thruk
%attr(0755,root, root) %{_bindir}/thruk
%attr(0755,root, root) %{_bindir}/naglint
%attr(0755,root, root) %{_bindir}/nagexp
%attr(0755,root, root) %{_initrddir}/thruk
%config %{_sysconfdir}/%{name}/ssi
%config %{_sysconfdir}/%{name}/thruk.conf
%attr(0644,%{apacheuser},%{apachegroup}) %config(noreplace) %{_sysconfdir}/%{name}/thruk_local.conf
%attr(0644,%{apacheuser},%{apachegroup}) %config(noreplace) %{_sysconfdir}/%{name}/cgi.cfg
%attr(0644,%{apacheuser},%{apachegroup}) %config(noreplace) %{_sysconfdir}/%{name}/htpasswd
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{_sysconfdir}/%{name}/bp
%config(noreplace) %{_sysconfdir}/%{name}/naglint.conf
%config(noreplace) %{_sysconfdir}/%{name}/log4perl.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-thruk
%config(noreplace) %{_sysconfdir}/%{apachedir}/conf.d/thruk.conf
%config(noreplace) %{_sysconfdir}/%{apachedir}/conf.d/thruk_cookie_auth_vhost.conf
%config(noreplace) %{_sysconfdir}/%{name}/themes
%config(noreplace) %{_sysconfdir}/%{name}/menu_local.conf
%config(noreplace) %{_sysconfdir}/%{name}/usercontent
%attr(0755,root, root) %{_datadir}/%{name}/thruk_auth
%attr(0755,root, root) %{_datadir}/%{name}/script/thruk_fastcgi.pl
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{_localstatedir}/cache/%{name}/thruk
%{_datadir}/%{name}/root
%{_datadir}/%{name}/templates
%{_datadir}/%{name}/themes
%{_datadir}/%{name}/plugins/plugins-available/business_process
%config %{_sysconfdir}/%{name}/plugins/plugins-enabled/business_process
%config %{_sysconfdir}/%{name}/plugins/plugins-available/business_process
%{_datadir}/%{name}/plugins/plugins-available/conf
%config %{_sysconfdir}/%{name}/plugins/plugins-enabled/conf
%config %{_sysconfdir}/%{name}/plugins/plugins-available/conf
%{_datadir}/%{name}/plugins/plugins-available/dashboard
%config %{_sysconfdir}/%{name}/plugins/plugins-available/dashboard
%{_datadir}/%{name}/plugins/plugins-available/minemap
%config %{_sysconfdir}/%{name}/plugins/plugins-enabled/minemap
%config %{_sysconfdir}/%{name}/plugins/plugins-available/minemap
%{_datadir}/%{name}/plugins/plugins-available/mobile
%config %{_sysconfdir}/%{name}/plugins/plugins-enabled/mobile
%config %{_sysconfdir}/%{name}/plugins/plugins-available/mobile
%{_datadir}/%{name}/plugins/plugins-available/panorama
%config %{_sysconfdir}/%{name}/plugins/plugins-enabled/panorama
%config %{_sysconfdir}/%{name}/plugins/plugins-available/panorama
%{_datadir}/%{name}/plugins/plugins-available/shinken_features
%config %{_sysconfdir}/%{name}/plugins/plugins-available/shinken_features
%{_datadir}/%{name}/plugins/plugins-available/statusmap
%config %{_sysconfdir}/%{name}/plugins/plugins-enabled/statusmap
%config %{_sysconfdir}/%{name}/plugins/plugins-available/statusmap
%{_datadir}/%{name}/plugins/plugins-available/wml
%config %{_sysconfdir}/%{name}/plugins/plugins-available/wml
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/Changes
%{_datadir}/%{name}/LICENSE
%{_datadir}/%{name}/menu.conf
%{_datadir}/%{name}/dist.ini
%{_datadir}/%{name}/thruk_cookie_auth.include
%{_datadir}/%{name}/docs/THRUK_MANUAL.html
%{_datadir}/%{name}/docs/FAQ.html
%{_datadir}/%{name}/%{name}-version
%attr(0755,root,root) %{_datadir}/%{name}/fcgid_env.sh
%{_mandir}/man3/nagexp.3*
%{_mandir}/man3/naglint.3*
%{_mandir}/man3/thruk.3*
%{_mandir}/man8/thruk.8*

%files thruk-libs
#%attr(-,root,root) %{_libdir}/%{name}/perl5

%files thruk-reporting
%{_datadir}/%{name}/plugins/plugins-available/reports2
%{_sysconfdir}/%{name}/plugins/plugins-available/reports2
%{_sysconfdir}/%{name}/plugins/plugins-enabled/reports2

%changelog
* Mon Feb 24 2014 Daniel Wittenberg <dwittenberg2008@gmail.com> 0.8.0-2
- More closely align spec and packaging with Fedora standards

* Sun Feb 23 2014 Daniel Wittenberg <dwittenberg2008@gmail.com> 0.8.0-2
- Add native and full systemctl control on el7

* Thu Feb 06 2014 Daniel Wittenberg <dwittenberg2008@gmail.com> 0.1.0-1
- Add reload for systemctl-based setups

* Thu Feb 06 2014 Sven Nierlein <sven.nierlein@consol.de> 0.1.0-1
- moved thruks reporting addon into seperate package

* Tue Nov 26 2013 Sven Nierlein <sven.nierlein@consol.de> 0.0.1-1
- initial naemon meta package

