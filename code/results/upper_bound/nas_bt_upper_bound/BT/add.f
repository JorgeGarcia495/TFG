c---------------------------------------------------------------------
c---------------------------------------------------------------------

      subroutine  add

c---------------------------------------------------------------------
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c     addition of update to the vector u
c---------------------------------------------------------------------

      include 'header.h'

      integer i, j, k, m

      if (timeron) call timer_start(t_add)
              PRINT *,"Loop entry",1,18,":", 1, grid_points(3)-2
      do     k = 1, grid_points(3)-2
                 PRINT *,"Loop entry",2,19,":", 1, grid_points(2)-2
         do     j = 1, grid_points(2)-2
                    PRINT *,"Loop entry",3,20,":", 1, grid_points(1)-2
            do     i = 1, grid_points(1)-2
                      PRINT *,"Loop entry",4,21,":", 1, 5
               do    m = 1, 5
                  u(m,i,j,k) = u(m,i,j,k) + rhs(m,i,j,k)
                 EXIT
               enddo
               PRINT *,"Loop exit",4,23
              EXIT
            enddo
            PRINT *,"Loop exit",3,24
           EXIT
         enddo
         PRINT *,"Loop exit",2,25
        EXIT
      enddo
      PRINT *,"Loop exit",1,26
      if (timeron) call timer_stop(t_add)

      return
      end
