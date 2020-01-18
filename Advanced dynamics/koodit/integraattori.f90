program integraattori
	use funktiot
	implicit none
	integer :: kpl				!kuinka monta kappaletta on simuloitavana
	integer :: ios, x, i, j		!iostat tiedostojen lukuun, x, i ja j ovat apumuuttujia
	integer :: kirjaus			!kirjaus kertoo kuinka mones simuloitu paikka aina tallennetaan
	integer :: indeksi			!kertoo käsiteltävän matriisin rivin indeksin, eli käytnnössä mitä kappaletta käsitellään
	integer :: leapf			!jos leapf on 1, käytetään leapfrogia, muutoin käytetään rungekuttaa
	double precision :: aikavali			!aikaväli kertoo kuinka kauan systeemiä simuloidaan, yksiköt vuosissa
	double precision :: t, tp				!t kertoo aika-askeleen pituuden, yksiköt vuosissa. tp on sama päivissä, käytetään laskuissa
	double precision :: aika				!aika kertoo tämänhetkisen ajan (alussa siis 0), sen avulla katsotaan milloin lopetetaan

	double precision, allocatable :: paikat(:,:), nopeudet(:,:), massat(:)		!säilötään näihin kappaleiden tiedot
	double precision, allocatable :: uudetpaikat(:,:), uudetnopeudet(:,:)		!väliaikaiset varastot lasketuille uusille paikoille ja nopeuksille
	character(len=999) :: rivi										!luetaan riviin tietoa tiedostosta ja lisäksi kirjoitetaan siihen tallennetavaksi haluttava tieto
	character(len=80) :: arg, inputfile, outputfile					!luetaan tämän avulla komentoriviargumentteja, inputfile ja outputfile ovat tiedostojen nimiä, joista luetaan alkudata ja joihin simuloitu data tallennettaan
	double precision :: a(8,1,3)			!lista runge-kutta funktion antamista arvoista
	double precision :: b(6)				!lista leapfrog funktion antamista arvoista
	double precision :: r0(1,3),v0(1,3),r1(1,3),v1(1,3)		!apumuuttujia uusien paikkojen ja nopeuksien kirjaukseen

!--------------------------------------------------------------------------------

	call get_command_argument(1,inputfile)		!luetaan inputfile ja outputfile komentoriviargumentteina
	call get_command_argument(2,outputfile)
	
	kpl = 0
	open(unit=1,file=trim(inputfile),status='old')	!luetaan tiedostosta simuloitavien kappaleiden määrä katsomalla rivimääriä

	do
		read(1,'(A)',iostat=ios) rivi	!luetaan tiedostosta rivi kerrallaan
		if(ios /= 0) exit				!jos tiedosto loppuu, lopetetaan
		if (index(rivi,"#") == 0) then	!mikäli rivillä ei ole #-merkkiä merkitsemässä kommenttiriviä, kasvatetaan kappalemäärää
			kpl = kpl + 1
		end if
	end do

	close(1)
	
	
!-------määritellään kaikki vakiot ja muuttujat--------

	call get_command_argument(3,arg)	!luetaan kuinka kauan simulaatiota pyöritetään vuosissa
	read(arg,*) aikavali
	call get_command_argument(4,arg)	!kuinka tiheästi tuloksia kirjataan
	read(arg,*) kirjaus
	call get_command_argument(5,arg)	!aika-askeleen pituus vuosissa
	read(arg,*) t
	call get_command_argument(6,arg)
	read(arg,*) leapf
	
	tp = t*dble(365.25)					!tp:tä käytetään laskuissa
	indeksi = 1
	aika = dble(0.)
	
	allocate(paikat(kpl,3))
	allocate(nopeudet(kpl,3))
	allocate(massat(kpl))

	allocate(uudetpaikat(kpl,3))
	allocate(uudetnopeudet(kpl,3))



