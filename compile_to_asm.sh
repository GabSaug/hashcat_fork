# $1: name of the c file to compile to assembly
# $2 output path
opt="$(echo $3 | sed -e "s/-O0/$(cat /etc/gcc.opt)/g") -Wno-error -fno-inline"

if ! gcc -S -pipe -Iinclude/ -IOpenCL/ -Ideps/LZMA-SDK/C -Ideps/zlib -Ideps/zlib/contrib -Ideps/OpenCL-Headers -Ideps/xxHash -DWITH_CUBIN -Ideps/unrar $opt "$1" -o "$2" -lpthread -ldl -lrt -lm -shared -fPIC -D  MODULE_INTERFACE_VERSION_CURRENT=700; then
	echo "error compile to asm"
	exit 1
fi
