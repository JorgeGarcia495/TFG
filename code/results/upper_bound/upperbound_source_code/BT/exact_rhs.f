
c---------------------------------------------------------------------
c---------------------------------------------------------------------

      subroutine exact_rhs

c---------------------------------------------------------------------
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c     compute the right hand side based on exact solution
c---------------------------------------------------------------------

      include 'header.h'

      double precision dtemp(5), xi, eta, zeta, dtpp
      integer m, i, j, k, ip1, im1, jp1, jm1, km1, kp1

c---------------------------------------------------------------------
c     initialize                                  
c---------------------------------------------------------------------
         PRINT *,"Loop entry",1,22,":", 0, grid_points(3)-1
      do k= 0, grid_points(3)-1
             PRINT *,"Loop entry",2,23,":", 0, grid_points(2)-1
         do j = 0, grid_points(2)-1
                PRINT *,"Loop entry",3,24,":", 0, grid_points(1)-1
            do i = 0, grid_points(1)-1
                   PRINT *,"Loop entry",4,25,":", 1, 5
               do m = 1, 5
                  forcing(m,i,j,k) = 0.0d0
                 EXIT
               enddo
               PRINT *,"Loop exit",4,27
              EXIT
            enddo
            PRINT *,"Loop exit",3,28
           EXIT
         enddo
         PRINT *,"Loop exit",2,29
        EXIT
      enddo
      PRINT *,"Loop exit",1,30

c---------------------------------------------------------------------
c     xi-direction flux differences                      
c---------------------------------------------------------------------
          PRINT *,"Loop entry",1,35,":", 1, grid_points(3)-2
      do k = 1, grid_points(3)-2
         zeta = dble(k) * dnzm1
             PRINT *,"Loop entry",2,37,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
            eta = dble(j) * dnym1

              PRINT *,"Loop entry",3,40,":",0, grid_points(1)-1
            do i=0, grid_points(1)-1
               xi = dble(i) * dnxm1

                   PRINT *,"Begin - exact_solution",43
               call exact_solution(xi, eta, zeta, dtemp)
                   PRINT *,"End - exact_solution",43
                   PRINT *,"Loop entry",4,44,":", 1, 5
               do m = 1, 5
                  ue(i,m) = dtemp(m)
                 EXIT
               enddo
               PRINT *,"Loop exit",4,46

               dtpp = 1.0d0 / dtemp(1)

                   PRINT *,"Loop entry",4,50,":", 2, 5
               do m = 2, 5
                  buf(i,m) = dtpp * dtemp(m)
                 EXIT
               enddo
               PRINT *,"Loop exit",4,52

               cuf(i)   = buf(i,2) * buf(i,2)
               buf(i,1) = cuf(i) + buf(i,3) * buf(i,3) + 
     >                 buf(i,4) * buf(i,4) 
               q(i) = 0.5d0*(buf(i,2)*ue(i,2) + buf(i,3)*ue(i,3) +
     >                 buf(i,4)*ue(i,4))

              EXIT
            enddo
            PRINT *,"Loop exit",3,60
               
                PRINT *,"Loop entry",3,62,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2
               im1 = i-1
               ip1 = i+1

               forcing(1,i,j,k) = forcing(1,i,j,k) -
     >                 tx2*( ue(ip1,2)-ue(im1,2) )+
     >                 dx1tx1*(ue(ip1,1)-2.0d0*ue(i,1)+ue(im1,1))

               forcing(2,i,j,k) = forcing(2,i,j,k) - tx2 * (
     >                 (ue(ip1,2)*buf(ip1,2)+c2*(ue(ip1,5)-q(ip1)))-
     >                 (ue(im1,2)*buf(im1,2)+c2*(ue(im1,5)-q(im1))))+
     >                 xxcon1*(buf(ip1,2)-2.0d0*buf(i,2)+buf(im1,2))+
     >                 dx2tx1*( ue(ip1,2)-2.0d0* ue(i,2)+ue(im1,2))

               forcing(3,i,j,k) = forcing(3,i,j,k) - tx2 * (
     >                 ue(ip1,3)*buf(ip1,2)-ue(im1,3)*buf(im1,2))+
     >                 xxcon2*(buf(ip1,3)-2.0d0*buf(i,3)+buf(im1,3))+
     >                 dx3tx1*( ue(ip1,3)-2.0d0*ue(i,3) +ue(im1,3))
                  
               forcing(4,i,j,k) = forcing(4,i,j,k) - tx2*(
     >                 ue(ip1,4)*buf(ip1,2)-ue(im1,4)*buf(im1,2))+
     >                 xxcon2*(buf(ip1,4)-2.0d0*buf(i,4)+buf(im1,4))+
     >                 dx4tx1*( ue(ip1,4)-2.0d0* ue(i,4)+ ue(im1,4))

               forcing(5,i,j,k) = forcing(5,i,j,k) - tx2*(
     >                 buf(ip1,2)*(c1*ue(ip1,5)-c2*q(ip1))-
     >                 buf(im1,2)*(c1*ue(im1,5)-c2*q(im1)))+
     >                 0.5d0*xxcon3*(buf(ip1,1)-2.0d0*buf(i,1)+
     >                 buf(im1,1))+
     >                 xxcon4*(cuf(ip1)-2.0d0*cuf(i)+cuf(im1))+
     >                 xxcon5*(buf(ip1,5)-2.0d0*buf(i,5)+buf(im1,5))+
     >                 dx5tx1*( ue(ip1,5)-2.0d0* ue(i,5)+ ue(im1,5))
              EXIT
            enddo
            PRINT *,"Loop exit",3,94

