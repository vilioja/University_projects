module funktiot
	implicit none

contains

	function vektoripituus(a) result(x)			!funktio vektorin pituuden laskemiselle
		implicit none
		double precision, intent(in) :: a(1,3)
		double precision :: x
		
		x = sqrt(a(1,1)**2 + a(1,2)**2 + a(1,3)**2)
	end function vektoripituus


	function nopeudenmuutos(r,paikat,massat,indeksi,kpl) result(muutos)	!funktio nopeuden muutoksen laskemiselle. summataan gravitaation vaikutukset yhteen kappaleeseen
		implicit none
		double precision, dimension(:,:), intent(in) :: r,paikat
		double precision, intent(in) :: massat(:)
		integer, intent(in) :: indeksi, kpl
		double precision, allocatable :: muutos(:,:)
		integer :: i
		double precision :: grav
		grav = 4*((dble(4)*dble(atan(dble(1))))**2)/(dble(365.25)**2) !gravitaatiovakio yksiköissä AU, d, M_sol

		muutos = r
		muutos = 0

		do i=1,kpl
			if (i /= indeksi) then
				muutos(1,:) = muutos(1,:) + (massat(i) * ((r(1,:) - paikat(i,:)) / (vektoripituus(r(1,:) - paikat(i,:)))**3))
			end if
		end do
		
		muutos = muutos*(-(grav))
	end function nopeudenmuutos


	function rungekutta(r0,v0,t,paikat,massat,indeksi,kpl) result(a)	!funktio palauttaa tarvittavat kertoimet uuden paikan ja nopeuden laskemiseksi yhdelle kappaleelle
		implicit none
		double precision, dimension(:,:), intent(in) :: r0, v0, paikat
		double precision, intent(in) :: massat(:)
		double precision, intent(in) :: t
		integer, intent(in) :: indeksi, kpl
		integer :: i
		double precision :: a(8,1,3)
		double precision, dimension(1,3) :: k1r,k1v,k2r,k2v,k3r,k3v,k4r,k4v

		k1r = v0
		k1v = nopeudenmuutos(r0,paikat,massat,indeksi,kpl)

		k2r = (v0+dble(1)/dble(2)*t*k1v)
		k2v = nopeudenmuutos((r0+dble(1)/dble(2)*t*k1r),paikat,massat,indeksi,kpl)

		k3r = (v0+dble(1)/dble(2)*t*k2v)
		k3v = nopeudenmuutos((r0+dble(1)/dble(2)*t*k2r),paikat,massat,indeksi,kpl)

		k4r = (v0+t*k3v)
		k4v = nopeudenmuutos((r0+t*k3r),paikat,massat,indeksi,kpl)
		
		a(1,1,:) = k1r(1,:)
		a(2,1,:) = k1v(1,:)
		a(3,1,:) = k2r(1,:)
		a(4,1,:) = k2v(1,:)
		a(5,1,:) = k3r(1,:)
		a(6,1,:) = k3v(1,:)
		a(7,1,:) = k4r(1,:)
		a(8,1,:) = k4v(1,:)
	end function rungekutta


	function leapfrog(r0,v0,t,paikat,massat,indeksi,kpl) result(b)
		implicit none
		double precision, dimension(:,:), intent(in) :: r0, v0, paikat
		double precision, intent(in) :: massat(:)
		double precision, intent(in) :: t
		integer, intent(in) :: indeksi, kpl
		integer :: i
		double precision, dimension(1,3) :: r1, v11, v12
		double precision, dimension(6) :: b

		v11 = v0 + nopeudenmuutos(r0,paikat,massat,indeksi,kpl)*(t/dble(2))
		r1 = r0 + v11*t
		v12 = v11 + nopeudenmuutos(r1,paikat,massat,indeksi,kpl)*(t/dble(2))

		b(1:3) = r1(1,:)
		b(4:6) = v12(1,:)
	end function leapfrog
end module
