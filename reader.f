      subroutine readmesafile(filename,startline,numlines,columns,dat)
      character(len=30), intent(in) :: filename
      integer, intent(in) :: startline, numlines, columns
      real(8), intent(out), dimension(numlines,columns) :: dat
      
      open(1,file=filename,status='old')
      do i=1,startline-1
            read(1,*)
      end do
      do i=1,numlines
            read(1,*) (dat(i,j), j=1,columns)
      end do
      close(1)

      end subroutine readmesafile