c---------------------------------------------------------------------
c     Fourth-order dissipation                         
c---------------------------------------------------------------------

                PRINT *,"Loop entry",3,100,":", 1, 5
            do m = 1, 5
               i = 1
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (5.0d0*ue(i,m) - 4.0d0*ue(i+1,m) +ue(i+2,m))
               i = 2
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (-4.0d0*ue(i-1,m) + 6.0d0*ue(i,m) -
     >                    4.0d0*ue(i+1,m) +       ue(i+2,m))
              EXIT
            enddo
            PRINT *,"Loop exit",3,108

                PRINT *,"Loop entry",3,110,":", 3, grid_points(1)-4
            do i = 3, grid_points(1)-4
                   PRINT *,"Loop entry",4,111,":", 1, 5
               do m = 1, 5
                  forcing(m,i,j,k) = forcing(m,i,j,k) - dssp*
     >                    (ue(i-2,m) - 4.0d0*ue(i-1,m) +
     >                    6.0d0*ue(i,m) - 4.0d0*ue(i+1,m) + ue(i+2,m))
                 EXIT
               enddo
               PRINT *,"Loop exit",4,115
              EXIT
            enddo
            PRINT *,"Loop exit",3,116

                PRINT *,"Loop entry",3,118,":", 1, 5
            do m = 1, 5
               i = grid_points(1)-3
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (ue(i-2,m) - 4.0d0*ue(i-1,m) +
     >                    6.0d0*ue(i,m) - 4.0d0*ue(i+1,m))
               i = grid_points(1)-2
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (ue(i-2,m) - 4.0d0*ue(i-1,m) + 5.0d0*ue(i,m))
              EXIT
            enddo
            PRINT *,"Loop exit",3,126

           EXIT
         enddo
         PRINT *,"Loop exit",2,128
        EXIT
      enddo
      PRINT *,"Loop exit",1,129

