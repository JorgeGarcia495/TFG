c---------------------------------------------------------------------
c---------------------------------------------------------------------

      double precision function randlc (x, a)

c---------------------------------------------------------------------
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c
c   This routine returns a uniform pseudorandom double precision number in the
c   range (0, 1) by using the linear congruential generator
c
c   x_{k+1} = a x_k  (mod 2^46)
c
c   where 0 < x_k < 2^46 and 0 < a < 2^46.  This scheme generates 2^44 numbers
c   before repeating.  The argument A is the same as 'a' in the above formula,
c   and X is the same as x_0.  A and X must be odd double precision integers
c   in the range (1, 2^46).  The returned value RANDLC is normalized to be
c   between 0 and 1, i.e. RANDLC = 2^(-46) * x_1.  X is updated to contain
c   the new seed x_1, so that subsequent calls to RANDLC using the same
c   arguments will generate a continuous sequence.
c
c   This routine should produce the same results on any computer with at least
c   48 mantissa bits in double precision floating point data.  On 64 bit
c   systems, double precision should be disabled.
c
c   David H. Bailey     October 26, 1990
c
c---------------------------------------------------------------------

      implicit none

      double precision r23,r46,t23,t46,a,x,t1,t2,t3,t4,a1,a2,x1,x2,z
      parameter (r23 = 0.5d0 ** 23, r46 = r23 ** 2, t23 = 2.d0 ** 23,
     >  t46 = t23 ** 2)

c---------------------------------------------------------------------
c   Break A into two parts such that A = 2^23 * A1 + A2.
c---------------------------------------------------------------------
      t1 = r23 * a
      a1 = int (t1)
      a2 = a - t23 * a1

c---------------------------------------------------------------------
c   Break X into two parts such that X = 2^23 * X1 + X2, compute
c   Z = A1 * X2 + A2 * X1  (mod 2^23), and then
c   X = 2^23 * Z + A2 * X2  (mod 2^46).
c---------------------------------------------------------------------
      t1 = r23 * x
      x1 = int (t1)
      x2 = x - t23 * x1
      t1 = a1 * x2 + a2 * x1
      t2 = int (r23 * t1)
      z = t1 - t23 * t2
      t3 = t23 * z + a2 * x2
      t4 = int (r46 * t3)
      x = t3 - t46 * t4
      randlc = r46 * x

      return
      end




c---------------------------------------------------------------------
c---------------------------------------------------------------------

      subroutine vranlc (n, x, a, y)

c---------------------------------------------------------------------
c---------------------------------------------------------------------

c---------------------------------------------------------------------
c
c   This routine generates N uniform pseudorandom double precision numbers in
c   the range (0, 1) by using the linear congruential generator
c
c   x_{k+1} = a x_k  (mod 2^46)
c
c   where 0 < x_k < 2^46 and 0 < a < 2^46.  This scheme generates 2^44 numbers
c   before repeating.  The argument A is the same as 'a' in the above formula,
c   and X is the same as x_0.  A and X must be odd double precision integers
c   in the range (1, 2^46).  The N results are placed in Y and are normalized
c   to be between 0 and 1.  X is updated to contain the new seed, so that
c   subsequent calls to VRANLC using the same arguments will generate a
c   continuous sequence.  If N is zero, only initialization is performed, and
c   the variables X, A and Y are ignored.
c
c   This routine is the standard version designed for scalar or RISC systems.
c   However, it should produce the same results on any single processor
c   computer with at least 48 mantissa bits in double precision floating point
c   data.  On 64 bit systems, double precision should be disabled.
c
c---------------------------------------------------------------------

      implicit none

      integer i,n
      double precision y,r23,r46,t23,t46,a,x,t1,t2,t3,t4,a1,a2,x1,x2,z
      dimension y(*)
      parameter (r23 = 0.5d0 ** 23, r46 = r23 ** 2, t23 = 2.d0 ** 23,
     >  t46 = t23 ** 2)


c---------------------------------------------------------------------
c   Break A into two parts such that A = 2^23 * A1 + A2.
c---------------------------------------------------------------------
      t1 = r23 * a
      a1 = int (t1)
      a2 = a - t23 * a1

c---------------------------------------------------------------------
c   Generate N results.   This loop is not vectorizable.
c---------------------------------------------------------------------
      do i = 1, n

c---------------------------------------------------------------------
c   Break X into two parts such that X = 2^23 * X1 + X2, compute
c   Z = A1 * X2 + A2 * X1  (mod 2^23), and then
c   X = 2^23 * Z + A2 * X2  (mod 2^46).
c---------------------------------------------------------------------
        t1 = r23 * x
        x1 = int (t1)
        x2 = x - t23 * x1
        t1 = a1 * x2 + a2 * x1
        t2 = int (r23 * t1)
        z = t1 - t23 * t2
        t3 = t23 * z + a2 * x2
        t4 = int (r46 * t3)
        x = t3 - t46 * t4
        y(i) = r46 * x
      enddo

      return
      end
