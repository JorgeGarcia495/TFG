c---------------------------------------------------------------------
c---------------------------------------------------------------------

      subroutine compute_rhs

c---------------------------------------------------------------------
c---------------------------------------------------------------------

      include 'header.h'

      integer i, j, k, m
      double precision rho_inv, uijk, up1, um1, vijk, vp1, vm1,
     >     wijk, wp1, wm1


      if (timeron) call timer_start(t_rhs)
c---------------------------------------------------------------------
c     compute the reciprocal of density, and the kinetic energy, 
c     and the speed of sound.
c---------------------------------------------------------------------
          PRINT *,"Loop entry",1,21,":", 0, grid_points(3)-1
      do k = 0, grid_points(3)-1
             PRINT *,"Loop entry",2,22,":", 0, grid_points(2)-1
         do j = 0, grid_points(2)-1
                PRINT *,"Loop entry",3,23,":", 0, grid_points(1)-1
            do i = 0, grid_points(1)-1
               rho_inv = 1.0d0/u(1,i,j,k)
               rho_i(i,j,k) = rho_inv
               us(i,j,k) = u(2,i,j,k) * rho_inv
               vs(i,j,k) = u(3,i,j,k) * rho_inv
               ws(i,j,k) = u(4,i,j,k) * rho_inv
               square(i,j,k)     = 0.5d0* (
     >                 u(2,i,j,k)*u(2,i,j,k) + 
     >                 u(3,i,j,k)*u(3,i,j,k) +
     >                 u(4,i,j,k)*u(4,i,j,k) ) * rho_inv
               qs(i,j,k) = square(i,j,k) * rho_inv
              EXIT
            enddo
            PRINT *,"Loop exit",3,34
           EXIT
         enddo
         PRINT *,"Loop exit",2,35
        EXIT
      enddo
      PRINT *,"Loop exit",1,36

c---------------------------------------------------------------------
c copy the exact forcing term to the right hand side;  because 
c this forcing term is known, we can store it on the whole grid
c including the boundary                   
c---------------------------------------------------------------------

          PRINT *,"Loop entry",1,44,":", 0, grid_points(3)-1
      do k = 0, grid_points(3)-1
             PRINT *,"Loop entry",2,45,":", 0, grid_points(2)-1
         do j = 0, grid_points(2)-1
                PRINT *,"Loop entry",3,46,":", 0, grid_points(1)-1
            do i = 0, grid_points(1)-1
                   PRINT *,"Loop entry",4,47,":", 1, 5
               do m = 1, 5
                  rhs(m,i,j,k) = forcing(m,i,j,k)
                 EXIT
               enddo
               PRINT *,"Loop exit",4,49
              EXIT
            enddo
            PRINT *,"Loop exit",3,50
           EXIT
         enddo
         PRINT *,"Loop exit",2,51
        EXIT
      enddo
      PRINT *,"Loop exit",1,52


      if (timeron) call timer_start(t_rhsx)
