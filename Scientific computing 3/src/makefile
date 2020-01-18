integrator.exe: functions.o integrator.o
	gfortran -o integrator.exe integrator.o functions.o
functions.o: functions.f90
	gfortran -c functions.f90
integrator.o: integrator.f90
	gfortran -c integrator.f90
clean:
	rm integrator.o functions.mod functions.o