c---------------------------------------------------------------------
c     eta-direction flux differences             
c---------------------------------------------------------------------
                    PRINT *,"Loop entry",1,134,":", 1, grid_points(3)-2
      do k = 1, grid_points(3)-2          
         zeta = dble(k) * dnzm1
           PRINT *,"Loop entry",2,136,":",1, grid_points(1)-2
         do i=1, grid_points(1)-2
            xi = dble(i) * dnxm1

              PRINT *,"Loop entry",3,139,":",0, grid_points(2)-1
            do j=0, grid_points(2)-1
               eta = dble(j) * dnym1

                   PRINT *,"Begin - exact_solution",142
               call exact_solution(xi, eta, zeta, dtemp)
                   PRINT *,"End - exact_solution",142
                    PRINT *,"Loop entry",4,143,":", 1, 5
               do m = 1, 5 
                  ue(j,m) = dtemp(m)
                 EXIT
               enddo
               PRINT *,"Loop exit",4,145
                  
               dtpp = 1.0d0/dtemp(1)

                   PRINT *,"Loop entry",4,149,":", 2, 5
               do m = 2, 5
                  buf(j,m) = dtpp * dtemp(m)
                 EXIT
               enddo
               PRINT *,"Loop exit",4,151

               cuf(j)   = buf(j,3) * buf(j,3)
               buf(j,1) = cuf(j) + buf(j,2) * buf(j,2) + 
     >                 buf(j,4) * buf(j,4)
               q(j) = 0.5d0*(buf(j,2)*ue(j,2) + buf(j,3)*ue(j,3) +
     >                 buf(j,4)*ue(j,4))
              EXIT
            enddo
            PRINT *,"Loop exit",3,158

                PRINT *,"Loop entry",3,160,":", 1, grid_points(2)-2
            do j = 1, grid_points(2)-2
               jm1 = j-1
               jp1 = j+1
                  
               forcing(1,i,j,k) = forcing(1,i,j,k) -
     >                 ty2*( ue(jp1,3)-ue(jm1,3) )+
     >                 dy1ty1*(ue(jp1,1)-2.0d0*ue(j,1)+ue(jm1,1))

               forcing(2,i,j,k) = forcing(2,i,j,k) - ty2*(
     >                 ue(jp1,2)*buf(jp1,3)-ue(jm1,2)*buf(jm1,3))+
     >                 yycon2*(buf(jp1,2)-2.0d0*buf(j,2)+buf(jm1,2))+
     >                 dy2ty1*( ue(jp1,2)-2.0* ue(j,2)+ ue(jm1,2))

               forcing(3,i,j,k) = forcing(3,i,j,k) - ty2*(
     >                 (ue(jp1,3)*buf(jp1,3)+c2*(ue(jp1,5)-q(jp1)))-
     >                 (ue(jm1,3)*buf(jm1,3)+c2*(ue(jm1,5)-q(jm1))))+
     >                 yycon1*(buf(jp1,3)-2.0d0*buf(j,3)+buf(jm1,3))+
     >                 dy3ty1*( ue(jp1,3)-2.0d0*ue(j,3) +ue(jm1,3))

               forcing(4,i,j,k) = forcing(4,i,j,k) - ty2*(
     >                 ue(jp1,4)*buf(jp1,3)-ue(jm1,4)*buf(jm1,3))+
     >                 yycon2*(buf(jp1,4)-2.0d0*buf(j,4)+buf(jm1,4))+
     >                 dy4ty1*( ue(jp1,4)-2.0d0*ue(j,4)+ ue(jm1,4))

               forcing(5,i,j,k) = forcing(5,i,j,k) - ty2*(
     >                 buf(jp1,3)*(c1*ue(jp1,5)-c2*q(jp1))-
     >                 buf(jm1,3)*(c1*ue(jm1,5)-c2*q(jm1)))+
     >                 0.5d0*yycon3*(buf(jp1,1)-2.0d0*buf(j,1)+
     >                 buf(jm1,1))+
     >                 yycon4*(cuf(jp1)-2.0d0*cuf(j)+cuf(jm1))+
     >                 yycon5*(buf(jp1,5)-2.0d0*buf(j,5)+buf(jm1,5))+
     >                 dy5ty1*(ue(jp1,5)-2.0d0*ue(j,5)+ue(jm1,5))
              EXIT
            enddo
            PRINT *,"Loop exit",3,192

