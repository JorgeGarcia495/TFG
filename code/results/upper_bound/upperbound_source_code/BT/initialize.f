c---------------------------------------------------------------------
c---------------------------------------------------------------------

      subroutine  initialize

c---------------------------------------------------------------------
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c     This subroutine initializes the field variable u using 
c     tri-linear transfinite interpolation of the boundary values     
c---------------------------------------------------------------------

      include 'header.h'
      
      integer i, j, k, m, ix, iy, iz
      double precision  xi, eta, zeta, Pface(5,3,2), Pxi, Peta, 
     >     Pzeta, temp(5)

c---------------------------------------------------------------------
c  Later (in compute_rhs) we compute 1/u for every element. A few of 
c  the corner elements are not used, but it convenient (and faster) 
c  to compute the whole thing with a simple loop. Make sure those 
c  values are nonzero by initializing the whole thing here. 
c---------------------------------------------------------------------
          PRINT *,"Loop entry",1,26,":", 0, grid_points(3)-1
      do k = 0, grid_points(3)-1
             PRINT *,"Loop entry",2,27,":", 0, grid_points(2)-1
         do j = 0, grid_points(2)-1
                PRINT *,"Loop entry",3,28,":", 0, grid_points(1)-1
            do i = 0, grid_points(1)-1
                   PRINT *,"Loop entry",4,29,":", 1, 5
               do m = 1, 5
                  u(m,i,j,k) = 1.0
                  EXIT
               end do
                PRINT *,"Loop exit",4,31
               EXIT
            end do
             PRINT *,"Loop exit",3,32
            EXIT
         end do
          PRINT *,"Loop exit",2,33
         EXIT
      end do
       PRINT *,"Loop exit",1,34
c---------------------------------------------------------------------



c---------------------------------------------------------------------
c     first store the "interpolated" values everywhere on the grid    
c---------------------------------------------------------------------

          PRINT *,"Loop entry",1,43,":", 0, grid_points(3)-1
      do k = 0, grid_points(3)-1
         zeta = dble(k) * dnzm1
             PRINT *,"Loop entry",2,45,":", 0, grid_points(2)-1
         do j = 0, grid_points(2)-1
            eta = dble(j) * dnym1
                PRINT *,"Loop entry",3,47,":", 0, grid_points(1)-1
            do i = 0, grid_points(1)-1
               xi = dble(i) * dnxm1
                  
                   PRINT *,"Loop entry",4,50,":", 1, 2
               do ix = 1, 2
                      PRINT *,"Begin - exact_solution",51
                  call exact_solution(dble(ix-1), eta, zeta, 
     >                    Pface(1,1,ix))
                         PRINT *,"End - exact_solution",52
                 EXIT
               enddo
               PRINT *,"Loop exit",4,53

                   PRINT *,"Loop entry",4,55,":", 1, 2
               do iy = 1, 2
                       PRINT *,"Begin - exact_solution",56
                  call exact_solution(xi, dble(iy-1) , zeta, 
     >                    Pface(1,2,iy))
                         PRINT *,"End - exact_solution",57
                 EXIT
               enddo
               PRINT *,"Loop exit",4,58

                   PRINT *,"Loop entry",4,60,":", 1, 2
               do iz = 1, 2
                        PRINT *,"Begin - exact_solution",61
                  call exact_solution(xi, eta, dble(iz-1),   
     >                    Pface(1,3,iz))
                         PRINT *,"End - exact_solution",62
                 EXIT
               enddo
               PRINT *,"Loop exit",4,63

                   PRINT *,"Loop entry",4,65,":", 1, 5
               do m = 1, 5
                  Pxi   = xi   * Pface(m,1,2) + 
     >                    (1.0d0-xi)   * Pface(m,1,1)
                  Peta  = eta  * Pface(m,2,2) + 
     >                    (1.0d0-eta)  * Pface(m,2,1)
                  Pzeta = zeta * Pface(m,3,2) + 
     >                    (1.0d0-zeta) * Pface(m,3,1)
                     
                  u(m,i,j,k) = Pxi + Peta + Pzeta - 
     >                    Pxi*Peta - Pxi*Pzeta - Peta*Pzeta + 
     >                    Pxi*Peta*Pzeta

                 EXIT
               enddo
               PRINT *,"Loop exit",4,77
              EXIT
            enddo
            PRINT *,"Loop exit",3,78
           EXIT
         enddo
         PRINT *,"Loop exit",2,79
        EXIT
      enddo
      PRINT *,"Loop exit",1,80