c---------------------------------------------------------------------
c     compute xi-direction fluxes 
c---------------------------------------------------------------------
          PRINT *,"Loop entry",1,59,":", 1, grid_points(3)-2
      do k = 1, grid_points(3)-2
             PRINT *,"Loop entry",2,60,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
                PRINT *,"Loop entry",3,61,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2
               uijk = us(i,j,k)
               up1  = us(i+1,j,k)
               um1  = us(i-1,j,k)

               rhs(1,i,j,k) = rhs(1,i,j,k) + dx1tx1 * 
     >                 (u(1,i+1,j,k) - 2.0d0*u(1,i,j,k) + 
     >                 u(1,i-1,j,k)) -
     >                 tx2 * (u(2,i+1,j,k) - u(2,i-1,j,k))

               rhs(2,i,j,k) = rhs(2,i,j,k) + dx2tx1 * 
     >                 (u(2,i+1,j,k) - 2.0d0*u(2,i,j,k) + 
     >                 u(2,i-1,j,k)) +
     >                 xxcon2*con43 * (up1 - 2.0d0*uijk + um1) -
     >                 tx2 * (u(2,i+1,j,k)*up1 - 
     >                 u(2,i-1,j,k)*um1 +
     >                 (u(5,i+1,j,k)- square(i+1,j,k)-
     >                 u(5,i-1,j,k)+ square(i-1,j,k))*
     >                 c2)

               rhs(3,i,j,k) = rhs(3,i,j,k) + dx3tx1 * 
     >                 (u(3,i+1,j,k) - 2.0d0*u(3,i,j,k) +
     >                 u(3,i-1,j,k)) +
     >                 xxcon2 * (vs(i+1,j,k) - 2.0d0*vs(i,j,k) +
     >                 vs(i-1,j,k)) -
     >                 tx2 * (u(3,i+1,j,k)*up1 - 
     >                 u(3,i-1,j,k)*um1)

               rhs(4,i,j,k) = rhs(4,i,j,k) + dx4tx1 * 
     >                 (u(4,i+1,j,k) - 2.0d0*u(4,i,j,k) +
     >                 u(4,i-1,j,k)) +
     >                 xxcon2 * (ws(i+1,j,k) - 2.0d0*ws(i,j,k) +
     >                 ws(i-1,j,k)) -
     >                 tx2 * (u(4,i+1,j,k)*up1 - 
     >                 u(4,i-1,j,k)*um1)

               rhs(5,i,j,k) = rhs(5,i,j,k) + dx5tx1 * 
     >                 (u(5,i+1,j,k) - 2.0d0*u(5,i,j,k) +
     >                 u(5,i-1,j,k)) +
     >                 xxcon3 * (qs(i+1,j,k) - 2.0d0*qs(i,j,k) +
     >                 qs(i-1,j,k)) +
     >                 xxcon4 * (up1*up1 -       2.0d0*uijk*uijk + 
     >                 um1*um1) +
     >                 xxcon5 * (u(5,i+1,j,k)*rho_i(i+1,j,k) - 
     >                 2.0d0*u(5,i,j,k)*rho_i(i,j,k) +
     >                 u(5,i-1,j,k)*rho_i(i-1,j,k)) -
     >                 tx2 * ( (c1*u(5,i+1,j,k) - 
     >                 c2*square(i+1,j,k))*up1 -
     >                 (c1*u(5,i-1,j,k) - 
     >                 c2*square(i-1,j,k))*um1 )
              EXIT
            enddo
            PRINT *,"Loop exit",3,111
           EXIT
         enddo
         PRINT *,"Loop exit",2,112

c---------------------------------------------------------------------
c     add fourth order xi-direction dissipation               
c---------------------------------------------------------------------
             PRINT *,"Loop entry",2,117,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
            i = 1
                PRINT *,"Loop entry",3,119,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k)- dssp * 
     >                    ( 5.0d0*u(m,i,j,k) - 4.0d0*u(m,i+1,j,k) +
     >                    u(m,i+2,j,k))
              EXIT
            enddo
            PRINT *,"Loop exit",3,123

            i = 2
                PRINT *,"Loop entry",3,126,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k) - dssp * 
     >                    (-4.0d0*u(m,i-1,j,k) + 6.0d0*u(m,i,j,k) -
     >                    4.0d0*u(m,i+1,j,k) + u(m,i+2,j,k))
              EXIT
            enddo
            PRINT *,"Loop exit",3,130
           EXIT
         enddo
         PRINT *,"Loop exit",2,131

             PRINT *,"Loop entry",2,133,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
               PRINT *,"Loop entry",3,134,":", 3,grid_points(1)-4
            do i = 3,grid_points(1)-4
                   PRINT *,"Loop entry",4,135,":", 1, 5
               do m = 1, 5
                  rhs(m,i,j,k) = rhs(m,i,j,k) - dssp * 
     >                    (  u(m,i-2,j,k) - 4.0d0*u(m,i-1,j,k) + 
     >                    6.0*u(m,i,j,k) - 4.0d0*u(m,i+1,j,k) + 
     >                    u(m,i+2,j,k) )
                 EXIT
               enddo
               PRINT *,"Loop exit",4,140
              EXIT
            enddo
            PRINT *,"Loop exit",3,141
           EXIT
         enddo
         PRINT *,"Loop exit",2,142
         
             PRINT *,"Loop entry",2,144,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
            i = grid_points(1)-3
                PRINT *,"Loop entry",3,146,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k) - dssp *
     >                    ( u(m,i-2,j,k) - 4.0d0*u(m,i-1,j,k) + 
     >                    6.0d0*u(m,i,j,k) - 4.0d0*u(m,i+1,j,k) )
              EXIT
            enddo
            PRINT *,"Loop exit",3,150

            i = grid_points(1)-2
                PRINT *,"Loop entry",3,153,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k) - dssp *
     >                    ( u(m,i-2,j,k) - 4.d0*u(m,i-1,j,k) +
     >                    5.d0*u(m,i,j,k) )
              EXIT
            enddo
            PRINT *,"Loop exit",3,157
           EXIT
         enddo
         PRINT *,"Loop exit",2,158
        EXIT
      enddo
      PRINT *,"Loop exit",1,159
      if (timeron) call timer_stop(t_rhsx)

      if (timeron) call timer_start(t_rhsy)
