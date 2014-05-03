# TODO:
# - separate spec for enigmail
# - build with system mozldap
#
# Conditional builds
%bcond_without	enigmail	# don't build enigmail - GPG/PGP support
%bcond_without	ldap		# disable e-mail address lookups in LDAP directories
%bcond_without	lightning	# disable Sunbird/Lightning calendar
%bcond_with	xulrunner	# system xulrunner
%bcond_with	crashreporter	# report crashes to crash-stats.mozilla.com

%if 0%{?_enable_debug_packages} != 1
%undefine	crashreporter
%endif

%define		enigmail_ver	1.6
%define		nspr_ver	4.9.3
%define		nss_ver		3.15.3.1

%define		xulrunner_ver	2:24.0

%if %{without xulrunner}
# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)
%endif

Summary:	Icedove - email client
Summary(pl.UTF-8):	Icedove - klient poczty
Name:		icedove
Version:	24.5.0
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Mail
Source0:	http://releases.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}.source.tar.bz2
# Source0-md5:	dbe164c48e42c04b4959910eda2e52ca
Source1:	http://www.mozilla-enigmail.org/download/source/enigmail-%{enigmail_ver}.tar.gz
# Source1-md5:	4a2bbcb020bdb282a660fda8c70d5608
Source2:	%{name}-branding.tar.bz2
# Source2-md5:	d8e6897870bf288fdf264c0e9ef85f7d
Source3:	%{name}-rm_nonfree.sh
Source4:	%{name}.desktop
Source5:	%{name}.sh
Patch0:		%{name}-branding.patch
Patch1:		%{name}-enigmail-shared.patch
Patch3:		%{name}-fonts.patch
Patch6:		%{name}-prefs.patch
Patch7:		system-mozldap.patch
Patch8:		%{name}-makefile.patch
Patch10:	%{name}-extensiondir.patch
Patch11:	crashreporter.patch
Patch12:	no-subshell.patch
# Edit patch below and restore --system-site-packages when system virtualenv gets 1.7 upgrade
Patch13:	system-virtualenv.patch
Patch14:	gyp-slashism.patch
Patch15:	enable-addons.patch
URL:		http://www.pld-linux.org/Packages/Icedove
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.10
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gstreamer0.10-devel
BuildRequires:	gstreamer0.10-plugins-base-devel
BuildRequires:	gtk+2-devel >= 2:2.10.0
BuildRequires:	hunspell-devel
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libevent-devel
BuildRequires:	libiw-devel
# requires libjpeg-turbo implementing at least libjpeg 6b API
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libnotify-devel >= 0.4
BuildRequires:	libpng-devel >= 1.4.1
BuildRequires:	libstdc++-devel
BuildRequires:	mozldap-devel
BuildRequires:	nspr-devel >= 1:%{nspr_ver}
BuildRequires:	nss-devel >= 1:%{nss_ver}
BuildRequires:	pango-devel >= 1:1.14.0
BuildRequires:	perl-base >= 1:5.6
BuildRequires:	python-virtualenv
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.5
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.7.4
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	libvpx-devel >= 1.0.0
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	yasm
BuildRequires:	zip
%if %{with xulrunner}
BuildRequires:	xulrunner-devel >= %{xulrunner_ver}
%else
Requires:	myspell-common
Requires:	nspr >= 1:%{nspr_ver}
Requires:	nss >= 1:%{nss_ver}
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
%define		_noautoprov		libmozalloc.so libxpcom.so libxul.so
# and as we don't provide them, don't require either
%define		_noautoreq		libmozalloc.so libxpcom.so libxul.so
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

%package addon-enigmail
Summary:	Extension for the authentication and encryption features provided by GnuPG
Summary(pl.UTF-8):	Rozszerzenie do uwierzytelniania i szyfrowania zapewnianego przez GnuPG
License:	MPL/LGPL
Group:		Applications/Networking
URL:		http://enigmail.mozdev.org/
Requires:	%{name} = %{version}-%{release}
Requires:	gnupg
Obsoletes:	mozilla-thunderbird-addon-enigmail

%description addon-enigmail
Enigmail is an extension to the Icedove mail client which allows users
to access the authentication and encryption features provided by
GnuPG.

Main Features:
- Encrypt/sign mail when sending, decrypt/authenticate received mail
- Support for inline-PGP (RFC 2440) and PGP/MIME (RFC 3156)
- Per-Account based encryption and signing defaults
- Per-Recipient rules for automated key selection, and
  enabling/disabling encryption and signing
- OpenPGP key management interface

%description addon-enigmail -l pl.UTF-8
Enigmail to rozszerzenie klienta pocztowego Icedove pozwalające
użytkownikom na dostęp do uwierzytelniania i szyfrowania zapewnianego
przez GnuPG.

Główne możliwości:
- szyfrowanie/podpisywanie poczty przy wysyłaniu,
  odszyfrowywanie/uwierzytelnianie poczty odebranej
- obsługa inline-PGP (RFC 2440) i PGP/MIME (RFC 3156)
- ustawienia domyślne szyfrowania i podpisywania dla każdego konta
- reguły automatycznego wyboru kluczy i włączenia szyfrowania oraz
  podpisywania dla każdego adresata
- interfejs do zarządzania kluczami OpenPGP

