# TODO:
# - build with system mozldap
#
# Conditional builds
%bcond_with	gtk3		# GTK+ 3.x instead of 2.x
%bcond_without	ldap		# disable e-mail address lookups in LDAP directories
%bcond_without	lightning	# disable Sunbird/Lightning calendar
%bcond_with	xulrunner	# system xulrunner
%bcond_with	crashreporter	# report crashes to crash-stats.mozilla.com
# - disabled shared_js - https://bugzilla.mozilla.org/show_bug.cgi?id=1039964
%bcond_with	shared_js	# shared libmozjs library [broken]

%if 0%{?_enable_debug_packages} != 1
%undefine	crashreporter
%endif

%define		nspr_ver	4.10.6
%define		nss_ver		3.19.2.1

%define		xulrunner_ver	2:31.3.0

%if %{without xulrunner}
# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)
%endif

Summary:	Icedove - email client
Summary(pl.UTF-8):	Icedove - klient poczty
Name:		icedove
Version:	38.4.0
Release:	1
License:	MPL v2.0
Group:		X11/Applications/Mail
Source0:	http://releases.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}.source.tar.bz2
# Source0-md5:	483373b1485cf2edea77c75a69602870
Source2:	%{name}-branding.tar.xz
# Source2-md5:	66753bc5c924d7492b6b5c9bdc3e4b5b
Source4:	%{name}.desktop
Source5:	%{name}.sh
Patch0:		%{name}-branding.patch
Patch1:		%{name}-fonts.patch
Patch2:		%{name}-prefs.patch
Patch3:		system-mozldap.patch
Patch4:		%{name}-makefile.patch
Patch5:		%{name}-extensiondir.patch
Patch6:		no-subshell.patch
# Edit patch below and restore --system-site-packages when system virtualenv gets 1.7 upgrade
Patch7:		system-virtualenv.patch
Patch8:		enable-addons.patch
Patch9:		bump-nss-req.patch
Patch11:	freetype-2.6.patch
URL:		http://www.pld-linux.org/Packages/Icedove
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.10
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	glib2-devel >= 1:2.20
BuildRequires:	gstreamer0.10-devel
BuildRequires:	gstreamer0.10-plugins-base-devel
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.14}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	hunspell-devel
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libevent-devel
BuildRequires:	libicu-devel >= 50.1
BuildRequires:	libiw-devel
# requires libjpeg-turbo implementing at least libjpeg 6b API
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libpng-devel >= 1.4.1
BuildRequires:	libstdc++-devel
BuildRequires:	mozldap-devel
BuildRequires:	nspr-devel >= 1:%{nspr_ver}
BuildRequires:	nss-devel >= 1:%{nss_ver}
BuildRequires:	pango-devel >= 1:1.22.0
BuildRequires:	perl-base >= 1:5.6
BuildRequires:	python-virtualenv
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.5
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.8.4.2
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	libvpx-devel >= 1.3.0
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	yasm
BuildRequires:	zip
%if %{with xulrunner}
BuildRequires:	xulrunner-devel >= %{xulrunner_ver}
BuildRequires:	xulrunner-devel < 2:32
%else
Requires:	glib2 >= 1:2.20
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.14}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Requires:	libvpx >= 1.3.0
Requires:	myspell-common
Requires:	nspr >= 1:%{nspr_ver}
Requires:	nss >= 1:%{nss_ver}
Requires:	pango >= 1:1.22.0
Requires:	sqlite3 >= %{sqlite_build_version}
%endif
Requires(post):	mktemp >= 1.5-18
%if %{with xulrunner}
%requires_eq_to	xulrunner xulrunner-devel
%endif
Requires:	libjpeg-turbo
Obsoletes:	mozilla-thunderbird
Obsoletes:	mozilla-thunderbird-dictionary-en-US
Conflicts:	icedove-lang-resources < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_cpp		-D_FORTIFY_SOURCE=[0-9]+

# iceweasel/icedove/iceape provide their own versions
%define		_noautoprovfiles	%{_libdir}/%{name}/components
%if %{without xulrunner}
# we don't want these to satisfy packages depending on xulrunner
%define		_noautoprov		libmozalloc.so libmozjs.so libxul.so
# and as we don't provide them, don't require either
%define		_noautoreq		libmozalloc.so libmozjs.so libxul.so
%endif

%define		topdir		%{_builddir}/%{name}-%{version}
%define		objdir		%{topdir}/obj-%{_target_cpu}

%description
Icedove is an open-source, fast and portable email client.

%description -l pl.UTF-8
Icedove jest mającym otwarte źródła, szybkim i przenośnym klientem
poczty.

%package addon-lightning
Summary:	An integrated calendar for Icedove
Summary(pl.UTF-8):	Zintegrowany kalendarz dla Icedove
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description addon-lightning
Lightning is an calendar extension to Icedove email client.

