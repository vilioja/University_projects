program Asteroid
	use PointHexatonCoords
	use TriangleHexaton
	use LSHexaton
	implicit none

	!Muuttujat
	integer :: point, triagle
	integer :: siz, sizz
	double precision :: bright
	type(PointInfo), allocatable :: list(:)
	type(TriangleInfo), allocatable :: list2(:)
	type(BrightInfo), allocatable  :: list3(:)

	!Kolmiointi
	write(6,*) ""
	write(6,*) "---------------------"
	write(6,*) "Asteroidin kolmiointi"
	write(6,*) "---------------------"
	write(6,*) ""

	call LommelSeeliger(bright, sizz, list3)

end program Asteroid
