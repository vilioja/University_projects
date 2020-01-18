module TriangleHexaton
	use PointHexatonCoords
	implicit none

	!Tyyppi kolmioiden säilytykseen
	type :: TriangleInfo
		integer :: triname
		integer :: tripoint(3)
	end type TriangleInfo

contains

	!Funktio uuden kolmion luomiseen
	type(TriangleInfo) function NewTriangle(nam, tripoi)
		implicit none
		integer, intent(in) :: nam, tripoi(3)
		NewTriangle=TriangleInfo(nam, tripoi)
	end function NewTriangle

	subroutine TriangleList(triagle, sizz, list2, point, siz, list, trirow, porow, poprow)
		implicit none
		integer :: point, triagle, point1, point2, point3
		integer :: siz, sizz
		type(PointInfo), allocatable :: list(:)
		type(TriangleInfo), allocatable :: list2(:)
		integer :: i, j, k, l, pointname, trirow, triprow, porow, poprow, pointam, triname, triam, tripoint(3), a, m, h
		real :: pos(3)


		!Kutsutaan PointListiä
		call PointList(point, siz, list, trirow, porow, poprow)

		pointam = 0

		do h=1,porow
			pointam=pointam+h
		end do

		triam=0

		!Lasketaan kolmioiden määrä
		do j=1,trirow
			triam=triam+j*2-1
		end do

		sizz=triam
		allocate(list2(sizz*8))

		triname=0
		a=1
		tripoint=0

		do m=1,8  !käsiteltävä oktantti
			do k=1,trirow   !käsiteltävä rivi

				do j=1,k    !käsiteltävä solmu tässä rivissä
				
					point1=0
					point2=0
					point3=0

					!Kolmion nimeäminen
					triname=triname+1

					!Määritellään kolmion pisteet
					if(j == 1) then
						point1=k*(k-1)/2+j +pointam*(m-1)
						point2=k*(k+1)/2+j +pointam*(m-1)
						point3=k*(k+1)/2+j+1 +pointam*(m-1)

						!Ylöspäin osoittavat kolmiot
						tripoint = (/point1, point2, point3/)
						list2(a)=NewTriangle(triname, tripoint)
					end if

					if(j > 1) then
						point1=k*(k-1)/2+j-1 +pointam*(m-1)
						point2=k*(k-1)/2+j +pointam*(m-1)
						point3=k*(k+1)/2+j +pointam*(m-1)
		
						!Ylöspäin osoittavat kolmiot
						tripoint = (/point1, point2, point3/)
						list2(a)=NewTriangle(triname, tripoint)
			
						a=a+1
						!Kolmion nimi
						triname= triname +1

						point1=k*(k-1)/2+j +pointam*(m-1)
						point2=k*(k+1)/2+j +pointam*(m-1)
						point3=k*(k+1)/2+j+1 +pointam*(m-1)

						!Alaspäin osoittavat kolmiot
						tripoint = (/point1, point2, point3/)
						list2(a)=NewTriangle(triname, tripoint)
					end if

					a=a+1

				end do
			end do
		end do

	end subroutine TriangleList

end module
