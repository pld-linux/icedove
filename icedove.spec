# TODO:
# - separate spec for enigmail
# - fix icedove (building) and installing nss/nspr libs!
# - build with system mozldap
#
# Conditional builds
%bcond_without	enigmail	# don't build enigmail - GPG/PGP support
%bcond_without	gnomeui		# disable gnomeui support
%bcond_without	gnomevfs	# disable GNOME comp. (gconf+libgnome+gnomevfs) and gnomevfs ext.
%bcond_without	gnome		# disable all GNOME components (gnome+gnomeui+gnomevfs)
%bcond_without	ldap		# disable e-mail address lookups in LDAP directories
%bcond_without  lightning	# disable sunbird calendar
%bcond_with		xulrunner	# build with system xulrunner

%if %{without gnome}
%undefine	with_gnomeui
%undefine	with_gnomevfs
%endif

%define		enigmail_ver		1.1

%if %{without xulrunner}
# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)
%endif

Summary:	Icedove - email client
Summary(pl.UTF-8):	Icedove - klient poczty
Name:		icedove
Version:	3.0.5
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		Applications/Networking
Source0:	http://releases.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}.source.tar.bz2
# Source0-md5:	564911289b5d895ba5eaf4b3fbed51e8
Source1:	http://www.mozilla-enigmail.org/download/source/enigmail-%{enigmail_ver}.tar.gz
# Source1-md5:	6304088073928e22f08ab756894329f4
Source2:	%{name}-branding.tar.bz2
# Source2-md5:	2da351522bdd7f4a3bd8aaff4c776976
Source3:	%{name}-rm_nonfree.sh
Source4:	%{name}.desktop
Source5:	%{name}.sh
Source6:	%{name}-enigmail.manifest
Patch0:		%{name}-branding.patch
Patch1:		%{name}-enigmail-shared.patch
Patch2:		%{name}-gcc.patch
Patch3:		%{name}-fonts.patch
Patch4:		%{name}-install.patch
Patch5:		%{name}-hunspell.patch
Patch6:		%{name}-prefs.patch
Patch7:		system-mozldap.patch
URL:		http://www.pld-linux.org/Packages/Icedove
%{?with_gnomevfs:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	freetype-devel >= 1:2.1.8
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	hunspell-devel
BuildRequires:	libIDL-devel >= 0.8.0
%{?with_gnomevfs:BuildRequires:	libgnome-devel >= 2.0}
%{?with_gnomeui:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.8
BuildRequires:	nss-devel >= 1:3.12.0
BuildRequires:	pango-devel >= 1:1.1.0
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.6.22
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zip
%if %{with xulrunner}
%else
Requires:	myspell-common
Requires:	nspr >= 1:4.6.1
Requires:	nss >= 1:3.11.3
Requires:	sqlite3 >= %{sqlite_build_version}
%endif
Obsoletes:	mozilla-thunderbird
Obsoletes:	mozilla-thunderbird-dictionary-en-US
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_cpp		-D_FORTIFY_SOURCE=[0-9]+

# iceweasel/icedove/iceape provide their own versions
%define		_noautoreqdep		libgfxpsshar.so libgkgfx.so libgtkxtbin.so libjsj.so libxpcom_compat.so libxpcom_core.so libxpistub.so
%define		_noautoprovfiles	%{_libdir}/%{name}/components
# we don't want these to satisfy xulrunner-devel
%define		_noautoprov		libgtkembedmoz.so libmozjs.so libxpcom.so libxul.so
# and as we don't provide them, don't require either
%define		_noautoreq		libgtkembedmoz.so libmozjs.so libxpcom.so libxul.so

%description
Icedove is an open-source,fast and portable email client.

%description -l pl.UTF-8
Icedove jest open sourcowym, szybkim i przenośnym klientem poczty.

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
mv -f comm-1.9.1 mozilla
%setup -q -T -D -a2
cd mozilla
%{?with_enigmail:tar xvfz %{SOURCE1} -C mailnews/extensions}
/bin/sh %{SOURCE3}
%patch0 -p1
%{?with_enigmail:%patch1 -p1}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
cd mozilla
export CFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"
export CXXFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"

cp -f %{_datadir}/automake/config.* mozilla/build/autoconf
cp -f %{_datadir}/automake/config.* mozilla/nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

install -d libxul-sdk
ln -snf %{_libdir}/xulrunner-sdk libxul-sdk/sdk

cat << EOF > .mozconfig
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}

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
%if %{with gnomeui}
ac_add_options --enable-gnomeui
%else
ac_add_options --disable-gnomeui
%endif
%if %{with gnomevfs}
ac_add_options --enable-gnomevfs
%else
ac_add_options --disable-gnomevfs
%endif
%if %{with ldap}
ac_add_options --enable-ldap
ac_add_options --with-system-ldap
%else
ac_add_options --disable-ldap
%endif
ac_add_options --disable-crashreporter
ac_add_options --disable-xterm-updates
ac_add_options --enable-postscript
%if %{with lightning}
ac_add_options --enable-calendar
%else
ac_add_options --disable-calendar
%endif
ac_add_options --disable-installer
ac_add_options --disable-jsd
ac_add_options --disable-updater
ac_add_options --disable-xprint
ac_add_options --disable-permissions
ac_add_options --disable-pref-extensions
ac_add_options --enable-canvas
ac_add_options --enable-crypto
ac_add_options --enable-mathml
ac_add_options --enable-pango
ac_add_options --enable-reorder
ac_add_options --enable-startup-notification
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --enable-xft
ac_add_options --enable-application=mail
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --enable-xinerama
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-branding=icedove/branding
%if %{with xulrunner}
ac_add_options --with-libxul-sdk=$(pwd)/libxul-sdk
ac_add_options --enable-shared
%else
ac_add_options --enable-static
%endif
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --enable-single-profile
ac_add_options --disable-profilesharing
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
EOF

%{__make} -j1 -f client.mk build \
	STRIP="/bin/true" \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%if %{with enigmail}
cd mailnews/extensions/enigmail
./makemake -r
%{__make} -C ../../../obj-%{_target_cpu}/mailnews/extensions/enigmail \
	STRIP="/bin/true" \
	CC="%{__cc}" \
	CXX="%{__cxx}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}} \
	       $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}

cd mozilla
%{__make} -C obj-%{_target_cpu}/mail/installer stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/isp $RPM_BUILD_ROOT%{_datadir}/%{name}/isp
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs
ln -s ../../share/%{name}/isp $RPM_BUILD_ROOT%{_libdir}/%{name}/isp
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

%{__sed} -e 's,@LIBDIR@,%{_libdir},' %{SOURCE5} > $RPM_BUILD_ROOT%{_bindir}/icedove
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/thunderbird
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird

install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%if %{with enigmail}
ext_dir=$RPM_BUILD_ROOT%{_libdir}/%{name}/extensions/\{847b3a00-7ab1-11d4-8f02-006008948af5\}
install -d $ext_dir/{chrome,components,defaults/preferences}
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail.jar $ext_dir/chrome
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/enig* $ext_dir/components
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/libenigmime.so $ext_dir/components
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/ipc.xpt $ext_dir/components
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults/preferences/enigmail.js $ext_dir/defaults/preferences
cp -f mailnews/extensions/enigmail/package/install.rdf $ext_dir
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults/preferences
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail-en-US.jar
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail-skin.jar
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmime.jar
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/components/enig*
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/libenigmime.so
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/ipc.xpt
cp -f %{SOURCE6} $ext_dir/chrome.manifest
cp -f icedove/branding/content/icon64.png $RPM_BUILD_ROOT%{_pixmapsdir}/icedove.png
%endif

# remove unecessary stuff
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/README.txt

# never package these
# nss
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{freebl3,nss3,nssckbi,nssdbm3,nssutil3,smime3,softokn3,ssl3}.*
# nspr
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{nspr4,plc4,plds4}.so
# mozldap
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{ldap,ldif,prldap,ssldap}60.so

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
if [ -d %{_libdir}/%{name}/dictionaries ] && [ ! -L %{_libdir}/%{name}/dictionaries ]; then
	mv -v %{_libdir}/%{name}/dictionaries{,.rpmsave}
fi
for d in chrome defaults greprefs icons isp res; do
	if [ -d %{_libdir}/%{name}/$d ] && [ ! -L %{_libdir}/%{name}/$d ]; then
		install -d %{_datadir}/%{name}
		mv %{_libdir}/%{name}/$d %{_datadir}/%{name}/$d
	fi
done
exit 0

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/icedove
%attr(755,root,root) %{_bindir}/mozilla-thunderbird
%attr(755,root,root) %{_bindir}/thunderbird
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.ini
%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%{_libdir}/%{name}/components/*.js
%{_libdir}/%{name}/components/*.xpt
%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so
%attr(755,root,root) %{_libdir}/%{name}/libxpcom.so
%attr(755,root,root) %{_libdir}/%{name}/libxpcom_core.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/*-bin
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/icedove

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/isp
%{_libdir}/%{name}/res

%{_libdir}/%{name}/dependentlibs.list
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/greprefs
%{_datadir}/%{name}/isp
%{_datadir}/%{name}/res

%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.js*
%dir %{_libdir}/%{name}/modules/activity
%{_libdir}/%{name}/modules/activity/*.js
%dir %{_libdir}/%{name}/modules/gloda
%{_libdir}/%{name}/modules/gloda/*.js

%dir %{_libdir}/%{name}/extensions
%{_libdir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

%if %{with lightning}
%files addon-lightning
%defattr(644,root,root,755)
%{_libdir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}
%{_libdir}/%{name}/extensions/calendar-timezones@mozilla.org
%endif

%if %{with enigmail}
%files addon-enigmail
%defattr(644,root,root,755)
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}
%endif
