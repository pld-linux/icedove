#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

LIBDIR="@LIBDIR@/icedove"

# copy profile from Thunderbird if its available and if no Icedove
# profile exists
if [ ! -d $HOME/.icedove ] && [ -d $HOME/.thunderbird ]; then
	echo "Copying profile from Thunderbird"
	cp -a $HOME/.thunderbird $HOME/.icedove
fi

# compreg.dat and/or chrome.rdf will screw things up if it's from an
# older version. http://bugs.gentoo.org/show_bug.cgi?id=63999
for f in ~/.icedove/*/{compreg.dat,chrome.rdf,XUL.mfasl}; do
	[ -f "$f" ] || continue
	if [ "$f" -ot "$0" ] || [ "$f" -ot "$LIBDIR/components/compreg.dat" ]; then
		echo "Removing $f leftover from older Icedove"
		rm -f "$f"
	fi
done

ICEDOVE="$LIBDIR/icedove"

if [ "$1" = "-remote" ]; then
	exec $ICEDOVE "$@"
else
	PING=$($ICEDOVE -remote 'ping()' 2>&1 >/dev/null)
	if [ -n "$PING" ]; then
		exec $ICEDOVE "$@"
	else
		case "$1" in
		-compose|-editor)
			exec $ICEDOVE -remote 'xfeDoCommand (composeMessage)'
			;;
		*)
			exec $ICEDOVE -remote 'xfeDoCommand (openInbox)'
			;;
		esac
	fi
fi
