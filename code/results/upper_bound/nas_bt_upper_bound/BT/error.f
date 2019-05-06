c---------------------------------------------------------------------
c---------------------------------------------------------------------

      subroutine error_norm(rms)

c---------------------------------------------------------------------
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c     this function computes the norm of the difference between the
c     computed solution and the exact solution
c---------------------------------------------------------------------

      include 'header.h'

      integer i, j, k, m, d
      double precision xi, eta, zeta, u_exact(5), rms(5), add

           PRINT *,"Loop entry",1,19,":", 1, 5
      do m = 1, 5 
         rms(m) = 0.0d0
        EXIT
      enddo
      PRINT *,"Loop exit",1,21

          PRINT *,"Loop entry",1,23,":", 0, grid_points(3)-1
      do k = 0, grid_points(3)-1
         zeta = dble(k) * dnzm1
             PRINT *,"Loop entry",2,25,":", 0, grid_points(2)-1
         do j = 0, grid_points(2)-1
            eta = dble(j) * dnym1
                PRINT *,"Loop entry",3,27,":", 0, grid_points(1)-1
            do i = 0, grid_points(1)-1
               xi = dble(i) * dnxm1
                   PRINT *,"Begin - exact_solution",29
               call exact_solution(xi, eta, zeta, u_exact)
                   PRINT *,"End - exact_solution",29

                   PRINT *,"Loop entry",4,31,":", 1, 5
               do m = 1, 5
                  add = u(m,i,j,k)-u_exact(m)
                  rms(m) = rms(m) + add*add
                 EXIT
               enddo
               PRINT *,"Loop exit",4,34
              EXIT
            enddo
            PRINT *,"Loop exit",3,35
            EXIT
          enddo
          PRINT *,"Loop exit",2,36
         EXIT
       enddo
       PRINT *,"Loop exit",1,37

          PRINT *,"Loop entry",1,39,":", 1, 5
      do m = 1, 5
             PRINT *,"Loop entry",2,40,":", 1, 3
         do d = 1, 3
            rms(m) = rms(m) / dble(grid_points(d)-2)
           EXIT
         enddo
         PRINT *,"Loop exit",2,42
         rms(m) = dsqrt(rms(m))
        EXIT
      enddo
      PRINT *,"Loop exit",1,44

      return
      end


c---------------------------------------------------------------------
c---------------------------------------------------------------------

      subroutine rhs_norm(rms)

c---------------------------------------------------------------------
c---------------------------------------------------------------------

      include 'header.h'

      integer i, j, k, d, m
      double precision rms(5), add

          PRINT *,"Loop entry",1,63,":", 1, 5
      do m = 1, 5
         rms(m) = 0.0d0
         EXIT
      enddo 
       PRINT *,"Loop exit",1,65

          PRINT *,"Loop entry",1,67,":", 1, grid_points(3)-2
      do k = 1, grid_points(3)-2
             PRINT *,"Loop entry",2,68,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
                PRINT *,"Loop entry",3,69,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2
                   PRINT *,"Loop entry",4,70,":", 1, 5
               do m = 1, 5
                  add = rhs(m,i,j,k)
                  rms(m) = rms(m) + add*add
                  EXIT
               enddo 
                PRINT *,"Loop exit",4,73
               EXIT
            enddo 
             PRINT *,"Loop exit",3,74
            EXIT
         enddo 
          PRINT *,"Loop exit",2,75
         EXIT
      enddo 
       PRINT *,"Loop exit",1,76

          PRINT *,"Loop entry",1,78,":", 1, 5
      do m = 1, 5
             PRINT *,"Loop entry",2,79,":", 1, 3
         do d = 1, 3
            rms(m) = rms(m) / dble(grid_points(d)-2)
            EXIT
         enddo 
          PRINT *,"Loop exit",2,81
         rms(m) = dsqrt(rms(m))
         EXIT
      enddo 
       PRINT *,"Loop exit",1,83

      return
      end