%description addon-lightning -l pl.UTF-8
Lightning to rozszerzenie do klienta poczty Icedove dodające
funkcjonalność kalendarza.

%prep
%setup -qc
%{__mv} comm-esr38 mozilla
%setup -q -T -D -a2
cd mozilla
%patch0 -p1
#%patch1 -p1
%patch2 -p1
%patch3 -p1
#%patch4 -p2
%patch5 -p2
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p2
%patch11 -p1

%build
cd mozilla
cp -f %{_datadir}/automake/config.* mozilla/build/autoconf
cp -f %{_datadir}/automake/config.* mozilla/nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* ldap/sdks/c-sdk/config/autoconf

cat << EOF > .mozconfig
mk_add_options MOZ_OBJDIR=%{objdir}

export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcflags}"

%if %{with crashreporter}
export MOZ_DEBUG_SYMBOLS=1
%endif

# Options for 'configure' (same as command-line options).
ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
%if %{?debug:1}0
ac_add_options --disable-optimize
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --enable-debugger-info-modules
ac_add_options --enable-crash-on-assert
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
ac_add_options --disable-logging
ac_add_options --enable-optimize="%{rpmcflags} -Os"
%endif
ac_add_options --disable-strip
ac_add_options --disable-strip-libs
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%if %{with lightning}
ac_add_options --enable-calendar
%else
ac_add_options --disable-calendar
%endif
%if %{with crashreporter}
ac_add_options --enable-crashreporter
%else
ac_add_options --disable-crashreporter
%endif
ac_add_options --disable-elf-dynstr-gc
ac_add_options --disable-gnomeui
ac_add_options --disable-gnomevfs
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-profilesharing
ac_add_options --disable-updater
ac_add_options --disable-xterm-updates
ac_add_options --enable-application=mail
ac_add_options --enable-crypto
ac_add_options --enable-default-toolkit=%{?with_gtk3:cairo-gtk3}%{!?with_gtk3:cairo-gtk2}
ac_add_options --enable-gio
%if %{with ldap}
ac_add_options --enable-ldap
ac_add_options --with-system-ldap
%else
ac_add_options --disable-ldap
%endif
ac_add_options --enable-libxul
ac_add_options --enable-pango
ac_add_options --enable-postscript
%{?with_shared_js:ac_add_options --enable-shared-js}
ac_add_options --enable-single-profile
ac_add_options --enable-startup-notification
ac_add_options --enable-system-cairo
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --with-branding=icedove/branding
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
ac_add_options --with-distribution-id=org.pld-linux
%if %{with xulrunner}
ac_add_options --with-libxul-sdk=$(pkg-config --variable=sdkdir libxul)
ac_add_options --with-system-libxul
%endif
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-ffi
ac_add_options --with-system-icu
ac_add_options --with-system-jpeg
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
EOF

