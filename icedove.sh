#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

LIBDIR="@LIBDIR@/icedove"

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
