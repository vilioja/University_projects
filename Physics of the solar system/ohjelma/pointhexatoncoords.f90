module PointHexatonCoords
	implicit none

	!Tyyppi pisteiden säilytykseen
	type :: PointInfo
		integer :: pointname
		real :: pos(3)
	end type PointInfo

contains

	!Funktio uusien pisteiden luomiseen
	type(PointInfo) function NewPoint(n, p)
		implicit none
		integer, intent(in) :: n
		real, intent(in) :: p(3)
		NewPoint=PointInfo(n, p)
	end function NewPoint

	!Subrutiini järjestää pisteet listaan
	subroutine PointList(point, siz, list, trirow, porow, poprow)
		implicit none
		integer, intent(in) :: point
		integer :: pointam, siz
		type(PointInfo), allocatable, intent(inout) :: list(:)
		integer :: i, j, h, pointname, trirow, porow, poprow, m
		real :: pos(3), a, b, c, x, y, z, az, el, r, halfpi
		character(len=80) :: outputfile, infofile


		!Kysytään alkuparametrejä
		write(6,*) "Anna ellipsoidin puoliakselien pituudet (a,b,c). Kokoluokka <10 on hyvä:"
		read(5,*) a, b, c
		write(6,*) "Kuinka monta kolmioriviä on yhdessä oktantissa:"
		read(5,*) trirow


		!Yhdellä kolmiorivillä on kaksi riviä pisteitä
		porow=trirow+1
		pointam=0

		do h=1,porow
			pointam=pointam+h
		end do

		siz=pointam

		allocate(list(siz*8))  !koko pallossa kahdeksan osaa

		!Alkuarvoja pisteiden laskentaan
		x=0
		y=0
		z=0
		r=0
		az=0
		el=0
		halfpi=1.570796327

		!Pisteitä rivillä ja koko oktantin pistemäärä
		pointam=0
		poprow=0
		pointname=0

		!Kysyy tiedostoja	
		!write(6,*) "--Point files--------------"
		!write(6,*) "Give name for raw data file"
		!read(5,*) outputfile
		!outputfile=trim(outputfile)
		write(6,*) ""
		write(6,*) "---Pistedata tallennetaan tiedostoon raw. Luettava versio tallenetaan tiedostoon info.---"
		write(6,*) ""
		outputfile = "raw"
		!write(6,*) "Give name for informative data file"
		!read(5,*) infofile
		!infofile=trim(infofile)
		infofile = "info"
		!Raakadata
		open(unit=1, file=outputfile, status='replace')
		!Ihmisdata
		open(unit=2, file=infofile, status='replace')

		m=1

		!Lasketaan kulmia pisteiden määrästä
		do i=1,porow
			el=(i-1)*halfpi/trirow
			pointam=pointam+i
			poprow=i

			!R parametriä käytetään paikkojen laskuissa
			r=a*b*c/(b**2*c**2*(sin(el))**2*(cos(az))**2+a**2*c**2*(sin(el))**2*(sin(az))**2+a**2*b**2*(cos(el))**2)**(0.5)

			!Z koordinaatti
			z=r*cos(el)

			!XY riippuu atsimuuttikulmasta
			do j=1,poprow
	
				!Pientä säätöä
				if (poprow==1) then
					az=0
				else
					az=(j-1)*halfpi/(poprow-1)
				end if

				!Lasketaan r uusilla kulmilla
				r=a*b*c/(b**2*c**2*(sin(el))**2*(cos(az))**2+a**2*c**2*(sin(el))**2*(sin(az))**2+a**2*b**2*(cos(el))**2)**(0.5)
	
				!X koordinaatti
				x=r*sin(el)*cos(az)
				!Y koordinaatti
				y=r*sin(el)*sin(az)	

				!Pisteiden numerointi
				pointname=pointname+1

				!Pyöristetään pienet nollaan
				if (x<10**(-6)) then
					x=0
				endif
				if (y<10**(-6)) then
					y=0
				endif
				if (z<10**(-6)) then
					z=0
				endif

				!XYZ listaksi, missä xyz>0 ja -<0
				pos = (/x, y, z/)
				list(m)=NewPoint(pointname, pos)


				!Raakadataa
				write(1,*) list(m)%pos(1)
				write(1,*) list(m)%pos(2)
				write(1,*) list(m)%pos(3)
				!Ihmisdataa
				write(2,*) "Point number: ", list(m)%pointname	
				write(2,*) "X: ", list(m)%pos(1)
				write(2,*) "Y: ", list(m)%pos(2)
				write(2,*) "Z: ", list(m)%pos(3)
				write(2,*) ""

				m=m+1
			end do
		end do

		

		!ylempi pallopuolikas:

		!XYZ listaan, missä yz>0 ja x<0 --->2. pala
		do m=1, pointam
			pointname=pointam+m
			x=-list(m)%pos(1)
			y=list(m)%pos(2)
			z=list(m)%pos(3)

			pos = (/x, y, z/)
			list(pointname)=NewPoint(pointname, pos)

				!Raakadataa
				write(1,*) list(pointname)%pos(1)
				write(1,*) list(pointname)%pos(2)
				write(1,*) list(pointname)%pos(3)
				!Ihmisdataa
				write(2,*) "Point number: ", list(pointname)%pointname
				write(2,*) "X: ", list(pointname)%pos(1)
				write(2,*) "Y: ", list(pointname)%pos(2)
				write(2,*) "Z: ", list(pointname)%pos(3)
				write(2,*) ""

		end do
		!XYZ listaan, missä z>0 ja xy<0 ---->3. pala
		do m=1, pointam
			pointname=pointam*2+m
			x=-list(m)%pos(1)
			y=-list(m)%pos(2)
			z=list(m)%pos(3)

			
			pos = (/x, y, z/)
			list(pointname)=NewPoint(pointname, pos)

				!Raakadataa
				write(1,*) list(pointname)%pos(1)
				write(1,*) list(pointname)%pos(2)
				write(1,*) list(pointname)%pos(3)
				!Ihmisdataa
				write(2,*) "Point number: ", list(pointname)%pointname
				write(2,*) "X: ", list(pointname)%pos(1)
				write(2,*) "Y: ", list(pointname)%pos(2)
				write(2,*) "Z: ", list(pointname)%pos(3)
				write(2,*) ""

		end do
		!XYZ listaan, missä xz>0 ja y<0 ----->4. pala
		do m=1, pointam
			pointname=pointam*3+m
			x=list(m)%pos(1)
			y=-list(m)%pos(2)
			z=list(m)%pos(3)

			
			pos = (/x, y, z/)
			list(pointname)=NewPoint(pointname, pos)

				!Raakadataa
				write(1,*) list(pointname)%pos(1)
				write(1,*) list(pointname)%pos(2)
				write(1,*) list(pointname)%pos(3)
				!Ihmisdataa
				write(2,*) "Point number: ", list(pointname)%pointname
				write(2,*) "X: ", list(pointname)%pos(1)
				write(2,*) "Y: ", list(pointname)%pos(2)
				write(2,*) "Z: ", list(pointname)%pos(3)
				write(2,*) ""


		end do

		!alempi puolikas:
		!XYZ listaan, missä xy>0 ja z<0 ------>5. pala
		do m=1, pointam
			pointname=pointam*4+m
			x=list(m)%pos(1)
			y=list(m)%pos(2)
			z=-list(m)%pos(3)

			
			pos = (/x, y, z/)
			list(pointname)=NewPoint(pointname, pos)

				!Raakadataa
				write(1,*) list(pointname)%pos(1)
				write(1,*) list(pointname)%pos(2)
				write(1,*) list(pointname)%pos(3)
				!Ihmisdataa
				write(2,*) "Point number: ", list(pointname)%pointname
				write(2,*) "X: ", list(pointname)%pos(1)
				write(2,*) "Y: ", list(pointname)%pos(2)
				write(2,*) "Z: ", list(pointname)%pos(3)
				write(2,*) ""

		end do
		!XYZ listaan, missä y>0 ja xz<0 ----->6. pala
		do m=1, pointam
			pointname=pointam*5+m
			x=-list(m)%pos(1)
			y=list(m)%pos(2)
			z=-list(m)%pos(3)

			
			pos = (/x, y, z/)
			list(pointname)=NewPoint(pointname, pos)

				!Raakadataa
				write(1,*) list(pointname)%pos(1)
				write(1,*) list(pointname)%pos(2)
				write(1,*) list(pointname)%pos(3)
				!Ihmisdataa
				write(2,*) "Point number: ", list(pointname)%pointname
				write(2,*) "X: ", list(pointname)%pos(1)
				write(2,*) "Y: ", list(pointname)%pos(2)
				write(2,*) "Z: ", list(pointname)%pos(3)
				write(2,*) ""

		end do
		!XYZ listaan, missä ->0 ja xyz<0 -----> 7. pala
		do m=1, pointam
			pointname=pointam*6+m
			x=-list(m)%pos(1)
			y=-list(m)%pos(2)
			z=-list(m)%pos(3)

			
			pos = (/x, y, z/)
			list(pointname)=NewPoint(pointname, pos)

				!Raakadataa
				write(1,*) list(pointname)%pos(1)
				write(1,*) list(pointname)%pos(2)
				write(1,*) list(pointname)%pos(3)
				!Ihmisdataa
				write(2,*) "Point number: ", list(pointname)%pointname
				write(2,*) "X: ", list(pointname)%pos(1)
				write(2,*) "Y: ", list(pointname)%pos(2)
				write(2,*) "Z: ", list(pointname)%pos(3)
				write(2,*) ""

		end do
		!XYZ listaan, missä x>0 ja yz<0  -------> 8. pala
		do m=1, pointam
			pointname=pointam*7+m
			x=list(m)%pos(1)
			y=-list(m)%pos(2)
			z=-list(m)%pos(3)
			
			
			pos = (/x, y, z/)
			list(pointname)=NewPoint(pointname, pos)

				!Raakadataa
				write(1,*) list(pointname)%pos(1)
				write(1,*) list(pointname)%pos(2)
				write(1,*) list(pointname)%pos(3)
				!Ihmisdataa
				write(2,*) "Point number: ", list(pointname)%pointname
				write(2,*) "X: ", list(pointname)%pos(1)
				write(2,*) "Y: ", list(pointname)%pos(2)
				write(2,*) "Z: ", list(pointname)%pos(3)
				write(2,*) ""

		end do

		close(1)
		close(2)

	end subroutine PointList

end module
