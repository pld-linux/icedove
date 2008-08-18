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

MOZARGS=
MOZLOCALE="$(/usr/bin/locale | grep "^LC_MESSAGES=" | \
		sed -e "s|LC_MESSAGES=||g" -e "s|\"||g" )"
for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
	eval MOZLANG="$(echo $MOZLANG | sed -e "s|_\([^.]*\).*|-\1|g")"

	if [ -f $LIBDIR/chrome/$MOZLANG.jar ]; then
		MOZARGS="-UILocale $MOZLANG"
		break
	fi
done

if [ -z "$MOZARGS" ]; then
	# try harder
	for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
		eval MOZLANG="$(echo $MOZLANG | sed -e "s|_.*||g")"

		LANGFILE=$(echo ${MOZILLA_FIVE_HOME}/chrome/${MOZLANG}*.jar \
				| sed 's/\s.*//g' )
		if [ -f "$LANGFILE" ]; then
			MOZLANG=$(basename "$LANGFILE" | sed 's/\.jar//')
			MOZARGS="-UILocale $MOZLANG"
			break
		fi
	done
fi

if [ -n "$MOZARGS" ]; then
	ICEDOVE="$LIBDIR/icedove $MOZARGS"
else
	ICEDOVE="$LIBDIR/icedove"
fi

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