mkdir -p %{objdir}/config
ln -s %{topdir}/mozilla/config/*.mk %{objdir}/config

%{__make} -j1 -f client.mk build \
	STRIP="/bin/true" \
	MOZ_MAKE_FLAGS="%{?_smp_mflags}" \
	installdir=%{_libdir}/%{name} \
	XLIBS="-lX11 -lXt" \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%if %{with crashreporter}
# create debuginfo for crash-stats.mozilla.com
%{__make} -j1 -C obj-%{_target_cpu} buildsymbols
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{_datadir}/%{name},%{_pixmapsdir},%{_desktopdir}}

cd %{objdir}
%{__make} -C mail/installer stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	installdir=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

%{__make} -C icedove/branding install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a dist/icedove/* $RPM_BUILD_ROOT%{_libdir}/%{name}/
 
%if %{with xulrunner}
# needed to find mozilla runtime
ln -s ../xulrunner $RPM_BUILD_ROOT%{_libdir}/%{name}/xulrunner
%endif
 
# Enable crash reporter for Thunderbird application
%if %{with crashreporter}
%{__sed} -i -e 's/\[Crash Reporter\]/[Crash Reporter]\nEnabled=1/' $RPM_BUILD_ROOT%{_libdir}/%{name}/application.ini

# Add debuginfo for crash-stats.mozilla.com
install -d $RPM_BUILD_ROOT%{_exec_prefix}/lib/debug%{_libdir}/%{name}
cp -a dist/%{name}-%{version}.en-US.linux-*.crashreporter-symbols.zip $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}/%{name}
%endif

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins $RPM_BUILD_ROOT%{_datadir}/%{name}/searchplugins
ln -s ../../share/%{name}/searchplugins $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins

# dir for arch independant extensions besides arch dependant extensions
# see mozilla/xpcom/build/nsXULAppAPI.h
# XRE_SYS_LOCAL_EXTENSION_PARENT_DIR and XRE_SYS_SHARE_EXTENSION_PARENT_DIR
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions

%if %{without xulrunner}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
%endif

%{__sed} -e "s|%MOZAPPDIR%|%{_libdir}/%{name}|" \
	 -e "s|%MOZ_APP_DISPLAYNAME%|Icedove|" \
	%{topdir}/mozilla/mozilla/build/unix/mozilla.in > $RPM_BUILD_ROOT%{_libdir}/%{name}/icedove

%{__sed} -e 's,@LIBDIR@,%{_libdir},' %{SOURCE5} > $RPM_BUILD_ROOT%{_bindir}/icedove
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/thunderbird
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird

# install icons and desktop file
cp -p %{topdir}/mozilla/icedove/branding/content/icon64.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
for i in 16 32 48 64 128 256; do
	install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps
	cp -a %{topdir}/mozilla/icedove/branding/icedove${i}.png \
		$RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps/icedove.png
done
install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/apps
cp -a %{topdir}/mozilla/icedove/branding/icedove.svg $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/apps/icedove.svg

cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# files created by regxpcom -register in post
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/xpti.dat
cat << 'EOF' > $RPM_BUILD_ROOT%{_libdir}/%{name}/register
#!/bin/sh
umask 022
# make temporary HOME, as it attempts to touch files in $HOME/.mozilla
# dangerous if you run this with sudo with keep_env += HOME
# also TMPDIR could be pointing to sudo user's homedir so we reset that too.
t=$(mktemp -d)
%{__rm} -f %{_libdir}/%{name}/components/{compreg,xpti}.dat
TMPDIR= TMP= HOME=$t %{_libdir}/%{name}/icedove -register
rm -rf $t
EOF
chmod a+rx $RPM_BUILD_ROOT%{_libdir}/%{name}/register

# mozldap
%{__sed} -i '/lib\(ldap\|ldif\|prldap\)60.so/d' $RPM_BUILD_ROOT%{_libdir}/%{name}/dependentlibs.list
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{ldap,ldif,prldap}60.so

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
if [ -d %{_libdir}/%{name}/dictionaries ] && [ ! -L %{_libdir}/%{name}/dictionaries ]; then
	mv -v %{_libdir}/%{name}/dictionaries{,.rpmsave}
fi
for d in chrome defaults icons isp modules res searchplugins; do
	if [ -d %{_libdir}/%{name}/$d ] && [ ! -L %{_libdir}/%{name}/$d ]; then
		install -d %{_datadir}/%{name}
		mv %{_libdir}/%{name}/$d %{_datadir}/%{name}/$d
	fi
done
exit 0

%post
%{_libdir}/%{name}/register || :

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/icedove
%attr(755,root,root) %{_bindir}/mozilla-thunderbird
%attr(755,root,root) %{_bindir}/thunderbird
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/blocklist.xml
%{_libdir}/%{name}/chrome.manifest
%dir %{_libdir}/%{name}/components
%{_libdir}/%{name}/components/components.manifest
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/*-bin
%attr(755,root,root) %{_libdir}/%{name}/icedove
%attr(755,root,root) %{_libdir}/%{name}/register
%{_libdir}/%{name}/omni.ja
%if %{without xulrunner}
%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/platform.ini
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%attr(755,root,root) %{_libdir}/%{name}/libmozalloc.so
%{?with_shared_js:%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so}
%attr(755,root,root) %{_libdir}/%{name}/libxul.so
%attr(755,root,root) %{_libdir}/%{name}/plugin-container
%endif

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/isp
%{_libdir}/%{name}/searchplugins
%if %{with xulrunner}
%{_libdir}/%{name}/xulrunner
%else
%{_libdir}/%{name}/dictionaries
%endif

%{_pixmapsdir}/icedove.png
%{_desktopdir}/icedove.desktop

%dir %{_datadir}/%{name}
%dir %{_libdir}/%{name}/distribution
%dir %{_libdir}/%{name}/distribution/extensions
%{_datadir}/%{name}/extensions
%{_datadir}/%{name}/searchplugins

%if %{with crashreporter}
%attr(755,root,root) %{_libdir}/%{name}/crashreporter
%{_libdir}/%{name}/crashreporter.ini
%{_libdir}/%{name}/Throbber-small.gif
%endif

%dir %{_libdir}/%{name}/extensions
%{_libdir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

# files created by regxpcom -register
%ghost %{_libdir}/%{name}/components/compreg.dat
%ghost %{_libdir}/%{name}/components/xpti.dat

%{_iconsdir}/hicolor/*/apps/icedove.*

%if %{with lightning}
%files addon-lightning
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/app.ini
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/chrome.jar
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/chrome.manifest
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/defaults
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/install.rdf
%dir %{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/components
%attr(755,root,root) %{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/components/*.so
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/components/*.js
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/components/*manifest
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/components/*.xpt
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/modules
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/calendar-js
%dir %{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/timezones
%{_libdir}/%{name}/distribution/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/timezones/zones.json
%endif
