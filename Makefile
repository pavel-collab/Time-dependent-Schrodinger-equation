all:
	gcc -fPIC -shared -o lib.so lib.c

matrix:
	g++ -o sandbox sandbox.cpp

clean:
	rm lib.so
	rm sandbox