mkdir -p build/bin
make clean > /dev/null
rm build/bin/hashcat
opt="$(echo $1 | sed -e "s/-O0/$(cat /etc/gcc.opt)/g") -Wno-error -finline-limit=2"
make EXTRA_CFLAGS=" $opt" -j -n &> log_make.txt
if ! make EXTRA_CFLAGS="$opt" -j ; then
	echo "error make"
	exit 1
fi
if ! cp hashcat build/bin/hashcat; then
	echo "error copying binary"
	exit 1
fi
