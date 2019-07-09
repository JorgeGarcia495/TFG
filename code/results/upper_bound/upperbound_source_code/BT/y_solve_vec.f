c---------------------------------------------------------------------
c---------------------------------------------------------------------

      subroutine y_solve

c---------------------------------------------------------------------
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c     Performs line solves in Y direction by first factoring
c     the block-tridiagonal matrix into an upper triangular matrix, 
c     and then performing back substitution to solve for the unknow
c     vectors of each line.  
c     
c     Make sure we treat elements zero to cell_size in the direction
c     of the sweep.
c---------------------------------------------------------------------

      include 'header.h'
      include 'work_lhs_vec.h'

      integer i, j, k, m, n, jsize

c---------------------------------------------------------------------
c---------------------------------------------------------------------

      if (timeron) call timer_start(t_ysolve)

c---------------------------------------------------------------------
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c     This function computes the left hand side for the three y-factors 
c---------------------------------------------------------------------

      jsize = grid_points(2)-1

c---------------------------------------------------------------------
c     Compute the indices for storing the tri-diagonal matrix;
c     determine a (labeled f) and n jacobians for cell c
c---------------------------------------------------------------------
          PRINT *,"Loop entry",1,42,":", 1, grid_points(3)-2
      do k = 1, grid_points(3)-2
             PRINT *,"Loop entry",2,43,":", 0, jsize
         do j = 0, jsize
                PRINT *,"Loop entry",3,44,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2

               tmp1 = rho_i(i,j,k)
               tmp2 = tmp1 * tmp1
               tmp3 = tmp1 * tmp2

               fjac(1,1,i,j) = 0.0d+00
               fjac(1,2,i,j) = 0.0d+00
               fjac(1,3,i,j) = 1.0d+00
               fjac(1,4,i,j) = 0.0d+00
               fjac(1,5,i,j) = 0.0d+00

               fjac(2,1,i,j) = - ( u(2,i,j,k)*u(3,i,j,k) )
     >              * tmp2
               fjac(2,2,i,j) = u(3,i,j,k) * tmp1
               fjac(2,3,i,j) = u(2,i,j,k) * tmp1
               fjac(2,4,i,j) = 0.0d+00
               fjac(2,5,i,j) = 0.0d+00

               fjac(3,1,i,j) = - ( u(3,i,j,k)*u(3,i,j,k)*tmp2)
     >              + c2 * qs(i,j,k)
               fjac(3,2,i,j) = - c2 *  u(2,i,j,k) * tmp1
               fjac(3,3,i,j) = ( 2.0d+00 - c2 )
     >              *  u(3,i,j,k) * tmp1 
               fjac(3,4,i,j) = - c2 * u(4,i,j,k) * tmp1 
               fjac(3,5,i,j) = c2

               fjac(4,1,i,j) = - ( u(3,i,j,k)*u(4,i,j,k) )
     >              * tmp2
               fjac(4,2,i,j) = 0.0d+00
               fjac(4,3,i,j) = u(4,i,j,k) * tmp1
               fjac(4,4,i,j) = u(3,i,j,k) * tmp1
               fjac(4,5,i,j) = 0.0d+00

               fjac(5,1,i,j) = ( c2 * 2.0d0 * square(i,j,k)
     >              - c1 * u(5,i,j,k) )
     >              * u(3,i,j,k) * tmp2
               fjac(5,2,i,j) = - c2 * u(2,i,j,k)*u(3,i,j,k) 
     >              * tmp2
               fjac(5,3,i,j) = c1 * u(5,i,j,k) * tmp1 
     >              - c2 
     >              * ( qs(i,j,k)
     >              + u(3,i,j,k)*u(3,i,j,k) * tmp2 )
               fjac(5,4,i,j) = - c2 * ( u(3,i,j,k)*u(4,i,j,k) )
     >              * tmp2
               fjac(5,5,i,j) = c1 * u(3,i,j,k) * tmp1 

               njac(1,1,i,j) = 0.0d+00
               njac(1,2,i,j) = 0.0d+00
               njac(1,3,i,j) = 0.0d+00
               njac(1,4,i,j) = 0.0d+00
               njac(1,5,i,j) = 0.0d+00

               njac(2,1,i,j) = - c3c4 * tmp2 * u(2,i,j,k)
               njac(2,2,i,j) =   c3c4 * tmp1
               njac(2,3,i,j) =   0.0d+00
               njac(2,4,i,j) =   0.0d+00
               njac(2,5,i,j) =   0.0d+00

               njac(3,1,i,j) = - con43 * c3c4 * tmp2 * u(3,i,j,k)
               njac(3,2,i,j) =   0.0d+00
               njac(3,3,i,j) =   con43 * c3c4 * tmp1
               njac(3,4,i,j) =   0.0d+00
               njac(3,5,i,j) =   0.0d+00

               njac(4,1,i,j) = - c3c4 * tmp2 * u(4,i,j,k)
               njac(4,2,i,j) =   0.0d+00
               njac(4,3,i,j) =   0.0d+00
               njac(4,4,i,j) =   c3c4 * tmp1
               njac(4,5,i,j) =   0.0d+00

               njac(5,1,i,j) = - (  c3c4
     >              - c1345 ) * tmp3 * (u(2,i,j,k)**2)
     >              - ( con43 * c3c4
     >              - c1345 ) * tmp3 * (u(3,i,j,k)**2)
     >              - ( c3c4 - c1345 ) * tmp3 * (u(4,i,j,k)**2)
     >              - c1345 * tmp2 * u(5,i,j,k)

               njac(5,2,i,j) = (  c3c4 - c1345 ) * tmp2 * u(2,i,j,k)
               njac(5,3,i,j) = ( con43 * c3c4
     >              - c1345 ) * tmp2 * u(3,i,j,k)
               njac(5,4,i,j) = ( c3c4 - c1345 ) * tmp2 * u(4,i,j,k)
               njac(5,5,i,j) = ( c1345 ) * tmp1

              EXIT
            enddo
            PRINT *,"Loop exit",3,128
           EXIT
         enddo
         PRINT *,"Loop exit",2,129