c---------------------------------------------------------------------
c     Fourth-order dissipation                      
c---------------------------------------------------------------------
                PRINT *,"Loop entry",3,197,":", 1, 5
            do m = 1, 5
               j = 1
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (5.0d0*ue(j,m) - 4.0d0*ue(j+1,m) +ue(j+2,m))
               j = 2
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (-4.0d0*ue(j-1,m) + 6.0d0*ue(j,m) -
     >                    4.0d0*ue(j+1,m) +       ue(j+2,m))
              EXIT
            enddo
            PRINT *,"Loop exit",3,205

                PRINT *,"Loop entry",3,207,":", 3, grid_points(2)-4
            do j = 3, grid_points(2)-4
                   PRINT *,"Loop entry",4,208,":", 1, 5
               do m = 1, 5
                  forcing(m,i,j,k) = forcing(m,i,j,k) - dssp*
     >                    (ue(j-2,m) - 4.0d0*ue(j-1,m) +
     >                    6.0d0*ue(j,m) - 4.0d0*ue(j+1,m) + ue(j+2,m))
                 EXIT
               enddo
               PRINT *,"Loop exit",4,212
              EXIT
            enddo
            PRINT *,"Loop exit",3,213

                PRINT *,"Loop entry",3,215,":", 1, 5
            do m = 1, 5
               j = grid_points(2)-3
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (ue(j-2,m) - 4.0d0*ue(j-1,m) +
     >                    6.0d0*ue(j,m) - 4.0d0*ue(j+1,m))
               j = grid_points(2)-2
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (ue(j-2,m) - 4.0d0*ue(j-1,m) + 5.0d0*ue(j,m))

              EXIT
            enddo
            PRINT *,"Loop exit",3,224

           EXIT
         enddo
         PRINT *,"Loop exit",2,226
        EXIT
      enddo
      PRINT *,"Loop exit",1,227

c---------------------------------------------------------------------
c     zeta-direction flux differences                      
c---------------------------------------------------------------------
        PRINT *,"Loop entry",1,232,":",1, grid_points(2)-2
      do j=1, grid_points(2)-2
         eta = dble(j) * dnym1
             PRINT *,"Loop entry",2,234,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
            xi = dble(i) * dnxm1

              PRINT *,"Loop entry",3,237,":",0, grid_points(3)-1
            do k=0, grid_points(3)-1
               zeta = dble(k) * dnzm1

                   PRINT *,"Begin - exact_solution",240
               call exact_solution(xi, eta, zeta, dtemp)
                   PRINT *,"End - exact_solution",240
                   PRINT *,"Loop entry",4,241,":", 1, 5
               do m = 1, 5
                  ue(k,m) = dtemp(m)
                 EXIT
               enddo
               PRINT *,"Loop exit",4,243

               dtpp = 1.0d0/dtemp(1)

                   PRINT *,"Loop entry",4,247,":", 2, 5
               do m = 2, 5
                  buf(k,m) = dtpp * dtemp(m)
                 EXIT
               enddo
               PRINT *,"Loop exit",4,249

               cuf(k)   = buf(k,4) * buf(k,4)
               buf(k,1) = cuf(k) + buf(k,2) * buf(k,2) + 
     >                 buf(k,3) * buf(k,3)
               q(k) = 0.5d0*(buf(k,2)*ue(k,2) + buf(k,3)*ue(k,3) +
     >                 buf(k,4)*ue(k,4))
              EXIT
            enddo
            PRINT *,"Loop exit",3,256

              PRINT *,"Loop entry",3,258,":",1, grid_points(3)-2
            do k=1, grid_points(3)-2
               km1 = k-1
               kp1 = k+1
                  
               forcing(1,i,j,k) = forcing(1,i,j,k) -
     >                 tz2*( ue(kp1,4)-ue(km1,4) )+
     >                 dz1tz1*(ue(kp1,1)-2.0d0*ue(k,1)+ue(km1,1))

               forcing(2,i,j,k) = forcing(2,i,j,k) - tz2 * (
     >                 ue(kp1,2)*buf(kp1,4)-ue(km1,2)*buf(km1,4))+
     >                 zzcon2*(buf(kp1,2)-2.0d0*buf(k,2)+buf(km1,2))+
     >                 dz2tz1*( ue(kp1,2)-2.0d0* ue(k,2)+ ue(km1,2))

               forcing(3,i,j,k) = forcing(3,i,j,k) - tz2 * (
     >                 ue(kp1,3)*buf(kp1,4)-ue(km1,3)*buf(km1,4))+
     >                 zzcon2*(buf(kp1,3)-2.0d0*buf(k,3)+buf(km1,3))+
     >                 dz3tz1*(ue(kp1,3)-2.0d0*ue(k,3)+ue(km1,3))

               forcing(4,i,j,k) = forcing(4,i,j,k) - tz2 * (
     >                 (ue(kp1,4)*buf(kp1,4)+c2*(ue(kp1,5)-q(kp1)))-
     >                 (ue(km1,4)*buf(km1,4)+c2*(ue(km1,5)-q(km1))))+
     >                 zzcon1*(buf(kp1,4)-2.0d0*buf(k,4)+buf(km1,4))+
     >                 dz4tz1*( ue(kp1,4)-2.0d0*ue(k,4) +ue(km1,4))

               forcing(5,i,j,k) = forcing(5,i,j,k) - tz2 * (
     >                 buf(kp1,4)*(c1*ue(kp1,5)-c2*q(kp1))-
     >                 buf(km1,4)*(c1*ue(km1,5)-c2*q(km1)))+
     >                 0.5d0*zzcon3*(buf(kp1,1)-2.0d0*buf(k,1)
     >                 +buf(km1,1))+
     >                 zzcon4*(cuf(kp1)-2.0d0*cuf(k)+cuf(km1))+
     >                 zzcon5*(buf(kp1,5)-2.0d0*buf(k,5)+buf(km1,5))+
     >                 dz5tz1*( ue(kp1,5)-2.0d0*ue(k,5)+ ue(km1,5))
              EXIT
            enddo
            PRINT *,"Loop exit",3,290