c---------------------------------------------------------------------
c     compute eta-direction fluxes 
c---------------------------------------------------------------------
          PRINT *,"Loop entry",1,166,":", 1, grid_points(3)-2
      do k = 1, grid_points(3)-2
             PRINT *,"Loop entry",2,167,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
                PRINT *,"Loop entry",3,168,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2
               vijk = vs(i,j,k)
               vp1  = vs(i,j+1,k)
               vm1  = vs(i,j-1,k)
               rhs(1,i,j,k) = rhs(1,i,j,k) + dy1ty1 * 
     >                 (u(1,i,j+1,k) - 2.0d0*u(1,i,j,k) + 
     >                 u(1,i,j-1,k)) -
     >                 ty2 * (u(3,i,j+1,k) - u(3,i,j-1,k))
               rhs(2,i,j,k) = rhs(2,i,j,k) + dy2ty1 * 
     >                 (u(2,i,j+1,k) - 2.0d0*u(2,i,j,k) + 
     >                 u(2,i,j-1,k)) +
     >                 yycon2 * (us(i,j+1,k) - 2.0d0*us(i,j,k) + 
     >                 us(i,j-1,k)) -
     >                 ty2 * (u(2,i,j+1,k)*vp1 - 
     >                 u(2,i,j-1,k)*vm1)
               rhs(3,i,j,k) = rhs(3,i,j,k) + dy3ty1 * 
     >                 (u(3,i,j+1,k) - 2.0d0*u(3,i,j,k) + 
     >                 u(3,i,j-1,k)) +
     >                 yycon2*con43 * (vp1 - 2.0d0*vijk + vm1) -
     >                 ty2 * (u(3,i,j+1,k)*vp1 - 
     >                 u(3,i,j-1,k)*vm1 +
     >                 (u(5,i,j+1,k) - square(i,j+1,k) - 
     >                 u(5,i,j-1,k) + square(i,j-1,k))
     >                 *c2)
               rhs(4,i,j,k) = rhs(4,i,j,k) + dy4ty1 * 
     >                 (u(4,i,j+1,k) - 2.0d0*u(4,i,j,k) + 
     >                 u(4,i,j-1,k)) +
     >                 yycon2 * (ws(i,j+1,k) - 2.0d0*ws(i,j,k) + 
     >                 ws(i,j-1,k)) -
     >                 ty2 * (u(4,i,j+1,k)*vp1 - 
     >                 u(4,i,j-1,k)*vm1)
               rhs(5,i,j,k) = rhs(5,i,j,k) + dy5ty1 * 
     >                 (u(5,i,j+1,k) - 2.0d0*u(5,i,j,k) + 
     >                 u(5,i,j-1,k)) +
     >                 yycon3 * (qs(i,j+1,k) - 2.0d0*qs(i,j,k) + 
     >                 qs(i,j-1,k)) +
     >                 yycon4 * (vp1*vp1       - 2.0d0*vijk*vijk + 
     >                 vm1*vm1) +
     >                 yycon5 * (u(5,i,j+1,k)*rho_i(i,j+1,k) - 
     >                 2.0d0*u(5,i,j,k)*rho_i(i,j,k) +
     >                 u(5,i,j-1,k)*rho_i(i,j-1,k)) -
     >                 ty2 * ((c1*u(5,i,j+1,k) - 
     >                 c2*square(i,j+1,k)) * vp1 -
     >                 (c1*u(5,i,j-1,k) - 
     >                 c2*square(i,j-1,k)) * vm1)
              EXIT
            enddo
            PRINT *,"Loop exit",3,213
           EXIT
         enddo
         PRINT *,"Loop exit",2,214