c---------------------------------------------------------------------
c     zero the whole left hand side for starters
c     set all diagonal values to 1. This is overkill, but convenient
c---------------------------------------------------------------------
             PRINT *,"Loop entry",2,135,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
                PRINT *,"Loop entry",3,136,":", 1, 5
            do m = 1, 5
                   PRINT *,"Loop entry",4,137,":", 1, 5
               do n = 1, 5
                  lhs(m,n,aa,i,0) = 0.0d0
                  lhs(m,n,bb,i,0) = 0.0d0
                  lhs(m,n,cc,i,0) = 0.0d0
                  lhs(m,n,aa,i,jsize) = 0.0d0
                  lhs(m,n,bb,i,jsize) = 0.0d0
                  lhs(m,n,cc,i,jsize) = 0.0d0
                  EXIT
               end do
                PRINT *,"Loop exit",4,144
               lhs(m,m,bb,i,0) = 1.0d0
               lhs(m,m,bb,i,jsize) = 1.0d0
               EXIT
            end do
             PRINT *,"Loop exit",3,147
           EXIT
         enddo
         PRINT *,"Loop exit",2,148

c---------------------------------------------------------------------
c     now joacobians set, so form left hand side in y direction
c---------------------------------------------------------------------
             PRINT *,"Loop entry",2,153,":", 1, jsize-1
         do j = 1, jsize-1
                PRINT *,"Loop entry",3,154,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2

               tmp1 = dt * ty1
               tmp2 = dt * ty2

               lhs(1,1,aa,i,j) = - tmp2 * fjac(1,1,i,j-1)
     >              - tmp1 * njac(1,1,i,j-1)
     >              - tmp1 * dy1 
               lhs(1,2,aa,i,j) = - tmp2 * fjac(1,2,i,j-1)
     >              - tmp1 * njac(1,2,i,j-1)
               lhs(1,3,aa,i,j) = - tmp2 * fjac(1,3,i,j-1)
     >              - tmp1 * njac(1,3,i,j-1)
               lhs(1,4,aa,i,j) = - tmp2 * fjac(1,4,i,j-1)
     >              - tmp1 * njac(1,4,i,j-1)
               lhs(1,5,aa,i,j) = - tmp2 * fjac(1,5,i,j-1)
     >              - tmp1 * njac(1,5,i,j-1)

               lhs(2,1,aa,i,j) = - tmp2 * fjac(2,1,i,j-1)
     >              - tmp1 * njac(2,1,i,j-1)
               lhs(2,2,aa,i,j) = - tmp2 * fjac(2,2,i,j-1)
     >              - tmp1 * njac(2,2,i,j-1)
     >              - tmp1 * dy2
               lhs(2,3,aa,i,j) = - tmp2 * fjac(2,3,i,j-1)
     >              - tmp1 * njac(2,3,i,j-1)
               lhs(2,4,aa,i,j) = - tmp2 * fjac(2,4,i,j-1)
     >              - tmp1 * njac(2,4,i,j-1)
               lhs(2,5,aa,i,j) = - tmp2 * fjac(2,5,i,j-1)
     >              - tmp1 * njac(2,5,i,j-1)

               lhs(3,1,aa,i,j) = - tmp2 * fjac(3,1,i,j-1)
     >              - tmp1 * njac(3,1,i,j-1)
               lhs(3,2,aa,i,j) = - tmp2 * fjac(3,2,i,j-1)
     >              - tmp1 * njac(3,2,i,j-1)
               lhs(3,3,aa,i,j) = - tmp2 * fjac(3,3,i,j-1)
     >              - tmp1 * njac(3,3,i,j-1)
     >              - tmp1 * dy3 
               lhs(3,4,aa,i,j) = - tmp2 * fjac(3,4,i,j-1)
     >              - tmp1 * njac(3,4,i,j-1)
               lhs(3,5,aa,i,j) = - tmp2 * fjac(3,5,i,j-1)
     >              - tmp1 * njac(3,5,i,j-1)

               lhs(4,1,aa,i,j) = - tmp2 * fjac(4,1,i,j-1)
     >              - tmp1 * njac(4,1,i,j-1)
               lhs(4,2,aa,i,j) = - tmp2 * fjac(4,2,i,j-1)
     >              - tmp1 * njac(4,2,i,j-1)
               lhs(4,3,aa,i,j) = - tmp2 * fjac(4,3,i,j-1)
     >              - tmp1 * njac(4,3,i,j-1)
               lhs(4,4,aa,i,j) = - tmp2 * fjac(4,4,i,j-1)
     >              - tmp1 * njac(4,4,i,j-1)
     >              - tmp1 * dy4
               lhs(4,5,aa,i,j) = - tmp2 * fjac(4,5,i,j-1)
     >              - tmp1 * njac(4,5,i,j-1)

               lhs(5,1,aa,i,j) = - tmp2 * fjac(5,1,i,j-1)
     >              - tmp1 * njac(5,1,i,j-1)
               lhs(5,2,aa,i,j) = - tmp2 * fjac(5,2,i,j-1)
     >              - tmp1 * njac(5,2,i,j-1)
               lhs(5,3,aa,i,j) = - tmp2 * fjac(5,3,i,j-1)
     >              - tmp1 * njac(5,3,i,j-1)
               lhs(5,4,aa,i,j) = - tmp2 * fjac(5,4,i,j-1)
     >              - tmp1 * njac(5,4,i,j-1)
               lhs(5,5,aa,i,j) = - tmp2 * fjac(5,5,i,j-1)
     >              - tmp1 * njac(5,5,i,j-1)
     >              - tmp1 * dy5

               lhs(1,1,bb,i,j) = 1.0d+00
     >              + tmp1 * 2.0d+00 * njac(1,1,i,j)
     >              + tmp1 * 2.0d+00 * dy1
               lhs(1,2,bb,i,j) = tmp1 * 2.0d+00 * njac(1,2,i,j)
               lhs(1,3,bb,i,j) = tmp1 * 2.0d+00 * njac(1,3,i,j)
               lhs(1,4,bb,i,j) = tmp1 * 2.0d+00 * njac(1,4,i,j)
               lhs(1,5,bb,i,j) = tmp1 * 2.0d+00 * njac(1,5,i,j)

               lhs(2,1,bb,i,j) = tmp1 * 2.0d+00 * njac(2,1,i,j)
               lhs(2,2,bb,i,j) = 1.0d+00
     >              + tmp1 * 2.0d+00 * njac(2,2,i,j)
     >              + tmp1 * 2.0d+00 * dy2
               lhs(2,3,bb,i,j) = tmp1 * 2.0d+00 * njac(2,3,i,j)
               lhs(2,4,bb,i,j) = tmp1 * 2.0d+00 * njac(2,4,i,j)
               lhs(2,5,bb,i,j) = tmp1 * 2.0d+00 * njac(2,5,i,j)

               lhs(3,1,bb,i,j) = tmp1 * 2.0d+00 * njac(3,1,i,j)
               lhs(3,2,bb,i,j) = tmp1 * 2.0d+00 * njac(3,2,i,j)
               lhs(3,3,bb,i,j) = 1.0d+00
     >              + tmp1 * 2.0d+00 * njac(3,3,i,j)
     >              + tmp1 * 2.0d+00 * dy3
               lhs(3,4,bb,i,j) = tmp1 * 2.0d+00 * njac(3,4,i,j)
               lhs(3,5,bb,i,j) = tmp1 * 2.0d+00 * njac(3,5,i,j)

               lhs(4,1,bb,i,j) = tmp1 * 2.0d+00 * njac(4,1,i,j)
               lhs(4,2,bb,i,j) = tmp1 * 2.0d+00 * njac(4,2,i,j)
               lhs(4,3,bb,i,j) = tmp1 * 2.0d+00 * njac(4,3,i,j)
               lhs(4,4,bb,i,j) = 1.0d+00
     >              + tmp1 * 2.0d+00 * njac(4,4,i,j)
     >              + tmp1 * 2.0d+00 * dy4
               lhs(4,5,bb,i,j) = tmp1 * 2.0d+00 * njac(4,5,i,j)

               lhs(5,1,bb,i,j) = tmp1 * 2.0d+00 * njac(5,1,i,j)
               lhs(5,2,bb,i,j) = tmp1 * 2.0d+00 * njac(5,2,i,j)
               lhs(5,3,bb,i,j) = tmp1 * 2.0d+00 * njac(5,3,i,j)
               lhs(5,4,bb,i,j) = tmp1 * 2.0d+00 * njac(5,4,i,j)
               lhs(5,5,bb,i,j) = 1.0d+00
     >              + tmp1 * 2.0d+00 * njac(5,5,i,j) 
     >              + tmp1 * 2.0d+00 * dy5

               lhs(1,1,cc,i,j) =  tmp2 * fjac(1,1,i,j+1)
     >              - tmp1 * njac(1,1,i,j+1)
     >              - tmp1 * dy1
               lhs(1,2,cc,i,j) =  tmp2 * fjac(1,2,i,j+1)
     >              - tmp1 * njac(1,2,i,j+1)
               lhs(1,3,cc,i,j) =  tmp2 * fjac(1,3,i,j+1)
     >              - tmp1 * njac(1,3,i,j+1)
               lhs(1,4,cc,i,j) =  tmp2 * fjac(1,4,i,j+1)
     >              - tmp1 * njac(1,4,i,j+1)
               lhs(1,5,cc,i,j) =  tmp2 * fjac(1,5,i,j+1)
     >              - tmp1 * njac(1,5,i,j+1)

               lhs(2,1,cc,i,j) =  tmp2 * fjac(2,1,i,j+1)
     >              - tmp1 * njac(2,1,i,j+1)
               lhs(2,2,cc,i,j) =  tmp2 * fjac(2,2,i,j+1)
     >              - tmp1 * njac(2,2,i,j+1)
     >              - tmp1 * dy2
               lhs(2,3,cc,i,j) =  tmp2 * fjac(2,3,i,j+1)
     >              - tmp1 * njac(2,3,i,j+1)
               lhs(2,4,cc,i,j) =  tmp2 * fjac(2,4,i,j+1)
     >              - tmp1 * njac(2,4,i,j+1)
               lhs(2,5,cc,i,j) =  tmp2 * fjac(2,5,i,j+1)
     >              - tmp1 * njac(2,5,i,j+1)

               lhs(3,1,cc,i,j) =  tmp2 * fjac(3,1,i,j+1)
     >              - tmp1 * njac(3,1,i,j+1)
               lhs(3,2,cc,i,j) =  tmp2 * fjac(3,2,i,j+1)
     >              - tmp1 * njac(3,2,i,j+1)
               lhs(3,3,cc,i,j) =  tmp2 * fjac(3,3,i,j+1)
     >              - tmp1 * njac(3,3,i,j+1)
     >              - tmp1 * dy3
               lhs(3,4,cc,i,j) =  tmp2 * fjac(3,4,i,j+1)
     >              - tmp1 * njac(3,4,i,j+1)
               lhs(3,5,cc,i,j) =  tmp2 * fjac(3,5,i,j+1)
     >              - tmp1 * njac(3,5,i,j+1)

               lhs(4,1,cc,i,j) =  tmp2 * fjac(4,1,i,j+1)
     >              - tmp1 * njac(4,1,i,j+1)
               lhs(4,2,cc,i,j) =  tmp2 * fjac(4,2,i,j+1)
     >              - tmp1 * njac(4,2,i,j+1)
               lhs(4,3,cc,i,j) =  tmp2 * fjac(4,3,i,j+1)
     >              - tmp1 * njac(4,3,i,j+1)
               lhs(4,4,cc,i,j) =  tmp2 * fjac(4,4,i,j+1)
     >              - tmp1 * njac(4,4,i,j+1)
     >              - tmp1 * dy4
               lhs(4,5,cc,i,j) =  tmp2 * fjac(4,5,i,j+1)
     >              - tmp1 * njac(4,5,i,j+1)

               lhs(5,1,cc,i,j) =  tmp2 * fjac(5,1,i,j+1)
     >              - tmp1 * njac(5,1,i,j+1)
               lhs(5,2,cc,i,j) =  tmp2 * fjac(5,2,i,j+1)
     >              - tmp1 * njac(5,2,i,j+1)
               lhs(5,3,cc,i,j) =  tmp2 * fjac(5,3,i,j+1)
     >              - tmp1 * njac(5,3,i,j+1)
               lhs(5,4,cc,i,j) =  tmp2 * fjac(5,4,i,j+1)
     >              - tmp1 * njac(5,4,i,j+1)
               lhs(5,5,cc,i,j) =  tmp2 * fjac(5,5,i,j+1)
     >              - tmp1 * njac(5,5,i,j+1)
     >              - tmp1 * dy5

              EXIT
            enddo
            PRINT *,"Loop exit",3,319
           EXIT
         enddo
         PRINT *,"Loop exit",2,320

