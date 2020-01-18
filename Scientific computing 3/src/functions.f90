module functions
	implicit none

contains

	function vectorlength(a) result(x)			!function for calculating the length of a vector
		implicit none
		real(kind=8), intent(in) :: a(1,3)
		real(kind=8) :: x
		
		x = sqrt(a(1,1)**2 + a(1,2)**2 + a(1,3)**2)
	end function vectorlength


	function deltav(r,places,masses,indx,pcs) result(change)	!function for calculating the change in velocity. sum up the effects of gravity on one particle
		implicit none
		real(kind=8), dimension(:,:), intent(in) :: r,places
		real(kind=8), intent(in) :: masses(:)
		integer, intent(in) :: indx, pcs
		real(kind=8), allocatable :: change(:,:)
		integer :: i, size1, size2

		size1 = size(r,1)
		size2 = size(r,2)
		allocate(change(size1,size2))
		change = 0

		do i=1,pcs
			if (i /= indx) then
				change(1,:) = change(1,:) + (masses(i) * ((r(1,:) - places(i,:)) / (vectorlength(r(1,:) - places(i,:)))**3))
			end if
		end do
		
		change(1,:) = change(1,:)*(-1)
	end function deltav

	function leapfrog(r0,v0,t,places,masses,indx,pcs) result(b)
		implicit none
		real(kind=8), dimension(:,:), intent(in) :: r0, v0, places
		real(kind=8), intent(in) :: masses(:)
		real(kind=8), intent(in) :: t
		integer, intent(in) :: indx, pcs
		integer :: i
		real(kind=8), dimension(1,3) :: r1, v11, v12
		real(kind=8), dimension(6) :: b

		v11 = v0 + deltav(r0,places,masses,indx,pcs)*(t/2)
		r1 = r0 + v11*t
		v12 = v11 + deltav(r1,places,masses,indx,pcs)*(t/2)

		b(1:3) = r1(1,:)
		b(4:6) = v12(1,:)
	end function leapfrog
end module
