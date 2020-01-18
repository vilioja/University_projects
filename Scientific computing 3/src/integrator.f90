program integrator
	use functions
	implicit none
	integer :: pcs				!how many items are we simulating
	integer :: ios, x, i, j		!iostat for reading files, x, i and j are auxiliary variables
	integer :: record			!this tells us how many of the simulated locations are saved, every record:th point is saved
	integer :: indx				!this tells us the index of the line of the current matrix, ie. which object is being handled
	real(kind=8) :: tinterval	!this tells us how long the system will be simulated
	real(kind=8) :: timestep	!timestep tells the length of the time step
	real(kind=8) :: time		!time tells us the current time (starts at 0), it's used to see when to stop
	real(kind=8) :: pi			!pi

	real(kind=8), allocatable :: places(:,:), velocities(:,:), masses(:)		!these are used to store data
	real(kind=8), allocatable :: newplaces(:,:), newvelocities(:,:)		!temporary storages for new data
	character(len=999) :: line										!this is used for writing and reading
	character(len=80) :: arg, inputfile, outputfile					!arg is used to read command line arguments, inputfile and outputfile are the input and output files, respectively
	real(kind=8) :: b(6)								!list of the results of the leapfrog function
	real(kind=8) :: r0(1,3),v0(1,3),r1(1,3),v1(1,3)		!auxiliary variables for writing new places and velocities

!--------------------------------------------------------------------------------

	call get_command_argument(1,inputfile)		!read inputfile and outputfile from command line
	call get_command_argument(2,outputfile)
	
	pcs = 0
	open(unit=1,file=trim(inputfile),status='old')	!read the number of objects to be simulated by looking at the amout of lines

	do
		read(1,'(A)',iostat=ios) line	!read one line at a time
		if(ios /= 0) exit				!if the file ends, quit
		if (index(line,"#") == 0) then	!if there is no #-sign to indicate a comment line, raise the amount of objects
			pcs = pcs + 1
		end if
	end do

	close(1)
	
	
!-------define constants and variables--------

	call get_command_argument(3,arg)	!read how long the simulation will be run, in whole orbits
	read(arg,*) tinterval
	call get_command_argument(4,arg)	!how often the data will be saved
	read(arg,*) record
	call get_command_argument(5,arg)	!timestep length
	read(arg,*) timestep

	pi = 4*atan(1.)
	tinterval = 2*pi*tinterval
	indx = 1
	time = 0
	
	allocate(places(pcs,3))
	allocate(velocities(pcs,3))
	allocate(masses(pcs))

	allocate(newplaces(pcs,3))
	allocate(newvelocities(pcs,3))



!-------read the initial data

	open(unit=1,file=trim(inputfile),status='old')

	do
		read(1,'(A)',iostat=ios) line	!read one line at a time
		if(ios /= 0) exit				!if the file ends, quit
		if (index(line,"#") == 0) then	!if there is no #-sign to indicate a comment line, raise the amount of objects
			line = trim(line)
			read(line,*) places(indx,:), velocities(indx,:), masses(indx)
			indx = indx + 1
		end if
	end do

	close(1)

!-------calculate new values and write them into a file

	open(unit=1,file=trim(outputfile),status='replace')

	line = ""

	do i=1,pcs										!write down the masses, the time step and the saving interval
		write(arg,*) masses(i)
		line = trim(line)//adjustl(trim(arg))
		line = trim(line)//','
		if (i == pcs) then
			write(arg,*) timestep
			line = trim(line)//adjustl(trim(arg))
			line = trim(line)//','
			write(arg,*) record
			line = trim(line)//adjustl(trim(arg))
		end if
	end do

	write(1,'(A)') trim(line)

	line = ""
	do i=1,pcs										!write the initial places and velocities
		do j=1,3
			write(arg,*) places(i,j)
			line = trim(line)//adjustl(trim(arg))
			line = trim(line)//','
		end do
		do j=1,3
			write(arg,*) velocities(i,j)
			line = trim(line)//adjustl(trim(arg))

			if (j /= 3) then
				line = trim(line)//','
			elseif (i /= pcs) then
				line = trim(line)//';'
			end if
		end do
	end do

	write(1,'(A)') trim(line)

	x = 1						!this is used to write down only every record:th calculation
	
	do while (time <= tinterval)
		do i=1,pcs
			indx = i
			r0(1,:) = places(i,:)
			v0(1,:) = velocities(i,:)
			b = leapfrog(r0,v0,timestep,places,masses,indx,pcs)
			newplaces(i,:) = b(1:3)
			newvelocities(i,:) = b(4:6)
		end do

		places = newplaces
		velocities = newvelocities
		if (modulo(x,record) == 0) then
			print*, x
			line = ""
			do i=1,pcs
				do j=1,3
					write(arg,*) places(i,j)
					line = trim(line)//adjustl(trim(arg))
					line = trim(line)//','
				end do
				do j=1,3
					write(arg,*) velocities(i,j)
					line = trim(line)//adjustl(trim(arg))

					if (j /= 3) then
						line = trim(line)//','
					elseif (i /= pcs) then
						line = trim(line)//';'
					end if
				end do
			end do
			write(1,'(A)') trim(line)
		end if
		
		time = time + timestep
		x = x + 1
	end do

	close(1)
end program integrator