c---------------------------------------------------------------------
c     now store the exact values on the boundaries        
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c     west face                                                  
c---------------------------------------------------------------------
      i = 0
      xi = 0.0d0
          PRINT *,"Loop entry",1,91,":", 0, grid_points(3)-1
      do k = 0, grid_points(3)-1
         zeta = dble(k) * dnzm1
             PRINT *,"Loop entry",2,93,":", 0, grid_points(2)-1
         do j = 0, grid_points(2)-1
            eta = dble(j) * dnym1
                PRINT *,"Begin - exact_solution",95
            call exact_solution(xi, eta, zeta, temp)
                PRINT *,"End - exact_solution",95
                PRINT *,"Loop entry",3,96,":", 1, 5
            do m = 1, 5
               u(m,i,j,k) = temp(m)
              EXIT
            enddo
            PRINT *,"Loop exit",3,98
           EXIT
         enddo
         PRINT *,"Loop exit",2,99
        EXIT
      enddo
      PRINT *,"Loop exit",1,100

c---------------------------------------------------------------------
c     east face                                                      
c---------------------------------------------------------------------

      i = grid_points(1)-1
      xi = 1.0d0
          PRINT *,"Loop entry",1,108,":", 0, grid_points(3)-1
      do k = 0, grid_points(3)-1
         zeta = dble(k) * dnzm1
             PRINT *,"Loop entry",2,110,":", 0, grid_points(2)-1
         do j = 0, grid_points(2)-1
            eta = dble(j) * dnym1
                PRINT *,"Begin - exact_solution",112
            call exact_solution(xi, eta, zeta, temp)
                PRINT *,"End - exact_solution",112
                PRINT *,"Loop entry",3,113,":", 1, 5
            do m = 1, 5
               u(m,i,j,k) = temp(m)
              EXIT
            enddo
            PRINT *,"Loop exit",3,115
           EXIT
         enddo
         PRINT *,"Loop exit",2,116
        EXIT
      enddo
      PRINT *,"Loop exit",1,117

c---------------------------------------------------------------------
c     south face                                                 
c---------------------------------------------------------------------
      j = 0
      eta = 0.0d0
          PRINT *,"Loop entry",1,124,":", 0, grid_points(3)-1
      do k = 0, grid_points(3)-1
         zeta = dble(k) * dnzm1
             PRINT *,"Loop entry",2,126,":", 0, grid_points(1)-1
         do i = 0, grid_points(1)-1
            xi = dble(i) * dnxm1
                PRINT *,"Begin - exact_solution",128
            call exact_solution(xi, eta, zeta, temp)
                PRINT *,"End - exact_solution",128
                PRINT *,"Loop entry",3,129,":", 1, 5
            do m = 1, 5
               u(m,i,j,k) = temp(m)
              EXIT
            enddo
            PRINT *,"Loop exit",3,131
           EXIT
         enddo
         PRINT *,"Loop exit",2,132
        EXIT
      enddo
      PRINT *,"Loop exit",1,133


