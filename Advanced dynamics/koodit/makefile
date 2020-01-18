integraattori.exe: funktiot.o integraattori.o
	gfortran -o integraattori.exe integraattori.o funktiot.o
funktiot.o: funktiot.f90
	gfortran -c funktiot.f90
integraattori.o: integraattori.f90
	gfortran -c integraattori.f90
clean:
	rm integraattori.o funktiot.mod funktiot.o