c---------------------------------------------------------------------
c     add fourth order eta-direction dissipation         
c---------------------------------------------------------------------
         j = 1
             PRINT *,"Loop entry",2,220,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
                PRINT *,"Loop entry",3,221,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k)- dssp * 
     >                    ( 5.0d0*u(m,i,j,k) - 4.0d0*u(m,i,j+1,k) +
     >                    u(m,i,j+2,k))
              EXIT
            enddo
            PRINT *,"Loop exit",3,225
           EXIT
         enddo
         PRINT *,"Loop exit",2,226

         j = 2
             PRINT *,"Loop entry",2,229,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
                PRINT *,"Loop entry",3,230,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k) - dssp * 
     >                    (-4.0d0*u(m,i,j-1,k) + 6.0d0*u(m,i,j,k) -
     >                    4.0d0*u(m,i,j+1,k) + u(m,i,j+2,k))
              EXIT
            enddo
            PRINT *,"Loop exit",3,234
           EXIT
         enddo
         PRINT *,"Loop exit",2,235

             PRINT *,"Loop entry",2,237,":", 3, grid_points(2)-4
         do j = 3, grid_points(2)-4
               PRINT *,"Loop entry",3,238,":", 1,grid_points(1)-2
            do i = 1,grid_points(1)-2
                   PRINT *,"Loop entry",4,239,":", 1, 5
               do m = 1, 5
                  rhs(m,i,j,k) = rhs(m,i,j,k) - dssp * 
     >                    (  u(m,i,j-2,k) - 4.0d0*u(m,i,j-1,k) + 
     >                    6.0*u(m,i,j,k) - 4.0d0*u(m,i,j+1,k) + 
     >                    u(m,i,j+2,k) )
                 EXIT
               enddo
               PRINT *,"Loop exit",4,244
              EXIT
            enddo
            PRINT *,"Loop exit",3,245
           EXIT
         enddo
         PRINT *,"Loop exit",2,246
         
         j = grid_points(2)-3
             PRINT *,"Loop entry",2,249,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
                PRINT *,"Loop entry",3,250,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k) - dssp *
     >                    ( u(m,i,j-2,k) - 4.0d0*u(m,i,j-1,k) + 
     >                    6.0d0*u(m,i,j,k) - 4.0d0*u(m,i,j+1,k) )
              EXIT
            enddo
            PRINT *,"Loop exit",3,254
           EXIT
         enddo
         PRINT *,"Loop exit",2,255

         j = grid_points(2)-2
             PRINT *,"Loop entry",2,258,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
                PRINT *,"Loop entry",3,259,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k) - dssp *
     >                    ( u(m,i,j-2,k) - 4.d0*u(m,i,j-1,k) +
     >                    5.d0*u(m,i,j,k) )
              EXIT
            enddo
            PRINT *,"Loop exit",3,263
           EXIT
         enddo
         PRINT *,"Loop exit",2,264
        EXIT
      enddo
      PRINT *,"Loop exit",1,265
      if (timeron) call timer_stop(t_rhsy)

      if (timeron) call timer_start(t_rhsz)
