rk4.exe: funktiot.o rk4.o
	gfortran -o rk4.exe rk4.o funktiot.o
funktiot.o: funktiot.f90
	gfortran -c funktiot.f90
rk4.o: rk4.f90
	gfortran -c rk4.f90
clean:
	rm rk4.o funktiot.mod funktiot.o