c---------------------------------------------------------------------
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c     performs guaussian elimination on this cell.
c     
c     assumes that unpacking routines for non-first cells 
c     preload C' and rhs' from previous cell.
c     
c     assumed send happens outside this routine, but that
c     c'(JMAX) and rhs'(JMAX) will be sent to next cell
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c     multiply c(i,0,k) by b_inverse and copy back to c
c     multiply rhs(0) by b_inverse(0) and copy to rhs
c---------------------------------------------------------------------
!dir$ ivdep
             PRINT *,"Loop entry",2,340,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
              PRINT *,"Begin - binvcrhs",341
            call binvcrhs( lhs(1,1,bb,i,0),
     >                        lhs(1,1,cc,i,0),
     >                        rhs(1,i,0,k) )
                              PRINT *,"End - binvcrhs",343
           EXIT
         enddo
         PRINT *,"Loop exit",2,344

c---------------------------------------------------------------------
c     begin inner most do loop
c     do all the elements of the cell unless last 
c---------------------------------------------------------------------
          PRINT *,"Loop entry",2,350,":",1,jsize-1
         do j=1,jsize-1
!dir$ ivdep
                PRINT *,"Loop entry",3,352,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2

c---------------------------------------------------------------------
c     subtract A*lhs_vector(j-1) from lhs_vector(j)
c     
c     rhs(j) = rhs(j) - A*rhs(j-1)
c---------------------------------------------------------------------
                PRINT *,"Begin - matvec_sub",359
               call matvec_sub(lhs(1,1,aa,i,j),
     >                         rhs(1,i,j-1,k),rhs(1,i,j,k))
                              PRINT *,"End - matvec_sub",360