%prep
%setup -qc
mv comm-esr24 mozilla
%setup -q -T -D -a2
cd mozilla
%{?with_enigmail:%{__gzip} -dc %{SOURCE1} | %{__tar} -xf - -C mailnews/extensions}
/bin/sh %{SOURCE3}
%patch0 -p1
%{?with_enigmail:%patch1 -p1}
%patch3 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p2
%patch10 -p2
#patch11 -p2
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

# the entire check in that configure is so wrong, it's simpler to just workaround it here temporarily
%{__sed} -i -e 's|min_nss_version=3.15.3.1|min_nss_version=3.15.3|' mozilla/configure

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
ac_add_options --enable-gio
ac_add_options --disable-gnomeui
ac_add_options --disable-gnomevfs
%if %{with ldap}
ac_add_options --enable-ldap
ac_add_options --with-system-ldap
%else
ac_add_options --disable-ldap
%endif
%if %{with crashreporter}
ac_add_options --enable-crashreporter
%else
ac_add_options --disable-crashreporter
%endif
ac_add_options --disable-xterm-updates
ac_add_options --enable-postscript
%if %{with lightning}
ac_add_options --enable-calendar
%else
ac_add_options --disable-calendar
%endif
ac_add_options --disable-elf-dynstr-gc
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --enable-crypto
ac_add_options --enable-libxul
ac_add_options --enable-pango
ac_add_options --enable-shared-js
ac_add_options --enable-startup-notification
ac_add_options --enable-system-cairo
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --enable-application=mail
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-branding=icedove/branding
%if %{with xulrunner}
ac_add_options --with-system-libxul
ac_add_options --with-libxul-sdk=$(pkg-config --variable=sdkdir libxul)
%endif
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-ffi
ac_add_options --with-system-jpeg
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --enable-single-profile
ac_add_options --disable-profilesharing
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
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

%if %{with enigmail}
cd mailnews/extensions/enigmail
./makemake -r -o %{objdir}
%{__make} -j1 -C %{objdir}/mailnews/extensions/enigmail \
	STRIP="/bin/true" \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%{__make} -j1 -C %{objdir}/mailnews/extensions/enigmail xpi \
	STRIP="/bin/true" \
	CC="%{__cc}" \
	CXX="%{__cxx}"
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

cp -a mozilla/dist/icedove/* $RPM_BUILD_ROOT%{_libdir}/%{name}/
 
%if %{with xulrunner}
# needed to find mozilla runtime
ln -s ../xulrunner $RPM_BUILD_ROOT%{_libdir}/%{name}/xulrunner
%endif
 
# Enable crash reporter for Thunderbird application
%if %{with crashreporter}
%{__sed} -i -e 's/\[Crash Reporter\]/[Crash Reporter]\nEnabled=1/' $RPM_BUILD_ROOT%{_libdir}/%{name}/application.ini

# Add debuginfo for crash-stats.mozilla.com
install -d $RPM_BUILD_ROOT%{_exec_prefix}/lib/debug%{_libdir}/%{name}
cp -a mozilla/dist/%{name}-%{version}.en-US.linux-*.crashreporter-symbols.zip $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}/%{name}
%endif

# copy manually lightning files, somewhy they are not installed by make
cp -a mozilla/dist/bin/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103} \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/extensions

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

%if %{with enigmail}
ext_dir=$RPM_BUILD_ROOT%{_libdir}/%{name}/extensions/\{847b3a00-7ab1-11d4-8f02-006008948af5\}
install -d $ext_dir/{chrome,components,defaults/preferences,modules}
cd mozilla/dist/bin
cp -rfLp chrome/enigmail.jar $ext_dir/chrome
cp -rfLp components/enig* $ext_dir/components
cp -rfLp defaults/preferences/enigmail.js $ext_dir/defaults/preferences
cp -rfLp modules/{commonFuncs,enigmailCommon,keyManagement,pipeConsole,subprocess}.jsm $ext_dir/modules
cp -rfLp modules/{subprocess_worker_unix,subprocess_worker_win}.js $ext_dir/modules
cd -
cp -p %{topdir}/mozilla/mailnews/extensions/enigmail/package/install.rdf $ext_dir
cp -p %{topdir}/mozilla/mailnews/extensions/enigmail/package/chrome.manifest $ext_dir/chrome.manifest
%endif

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
#%{_libdir}/%{name}/greprefs.js
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%attr(755,root,root) %{_libdir}/%{name}/libmozalloc.so
%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so
%attr(755,root,root) %{_libdir}/%{name}/libxul.so
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/plugin-container
%endif

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/isp
#%{_libdir}/%{name}/modules
%{_libdir}/%{name}/searchplugins
%if %{with xulrunner}
%{_libdir}/%{name}/xulrunner
%else
%{_libdir}/%{name}/dictionaries
%endif

%{_pixmapsdir}/icedove.png
%{_desktopdir}/icedove.desktop

%dir %{_datadir}/%{name}
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
%dir %{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/application.ini
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/chrome
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/chrome.manifest
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/defaults
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/install.rdf
%dir %{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/components
%attr(755,root,root) %{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/components/*.so
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/components/*.js
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/components/*.manifest
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/components/*.xpt
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/modules
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/calendar-js
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/timezones.sqlite
%endif

%if %{with enigmail}
%files addon-enigmail
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/defaults
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/chrome
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/chrome.manifest
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/install.rdf
%dir %{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/components
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/components/*.xpt
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/components/*.js
%dir %{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/modules
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/modules/*.jsm
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}/modules/*.js
%endif