c---------------------------------------------------------------------
c     Fourth-order dissipation                        
c---------------------------------------------------------------------
                PRINT *,"Loop entry",3,295,":", 1, 5
            do m = 1, 5
               k = 1
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (5.0d0*ue(k,m) - 4.0d0*ue(k+1,m) +ue(k+2,m))
               k = 2
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (-4.0d0*ue(k-1,m) + 6.0d0*ue(k,m) -
     >                    4.0d0*ue(k+1,m) +       ue(k+2,m))
              EXIT
            enddo
            PRINT *,"Loop exit",3,303

                PRINT *,"Loop entry",3,305,":", 3, grid_points(3)-4
            do k = 3, grid_points(3)-4
                   PRINT *,"Loop entry",4,306,":", 1, 5
               do m = 1, 5
                  forcing(m,i,j,k) = forcing(m,i,j,k) - dssp*
     >                    (ue(k-2,m) - 4.0d0*ue(k-1,m) +
     >                    6.0d0*ue(k,m) - 4.0d0*ue(k+1,m) + ue(k+2,m))
                 EXIT
               enddo
               PRINT *,"Loop exit",4,310
              EXIT
            enddo
            PRINT *,"Loop exit",3,311

                PRINT *,"Loop entry",3,313,":", 1, 5
            do m = 1, 5
               k = grid_points(3)-3
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (ue(k-2,m) - 4.0d0*ue(k-1,m) +
     >                    6.0d0*ue(k,m) - 4.0d0*ue(k+1,m))
               k = grid_points(3)-2
               forcing(m,i,j,k) = forcing(m,i,j,k) - dssp *
     >                    (ue(k-2,m) - 4.0d0*ue(k-1,m) + 5.0d0*ue(k,m))
              EXIT
            enddo
            PRINT *,"Loop exit",3,321

           EXIT
         enddo
         PRINT *,"Loop exit",2,323
        EXIT
      enddo
      PRINT *,"Loop exit",1,324

c---------------------------------------------------------------------
c     now change the sign of the forcing function, 
c---------------------------------------------------------------------
          PRINT *,"Loop entry",1,329,":", 1, grid_points(3)-2
      do k = 1, grid_points(3)-2
             PRINT *,"Loop entry",2,330,":", 1, grid_points(2)-2
         do j = 1, grid_points(2)-2
                PRINT *,"Loop entry",3,331,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2
                   PRINT *,"Loop entry",4,332,":", 1, 5
               do m = 1, 5
                  forcing(m,i,j,k) = -1.d0 * forcing(m,i,j,k)
                 EXIT
               enddo
               PRINT *,"Loop exit",4,334
              EXIT
            enddo
            PRINT *,"Loop exit",3,335
           EXIT
         enddo
         PRINT *,"Loop exit",2,336
        EXIT
      enddo
      PRINT *,"Loop exit",1,337


      return
      end