c---------------------------------------------------------------------
c     B(j) = B(j) - C(j-1)*A(j)
c---------------------------------------------------------------------
                PRINT *,"Begin - matmul_sub",365
               call matmul_sub(lhs(1,1,aa,i,j),
     >                         lhs(1,1,cc,i,j-1),
     >                         lhs(1,1,bb,i,j))
                              PRINT *,"End - matmul_sub",367

c---------------------------------------------------------------------
c     multiply c(i,j,k) by b_inverse and copy back to c
c     multiply rhs(i,1,k) by b_inverse(i,1,k) and copy to rhs
c---------------------------------------------------------------------
                 PRINT *,"Begin - binvcrhs",373
               call binvcrhs( lhs(1,1,bb,i,j),
     >                        lhs(1,1,cc,i,j),
     >                        rhs(1,i,j,k) )
                              PRINT *,"End - binvcrhs",375

              EXIT
            enddo
            PRINT *,"Loop exit",3,377
           EXIT
         enddo
         PRINT *,"Loop exit",2,378


c---------------------------------------------------------------------
c     rhs(jsize) = rhs(jsize) - A*rhs(jsize-1)
c---------------------------------------------------------------------
!dir$ ivdep
             PRINT *,"Loop entry",2,385,":", 1, grid_points(1)-2
         do i = 1, grid_points(1)-2
             PRINT *,"Begin - matvec_sub",386
            call matvec_sub(lhs(1,1,aa,i,jsize),
     >                         rhs(1,i,jsize-1,k),rhs(1,i,jsize,k))
                              PRINT *,"End - matvec_sub",387

