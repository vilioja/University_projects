ANM: pointhexatoncoords.o trianglehexaton.o lshexaton.o anm.o
	gfortran -o ANM anm.o lshexaton.o trianglehexaton.o pointhexatoncoords.o
pointhexatoncoords.o: pointhexatoncoords.f90
	gfortran -c pointhexatoncoords.f90
trianglehexaton.o: trianglehexaton.f90
	gfortran -c trianglehexaton.f90
lshexaton.o: lshexaton.f90
	gfortran -c lshexaton.f90
anm.o: anm.f90
	gfortran -c anm.f90
clean:
	rm anm.o lshexaton.mod lshexaton.o trianglehexaton.mod trianglehexaton.o pointhexatoncoords.mod pointhexatoncoords.o