c---------------------------------------------------------------------
c     north face                                    
c---------------------------------------------------------------------
      j = grid_points(2)-1
      eta = 1.0d0
          PRINT *,"Loop entry",1,141,":", 0, grid_points(3)-1
      do k = 0, grid_points(3)-1
         zeta = dble(k) * dnzm1
             PRINT *,"Loop entry",2,143,":", 0, grid_points(1)-1
         do i = 0, grid_points(1)-1
            xi = dble(i) * dnxm1
                PRINT *,"Begin - exact_solution",145
            call exact_solution(xi, eta, zeta, temp)
                PRINT *,"End - exact_solution",145
                PRINT *,"Loop entry",3,146,":", 1, 5
            do m = 1, 5
               u(m,i,j,k) = temp(m)
              EXIT
            enddo
            PRINT *,"Loop exit",3,148
           EXIT
         enddo
         PRINT *,"Loop exit",2,149
        EXIT
      enddo
      PRINT *,"Loop exit",1,150

c---------------------------------------------------------------------
c     bottom face                                       
c---------------------------------------------------------------------
      k = 0
      zeta = 0.0d0
          PRINT *,"Loop entry",1,157,":", 0, grid_points(2)-1
      do j = 0, grid_points(2)-1
         eta = dble(j) * dnym1
            PRINT *,"Loop entry",2,159,":",0, grid_points(1)-1
         do i =0, grid_points(1)-1
            xi = dble(i) *dnxm1
                PRINT *,"Begin - exact_solution",161
            call exact_solution(xi, eta, zeta, temp)
                PRINT *,"End - exact_solution",161
                PRINT *,"Loop entry",3,162,":", 1, 5
            do m = 1, 5
               u(m,i,j,k) = temp(m)
              EXIT
            enddo
            PRINT *,"Loop exit",3,164
           EXIT
         enddo
         PRINT *,"Loop exit",2,165
        EXIT
      enddo
      PRINT *,"Loop exit",1,166

c---------------------------------------------------------------------
c     top face     
c---------------------------------------------------------------------
      k = grid_points(3)-1
      zeta = 1.0d0
          PRINT *,"Loop entry",1,173,":", 0, grid_points(2)-1
      do j = 0, grid_points(2)-1
         eta = dble(j) * dnym1
            PRINT *,"Loop entry",2,175,":",0, grid_points(1)-1
         do i =0, grid_points(1)-1
            xi = dble(i) * dnxm1
                PRINT *,"Begin - exact_solution",177
            call exact_solution(xi, eta, zeta, temp)
                PRINT *,"End - exact_solution",177
                PRINT *,"Loop entry",3,178,":", 1, 5
            do m = 1, 5
               u(m,i,j,k) = temp(m)
              EXIT
            enddo
            PRINT *,"Loop exit",3,180
           EXIT
         enddo
         PRINT *,"Loop exit",2,181
        EXIT
      enddo
      PRINT *,"Loop exit",1,182

      return
      end


c---------------------------------------------------------------------
c---------------------------------------------------------------------

      subroutine lhsinit(lhs, size)
      implicit none
      integer size
      double precision lhs(5,5,3,0:size)

c---------------------------------------------------------------------
c---------------------------------------------------------------------

      integer i, m, n

      i = size
c---------------------------------------------------------------------
c     zero the whole left hand side for starters
c---------------------------------------------------------------------
          PRINT *,"Loop entry",1,205,":", 1, 5
      do m = 1, 5
             PRINT *,"Loop entry",2,206,":", 1, 5
         do n = 1, 5
            lhs(m,n,1,0) = 0.0d0
            lhs(m,n,2,0) = 0.0d0
            lhs(m,n,3,0) = 0.0d0
            lhs(m,n,1,i) = 0.0d0
            lhs(m,n,2,i) = 0.0d0
            lhs(m,n,3,i) = 0.0d0
           EXIT
         enddo
         PRINT *,"Loop exit",2,213
        EXIT
      enddo
      PRINT *,"Loop exit",1,214

c---------------------------------------------------------------------
c     next, set all diagonal values to 1. This is overkill, but convenient
c---------------------------------------------------------------------
          PRINT *,"Loop entry",1,219,":", 1, 5
      do m = 1, 5
         lhs(m,m,2,0) = 1.0d0
         lhs(m,m,2,i) = 1.0d0
        EXIT
      enddo
      PRINT *,"Loop exit",1,222

      return
      end