c---------------------------------------------------------------------
c     B(jsize) = B(jsize) - C(jsize-1)*A(jsize)
c     call matmul_sub(aa,i,jsize,k,c,
c     $              cc,i,jsize-1,k,c,bb,i,jsize,k)
c---------------------------------------------------------------------
             PRINT *,"Begin - matmul_sub",394
            call matmul_sub(lhs(1,1,aa,i,jsize),
     >                         lhs(1,1,cc,i,jsize-1),
     >                         lhs(1,1,bb,i,jsize))
                              PRINT *,"End - matmul_sub",396

c---------------------------------------------------------------------
c     multiply rhs(jsize) by b_inverse(jsize) and copy to rhs
c---------------------------------------------------------------------
              PRINT *,"Begin - binvrhs",401
            call binvrhs( lhs(1,1,bb,i,jsize),
     >                       rhs(1,i,jsize,k) )
                             PRINT *,"End - binvrhs",402
           EXIT
         enddo
         PRINT *,"Loop exit",2,403


c---------------------------------------------------------------------
c     back solve: if last cell, then generate U(jsize)=rhs(jsize)
c     else assume U(jsize) is loaded in un pack backsub_info
c     so just use it
c     after call u(jstart) will be sent to next cell
c---------------------------------------------------------------------
      
          PRINT *,"Loop entry",2,413,":",jsize-1,0,-1
         do j=jsize-1,0,-1
                PRINT *,"Loop entry",3,414,":", 1, grid_points(1)-2
            do i = 1, grid_points(1)-2
                PRINT *,"Loop entry",4,415,":",1,BLOCK_SIZE
               do m=1,BLOCK_SIZE
                   PRINT *,"Loop entry",5,416,":",1,BLOCK_SIZE
                  do n=1,BLOCK_SIZE
                     rhs(m,i,j,k) = rhs(m,i,j,k) 
     >                    - lhs(m,n,cc,i,j)*rhs(n,i,j+1,k)
                    EXIT
                  enddo
                  PRINT *,"Loop exit",5,419
                 EXIT
               enddo
               PRINT *,"Loop exit",4,420
              EXIT
            enddo
            PRINT *,"Loop exit",3,421
           EXIT
         enddo
         PRINT *,"Loop exit",2,422

        EXIT
      enddo
      PRINT *,"Loop exit",1,424
      if (timeron) call timer_stop(t_ysolve)

      return
      end