c---------------------------------------------------------------------
c     compute zeta-direction fluxes 
c---------------------------------------------------------------------
          PRINT *,"Loop entry",1,272,":", 1, grid_points(3)-2
      do k = 1, grid_points(3)-2
             PRINT *,"Loop entry",2,273,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
                PRINT *,"Loop entry",3,274,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2
               wijk = ws(i,j,k)
               wp1  = ws(i,j,k+1)
               wm1  = ws(i,j,k-1)

               rhs(1,i,j,k) = rhs(1,i,j,k) + dz1tz1 * 
     >                 (u(1,i,j,k+1) - 2.0d0*u(1,i,j,k) + 
     >                 u(1,i,j,k-1)) -
     >                 tz2 * (u(4,i,j,k+1) - u(4,i,j,k-1))
               rhs(2,i,j,k) = rhs(2,i,j,k) + dz2tz1 * 
     >                 (u(2,i,j,k+1) - 2.0d0*u(2,i,j,k) + 
     >                 u(2,i,j,k-1)) +
     >                 zzcon2 * (us(i,j,k+1) - 2.0d0*us(i,j,k) + 
     >                 us(i,j,k-1)) -
     >                 tz2 * (u(2,i,j,k+1)*wp1 - 
     >                 u(2,i,j,k-1)*wm1)
               rhs(3,i,j,k) = rhs(3,i,j,k) + dz3tz1 * 
     >                 (u(3,i,j,k+1) - 2.0d0*u(3,i,j,k) + 
     >                 u(3,i,j,k-1)) +
     >                 zzcon2 * (vs(i,j,k+1) - 2.0d0*vs(i,j,k) + 
     >                 vs(i,j,k-1)) -
     >                 tz2 * (u(3,i,j,k+1)*wp1 - 
     >                 u(3,i,j,k-1)*wm1)
               rhs(4,i,j,k) = rhs(4,i,j,k) + dz4tz1 * 
     >                 (u(4,i,j,k+1) - 2.0d0*u(4,i,j,k) + 
     >                 u(4,i,j,k-1)) +
     >                 zzcon2*con43 * (wp1 - 2.0d0*wijk + wm1) -
     >                 tz2 * (u(4,i,j,k+1)*wp1 - 
     >                 u(4,i,j,k-1)*wm1 +
     >                 (u(5,i,j,k+1) - square(i,j,k+1) - 
     >                 u(5,i,j,k-1) + square(i,j,k-1))
     >                 *c2)
               rhs(5,i,j,k) = rhs(5,i,j,k) + dz5tz1 * 
     >                 (u(5,i,j,k+1) - 2.0d0*u(5,i,j,k) + 
     >                 u(5,i,j,k-1)) +
     >                 zzcon3 * (qs(i,j,k+1) - 2.0d0*qs(i,j,k) + 
     >                 qs(i,j,k-1)) +
     >                 zzcon4 * (wp1*wp1 - 2.0d0*wijk*wijk + 
     >                 wm1*wm1) +
     >                 zzcon5 * (u(5,i,j,k+1)*rho_i(i,j,k+1) - 
     >                 2.0d0*u(5,i,j,k)*rho_i(i,j,k) +
     >                 u(5,i,j,k-1)*rho_i(i,j,k-1)) -
     >                 tz2 * ( (c1*u(5,i,j,k+1) - 
     >                 c2*square(i,j,k+1))*wp1 -
     >                 (c1*u(5,i,j,k-1) - 
     >                 c2*square(i,j,k-1))*wm1)
              EXIT
            enddo
            PRINT *,"Loop exit",3,320
           EXIT
         enddo
         PRINT *,"Loop exit",2,321
        EXIT
      enddo
      PRINT *,"Loop exit",1,322

