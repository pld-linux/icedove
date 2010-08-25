#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

LIBDIR="@LIBDIR@/icedove"

# copy profile from Thunderbird if its available and if no Icedove
# profile exists
if [ ! -d $HOME/.icedove ]; then
	if [ -d $HOME/.thunderbird ]; then
		echo "Copying profile from Thunderbird"
		cp -rf $HOME/.thunderbird $HOME/.icedove
	fi
fi

# compreg.dat and/or chrome.rdf will screw things up if it's from an
# older version.  http://bugs.gentoo.org/show_bug.cgi?id=63999
for f in ~/.icedove/*/{compreg.dat,chrome.rdf,XUL.mfasl}; do
	if [[ -f ${f} && ${f} -ot "$0" ]]; then
		echo "Removing ${f} leftover from older Icedove"
		rm -f "${f}"
	fi
done

ICEDOVE="$LIBDIR/icedove"

if [ "$1" == "-remote" ]; then
	$ICEDOVE "$@"
else
	PING=`$ICEDOVE -remote 'ping()' 2>&1 >/dev/null`
	if [ -n "$PING" ]; then
		$ICEDOVE "$@"
	else
		case "$1" in
		    -compose|-editor)
			$ICEDOVE -remote 'xfeDoCommand (composeMessage)'
			;;
		    *)
			$ICEDOVE -remote 'xfeDoCommand (openInbox)'
			;;
		esac
	fi
fi