!-------luetaan taulukoihin kappaleiden alkudata

	open(unit=1,file=trim(inputfile),status='old')

	do
		read(1,'(A)',iostat=ios) rivi	!luetaan tiedostosta rivi kerrallaan
		if(ios /= 0) exit				!jos tiedosto loppuu, lopetetaan
		if (index(rivi,"#") == 0) then	!mikäli rivillä ei ole #-merkkiä merkitsemässä kommenttiriviä, luetaan dataa
			rivi = trim(rivi)
			read(rivi,*) paikat(indeksi,:), nopeudet(indeksi,:), massat(indeksi)
			indeksi = indeksi + 1
		end if
	end do

	close(1)

	massat = massat/(dble(1.998e30))			!massat auringon massoiksi

!-------lasketaan kappaleiden uusia arvoja ja kirjoitetaan muistiin

	open(unit=1,file=trim(outputfile),status='replace')

	rivi = ""

	do i=1,kpl										!kirjataan kappaleiden massat
		write(arg,*) massat(i)
		rivi = trim(rivi)//adjustl(trim(arg))
		if (i /= kpl) then
			rivi = trim(rivi)//','
		end if
	end do

	write(1,'(A)') trim(rivi)

	rivi = ""
	do i=1,kpl										!kirjataan kappaleiden alkupaikat ja -nopeudet muistiin
		do j=1,3
			write(arg,*) paikat(i,j)
			rivi = trim(rivi)//adjustl(trim(arg))
			rivi = trim(rivi)//','
		end do
		do j=1,3
			write(arg,*) nopeudet(i,j)
			rivi = trim(rivi)//adjustl(trim(arg))

			if (j /= 3) then
				rivi = trim(rivi)//','
			elseif (i /= kpl) then
				rivi = trim(rivi)//';'
			end if
		end do
	end do

	write(1,'(A)') trim(rivi)

	x = 1						!muuttujan avulla kirjataan vain joka 'kirjaus' laskettu paikka
	
	do while (aika <= aikavali)
		if (leapf == 1) then		!jos leapf on 1, käytetään leapfrogia, muutoin käytetään rungekuttaa
			do i=1,kpl
				indeksi = i
				r0(1,:) = paikat(i,:)
				v0(1,:) = nopeudet(i,:)
				b = leapfrog(r0,v0,tp,paikat,massat,indeksi,kpl)
				uudetpaikat(i,:) = b(1:3)
				uudetnopeudet(i,:) = b(4:6)
			end do
		else
			do i=1,kpl
				indeksi = i
				r0(1,:) = paikat(i,:)
				v0(1,:) = nopeudet(i,:)
				a = rungekutta(r0,v0,tp,paikat,massat,indeksi,kpl)
				r1(1,:) = paikat(i,:)+(tp/dble(6))*(a(1,1,:)+2*a(3,1,:)+2*a(5,1,:)+a(7,1,:))
				v1(1,:) = nopeudet(i,:)+(tp/dble(6))*(a(2,1,:)+2*a(4,1,:)+2*a(6,1,:)+a(8,1,:))
				uudetpaikat(i,:) = r1(1,:)
				uudetnopeudet(i,:) = v1(1,:)
			end do
		end if

		paikat = uudetpaikat
		nopeudet = uudetnopeudet
		if (modulo(x,kirjaus) == 0) then
			print*, x
			rivi = ""
			do i=1,kpl
				do j=1,3
					write(arg,*) paikat(i,j)
					rivi = trim(rivi)//adjustl(trim(arg))
					rivi = trim(rivi)//','
				end do
				do j=1,3
					write(arg,*) nopeudet(i,j)
					rivi = trim(rivi)//adjustl(trim(arg))

					if (j /= 3) then
						rivi = trim(rivi)//','
					elseif (i /= kpl) then
						rivi = trim(rivi)//';'
					end if
				end do
			end do
			write(1,'(A)') trim(rivi)
		end if
		
		aika = aika + t
		x = x + 1
	end do

	close(1)
end program integraattori