c---------------------------------------------------------------------
c     add fourth order zeta-direction dissipation                
c---------------------------------------------------------------------
      k = 1
          PRINT *,"Loop entry",1,328,":", 1, grid_points(2)-2
      do j = 1, grid_points(2)-2
             PRINT *,"Loop entry",2,329,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
                PRINT *,"Loop entry",3,330,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k)- dssp * 
     >                    ( 5.0d0*u(m,i,j,k) - 4.0d0*u(m,i,j,k+1) +
     >                    u(m,i,j,k+2))
              EXIT
            enddo
            PRINT *,"Loop exit",3,334
           EXIT
         enddo
         PRINT *,"Loop exit",2,335
        EXIT
      enddo
      PRINT *,"Loop exit",1,336

      k = 2
          PRINT *,"Loop entry",1,339,":", 1, grid_points(2)-2
      do j = 1, grid_points(2)-2
             PRINT *,"Loop entry",2,340,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
                PRINT *,"Loop entry",3,341,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k) - dssp * 
     >                    (-4.0d0*u(m,i,j,k-1) + 6.0d0*u(m,i,j,k) -
     >                    4.0d0*u(m,i,j,k+1) + u(m,i,j,k+2))
              EXIT
            enddo
            PRINT *,"Loop exit",3,345
           EXIT
         enddo
         PRINT *,"Loop exit",2,346
        EXIT
      enddo
      PRINT *,"Loop exit",1,347

          PRINT *,"Loop entry",1,349,":", 3, grid_points(3)-4
      do k = 3, grid_points(3)-4
             PRINT *,"Loop entry",2,350,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
               PRINT *,"Loop entry",3,351,":", 1,grid_points(1)-2
            do i = 1,grid_points(1)-2
                   PRINT *,"Loop entry",4,352,":", 1, 5
               do m = 1, 5
                  rhs(m,i,j,k) = rhs(m,i,j,k) - dssp * 
     >                    (  u(m,i,j,k-2) - 4.0d0*u(m,i,j,k-1) + 
     >                    6.0*u(m,i,j,k) - 4.0d0*u(m,i,j,k+1) + 
     >                    u(m,i,j,k+2) )
                 EXIT
               enddo
               PRINT *,"Loop exit",4,357
              EXIT
            enddo
            PRINT *,"Loop exit",3,358
           EXIT
         enddo
         PRINT *,"Loop exit",2,359
        EXIT
      enddo
      PRINT *,"Loop exit",1,360
         
      k = grid_points(3)-3
          PRINT *,"Loop entry",1,363,":", 1, grid_points(2)-2
      do j = 1, grid_points(2)-2
             PRINT *,"Loop entry",2,364,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
                PRINT *,"Loop entry",3,365,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k) - dssp *
     >                    ( u(m,i,j,k-2) - 4.0d0*u(m,i,j,k-1) + 
     >                    6.0d0*u(m,i,j,k) - 4.0d0*u(m,i,j,k+1) )
              EXIT
            enddo
            PRINT *,"Loop exit",3,369
           EXIT
         enddo
         PRINT *,"Loop exit",2,370
        EXIT
      enddo
      PRINT *,"Loop exit",1,371

      k = grid_points(3)-2
          PRINT *,"Loop entry",1,374,":", 1, grid_points(2)-2
      do j = 1, grid_points(2)-2
             PRINT *,"Loop entry",2,375,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
                PRINT *,"Loop entry",3,376,":", 1, 5
            do m = 1, 5
               rhs(m,i,j,k) = rhs(m,i,j,k) - dssp *
     >                    ( u(m,i,j,k-2) - 4.d0*u(m,i,j,k-1) +
     >                    5.d0*u(m,i,j,k) )
              EXIT
            enddo
            PRINT *,"Loop exit",3,380
           EXIT
         enddo
         PRINT *,"Loop exit",2,381
        EXIT
      enddo
      PRINT *,"Loop exit",1,382
      if (timeron) call timer_stop(t_rhsz)

          PRINT *,"Loop entry",1,385,":", 1, grid_points(3)-2
      do k = 1, grid_points(3)-2
             PRINT *,"Loop entry",2,386,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
                PRINT *,"Loop entry",3,387,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2
                   PRINT *,"Loop entry",4,388,":", 1, 5
               do m = 1, 5
                  rhs(m,i,j,k) = rhs(m,i,j,k) * dt
                 EXIT
               enddo
               PRINT *,"Loop exit",4,390
              EXIT
            enddo
            PRINT *,"Loop exit",3,391
           EXIT
         enddo
         PRINT *,"Loop exit",2,392
        EXIT
      enddo
      PRINT *,"Loop exit",1,393
      if (timeron) call timer_stop(t_rhs)

      return
      end




