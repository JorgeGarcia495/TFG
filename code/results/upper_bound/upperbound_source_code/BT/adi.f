c---------------------------------------------------------------------
c---------------------------------------------------------------------

      subroutine  adi

c---------------------------------------------------------------------
c---------------------------------------------------------------------

       PRINT *,"Begin - compute_rhs",9
      call compute_rhs
       PRINT *,"End - compute_rhs",9

       PRINT *,"Begin - x_solve",11
      call x_solve
       PRINT *,"End - x_solve",11

       PRINT *,"Begin - y_solve",13
      call y_solve
       PRINT *,"End - y_solve",13

       PRINT *,"Begin - z_solve",15
      call z_solve
       PRINT *,"End - z_solve",15

       PRINT *,"Begin - add",17
      call add
       PRINT *,"End - add",17

      return
      end

