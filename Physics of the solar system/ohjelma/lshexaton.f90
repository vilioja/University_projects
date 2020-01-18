module LSHexaton
	use PointHexatonCoords
	use TriangleHexaton
	implicit none

	!Tyyppi kolmioiden kirkkaudelle
	type :: BrightInfo
		integer :: triname
		double precision :: bright
	end type BrightInfo


contains

	!Funktio kirkkausinfon luomiseen
	type(BrightInfo) function NewBright(naam, bri)
		implicit none
		integer, intent(in) :: naam
		double precision, intent(in) :: bri
		NewBright=BrightInfo(naam, bri)
	end function NewBright

	!Funktio kahden vektorin välisen kulman laskemiseen
	function valinenkulma(asteroid,toinen) result(kulma)
		real, intent(in) :: asteroid(3),toinen(3)
		real :: kulma, radkulma, pistetulo, aspituus, toinpituus
		pistetulo = (asteroid(1)*toinen(1) + asteroid(2)*toinen(2) + asteroid(3)*toinen(3))
		aspituus = sqrt((asteroid(1))**2 + (asteroid(2))**2 + (asteroid(3))**2)
		toinpituus = sqrt((toinen(1))**2 + (toinen(2))**2 + (toinen(3))**2)
		kulma = ((pistetulo) / (aspituus * toinpituus))
	end function



	subroutine LommelSeeliger(bright, sizz, list3)
		implicit none
		integer :: point, triagle, point1, point2, point3
		integer :: siz, sizz
		type(PointInfo), allocatable :: list(:)
		type(TriangleInfo), allocatable :: list2(:)
		type(BrightInfo), allocatable :: list3(:)
		integer :: i, j, k, l, pointname, trirow, triprow, porow, poprow, pointam, triname, triam, tripoint(3), m
		integer :: kolmionumero, pistenumero
		real :: pos(3), aurcoords(3), maacoords(3), calpos(3,3), vectora(3), vectorb(3), vectorc(3), normal(3)
		real :: triala, p, a, b, c, myy, myy0, totkirkkaus, vaihekulma, totlambert
		double precision :: bri, bright, brilam
		character(len=80) :: lsoutputfile, lsinfofile, pisteetjakirkkaudet

		!Kysytään tietoja
		write(6,*) ""
		write(6,*) "---Kirkkausdata tallennetaan tiedostoon rawbri. Luettava versio tallenetaan tiedostoon infobri.---"
		write(6,*) "---Lopullinen data menee tiedostoon data.---"
		write(6,*) ""
		!write(6,*) "Give name for raw data file"
		!read(5,*) lsoutputfile
		!lsoutputfile=trim(lsoutputfile)
		lsoutputfile = "rawbri"
		!write(6,*) "Give name for informative data file"
		!read(5,*) lsinfofile
		!lsinfofile=trim(lsinfofile)
		lsinfofile = "infobri"
		!write(6,*) "Anna lopullisen tiedoston nimi"
		!read(5,*) pisteetjakirkkaudet
		!pisteetjakirkkaudet = trim(pisteetjakirkkaudet)
		pisteetjakirkkaudet = "data"
		!Raakadata
		open(unit=3, file=lsoutputfile, status='replace')
		!Ihmisdata
		open(unit=4, file=lsinfofile, status='replace')
		!Lopullinen data
		open(unit=7, file=pisteetjakirkkaudet, status='replace')

		write(6,*) "Asteroidi on origossa. Anna Auringon koordinaatit karteesisessa koordinaatistossa (x,y,z)."
		write(6,*) "Etäisyydellä ei ole väliä, vain kulmalla. Kokoluokka ~100 on hyvä:"
		read(5,*) aurcoords(1), aurcoords(2), aurcoords(3)
		write(6,*) "Anna havaitsijan koordinaatit karteesisessa koordinaatistossa (x,y,z). Sama suuruusluokka:"
		read(5,*) maacoords(1), maacoords(2), maacoords(3)

		!Kutsutaan TriangleListiä
		call TriangleList(triagle, sizz, list2, point, siz, list, trirow, porow, poprow)

		triam=sizz
		allocate(list3(triam*8))

		!Kirjoitetaan auringon ja havaitsijan paikat ylös
		write(7,*) aurcoords(1)
		write(7,*) aurcoords(2)
		write(7,*) aurcoords(3)
		write(7,*) maacoords(1)
		write(7,*) maacoords(2)
		write(7,*) maacoords(3)

		totkirkkaus = 0

		do k=1, triam*8	!missä kolmiossa mennään

			triname=list2(k)%triname
			tripoint(1) = list2(k)%tripoint(1)
			tripoint(2) = list2(k)%tripoint(2)
			tripoint(3) = list2(k)%tripoint(3)

		  	do l=1,3
				pointname=tripoint(l)
				pos=list(pointname)%pos

				calpos(l,:)=pos
			end do


			vectora=calpos(2,:)-calpos(1,:)
			vectorb=calpos(3,:)-calpos(1,:)
			vectorc=calpos(3,:)-calpos(2,:)


			normal(1)=vectora(2)*vectorb(3)-vectora(3)*vectorb(2)
			normal(2)=vectora(3)*vectorb(1)-vectora(1)*vectorb(3)
			normal(3)=vectora(1)*vectorb(2)-vectora(2)*vectorb(1)

			!osa normaaleista osoittaa väärään suuntaan
			!käännetään normaalit oikein päin jos ei ole
			!eka oktantti, katotaan että x-suunta on positiivinen
			if (k <= triam) then
				if (normal(1) < 0) then
					normal = -normal
				end if
			end if
			
			!toka oktantti, katotaan että x on negatiivinen
			if (k > triam .and. k <= triam*2) then
				if (normal(1) > 0) then
					normal = -normal
				end if
			end if

			!kolmas, katotaan että x on negatiivinen
			if (k > triam*2 .and. k <= triam*3) then
				if (normal(1) > 0) then
					normal = -normal
				end if
			end if

			!neljäs, katotaan että x on positiivinen
			if (k > triam*3 .and. k <= triam*4) then
				if (normal(1) < 0) then
					normal = -normal
				end if
			end if

			!alempi pallonpuolisko
			!viides, katotaan että x on positiivinen
			if (k > triam*4 .and. k <= triam*5) then
				if (normal(1) < 0) then
					normal = -normal
				end if
			end if

			!kuudes, katotaan että x on negatiivinen
			if (k > triam*5 .and. k <= triam*6) then
				if (normal(1) > 0) then
					normal = -normal
				end if
			end if

			!seittemäs, katotaan että x on negatiivinen
			if (k > triam*6 .and. k <= triam*7) then
				if (normal(1) > 0) then
					normal = -normal
				end if
			end if

			!kahdeksas, katotaan että x on positiivinen
			if (k > triam*7) then
				if (normal(1) < 0) then
					normal = -normal
				end if
			end if

			myy = valinenkulma(normal,maacoords)
			myy0 = valinenkulma(normal,aurcoords)
			
			!abc vektoreiden pituuksia
			a=SQRT((vectora(1))**2+(vectora(2))**2+(vectora(3))**2)
			b=SQRT((vectorb(1))**2+(vectorb(2))**2+(vectorb(3))**2)
			c=SQRT((vectorc(1))**2+(vectorc(2))**2+(vectorc(3))**2)

			!Heronin kaava
			p=(a+b+c)/2
			triala =SQRT(p*(p-a)*(p-b)*(p-c))


			if (myy > 0. .and. myy0 > 0.) then
				bri = triala*myy*myy0*(1./4.)*(1./(myy+myy0))
				brilam = triala*myy*myy0
			else
				bri = 0
				brilam = 0
			end if

			list3(k)=NewBright(triname, bri)

			totkirkkaus = totkirkkaus + bri
			totlambert = totlambert + brilam

			!Writing raw output
			write(3,*) list3(k)%triname
			write(3,*) list3(k)%bright
			!Writing informative output
			write(4,*) "Triangle number: ", list3(k)%triname
			write(4,*) "Brightness: ", list3(k)%bright
			write(4,*) !Empty line

			!data for plotting
			write(7,*) bri
			write(7,*) list(tripoint(1))%pos(1)
			write(7,*) list(tripoint(1))%pos(2)
			write(7,*) list(tripoint(1))%pos(3)
			write(7,*) list(tripoint(2))%pos(1)
			write(7,*) list(tripoint(2))%pos(2)
			write(7,*) list(tripoint(2))%pos(3)
			write(7,*) list(tripoint(3))%pos(1)
			write(7,*) list(tripoint(3))%pos(2)
			write(7,*) list(tripoint(3))%pos(3)

		end do

		vaihekulma = acos(valinenkulma(aurcoords,maacoords))

		write(4,*) "Total brightness (Lambert): ", totlambert
		write(4,*) "Total brightness (Lommel-Seeliger): ", totkirkkaus
		write(4,*) "Phase angle, in radians: ", vaihekulma
		write(4,*) "Phase angle, in degrees: ", (vaihekulma * (180/(4.*atan(1.))))

		close(3)
		close(4)
		close(7)

		write(6,*) ""
		write(6,*) "Vaihekulma oli ", vaihekulma, " radiaania, tai ", (vaihekulma * (180/(4.*atan(1.)))), " astetta"
		write(6,*) "Asteroidin kokonaiskirkkaus Lambertilla oli ", totlambert
		write(6,*) "Lommel-Seeligerillä ", totkirkkaus

	end subroutine LommelSeeliger

end module
