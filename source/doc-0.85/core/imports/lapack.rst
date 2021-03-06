LAPACK
------
A handful of LAPACK routines are currently used by Elemental: a few
routines for querying floating point characteristics and a few other utilities.
In addition, there are several BLAS-like routines which are technically part 
of LAPACK (e.g., ``csyr``) which were included in the BLAS imports section.

The prototypes can be found in
`include/El/core/imports/lapack.hpp <https://github.com/elemental/Elemental/tree/master/include/El/core/imports/lapack.hpp>`_,
while the implementations are in
`src/imports/lapack.cpp <https://github.com/elemental/Elemental/tree/master/src/imports/lapack.cpp>`_.

Machine information
^^^^^^^^^^^^^^^^^^^

In all of the following functions, `R` can be equal to either `float` or
`double`.

.. cpp:function:: Real lapack::MachineEpsilon<Real>()

   Return the relative machine precision.

.. cpp:function:: Real lapack::MachineSafeMin<Real>()

   Return the minimum number which can be inverted without underflow.

.. cpp:function:: Real lapack::MachinePrecision<Real>()

   Return the relative machine precision multiplied by the base.

.. cpp:function:: Real lapack::MachineUnderflowExponent<Real>()

   Return the minimum exponent before (gradual) underflow occurs.

.. cpp:function:: Real lapack::MachineUnderflowThreshold<Real>()

   Return the underflow threshold: ``(base)^((underflow exponent)-1)``.

.. cpp:function:: Real lapack::MachineOverflowExponent<Real>()

   Return the largest exponent before overflow.
    
.. cpp:function:: Real lapack::MachineOverflowThreshold<Real>()

   Return the overflow threshold: 
   ``(1-rel. prec.)) * (base)^(overflow exponent)``.

Safe norms
^^^^^^^^^^

.. cpp:function:: Real lapack::SafeNorm( Real alpha, Real beta )

   Return :math:`\sqrt{\alpha^2+\beta^2}` in a manner which avoids 
   under/overflow. `R` can be equal to either `float` or `double`.

.. cpp:function:: Real lapack::SafeNorm( Real alpha, Real beta, Real gamma )

   Return :math:`\sqrt{\alpha^2+\beta^2+\gamma^2}` in a manner which avoids
   under/overflow. `R` can be equal to either `float` or `double`.

Givens rotations
^^^^^^^^^^^^^^^^

Given :math:`\phi, \gamma \in \mathbb{C}^{n \times n}`, carefully compute 
:math:`c \in \mathbb{R}` and :math:`s, \rho \in \mathbb{C}` such that 

.. math::

   \left[\begin{array}{cc}
     c       & s \\
     -\bar s & c \end{array}\right] 
   \left[ \begin{array}{c} \phi \\ \gamma \end{array} \right] = 
   \left[ \begin{array}{c} \rho \\ 0 \end{array} \right],

where :math:`c^2 + |s|^2 = 1` and the mapping from :math:`(\phi,\gamma) \rightarrow (c,s,\rho)` is "as continuous as possible", in the manner described by 
Kahan and Demmel's "On computing Givens rotations reliably and efficiently".

.. cpp:function:: F lapack::Givens( F phi, F gamma, Base<F>* c, F* s )

   Computes a Givens rotation and returns the combined result, :math:`\rho`.

MRRR-based Hermitian EVP 
^^^^^^^^^^^^^^^^^^^^^^^^

.. cpp:function:: void lapack::HermitianEig( char uplo, int n, F* A, int lda, Base<F>* w, Base<F> absTol=0 )
.. cpp:function:: void lapack::HermitianEig( char uplo, int n, F* A, int lda, Base<F>* w, F* Z, int ldz, Base<F> absTol=0 )

   Compute all eigen-values/pairs of a Hermitian matrix.

.. cpp:function:: void lapack::HermitianEig( char uplo, int n, F* A, int lda, Base<F>* w, int il, int iu, Base<F> absTol=0 )
.. cpp:function:: void lapack::HermitianEig( char uplo, int n, F* A, int lda, Base<F>* w, F* Z, int ldz, int il, int iu, Base<F> absTol=0 )

   Compute the `il`'th through `iu`'th eigen-values/pairs of a Hermitian matrix.

.. cpp:function:: void lapack::HermitianEig( char uplo, int n, F* A, int lda, Base<F>* w, Base<F> vl, Base<F> vu, Base<F> absTol=0 )
.. cpp:function:: void lapack::HermitianEig( char uplo, int n, F* A, int lda, Base<F>* w, F* Z, int ldz, Base<F> vl, Base<F> vu, Base<F> absTol=0 )

   Compute the eigen-values/pairs of a Hermitian matrix with eigenvalues in the
   half-open interval :math:`(v_l,v_u]`.

QR- and DQDS-based SVD
^^^^^^^^^^^^^^^^^^^^^^

.. cpp:function:: void lapack::QRSVD( int m, int n, F* A, int lda, Base<F>* s, F* U, int ldu, F* VAdj, int ldva )

   Computes the singular value decomposition of a general matrix by running the 
   QR algorithm on the condensed bidiagonal matrix.

.. cpp:function:: void lapack::SVD( int m, int n, F* A, int lda, Base<F>* s )

   Computes the singular values of a general matrix by running DQDS on the 
   condensed bidiagonal matrix.

Divide-and-conquer SVD
^^^^^^^^^^^^^^^^^^^^^^

.. cpp:function:: void lapack::DivideAndConquerSVD( int m, int n, F* A, int lda, Base<F>* s, F* U, int ldu, F* VAdj, int ldva )

   Computes the SVD of a general matrix using a divide-and-conquer algorithm on
   the condensed bidiagonal matrix.

Bidiagonal QR
^^^^^^^^^^^^^

.. cpp:function:: void lapack::BidiagQRAlg( char uplo, int n, int numColsVTrans, int numRowsU, Base<F>* d, Base<F>* e, F* VAdj, int ldva, F* U, int ldu )

   Computes the SVD of a bidiagonal matrix using the QR algorithm.

Hessenberg Schur decomposition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. cpp:function:: void lapack::HessenbergSchur( int n, F* H, int ldh, Complex<Base<F>>* w, bool fullTriangle=false )

   Computes the eigenvalues (and possibly the full Schur factor) of an upper 
   Hessenberg matrix using the QR algorithm.

.. cpp:function:: void lapack::HessenbergSchur( int n, F* H, int ldh, Complex<Base<F>>* w, F* Q, int ldq, bool fullTriangle=true, bool multiplyQ=false )

   Computes the eigenvalues (and possibly the full Schur factor) as well as 
   the Schur vectors of of an upper Hessenberg matrix using the QR algorithm.
   If `multiplyQ` is true, then the Schur vectors are multiplied against the
   input matrix from the right.

Hessenberg eigenvalues/pairs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. cpp:function:: void lapack::HessenbergEig( int n, F* H, int ldh, Complex<Base<F>>* w )

   Computes the eigenvalues of an upper Hessenberg matrix using the QR 
   algorithm.

.. note::

   There are not yet wrappers for computing Hessenberg eigenvectors.

Schur decomposition
^^^^^^^^^^^^^^^^^^^

.. cpp:function:: void lapack::Schur( int n, F* A, int lda, Complex<Base<F>>* w, bool fullTriangle=false )

   Returns the eigenvalues (and possibly also the Schur factor) of a square 
   matrix using the QR algorithm.

.. cpp:function:: void lapack::Schur( int n, F* A, int lda, Complex<Base<F>>* w, F* Q, int ldq, bool fullTriangle=true )

   Returns the Schur decomposition of a square matrix using the QR algorithm.

Eigenvalues/pairs
^^^^^^^^^^^^^^^^^

.. cpp:function:: void lapack::Eig( int n, F* A, int lda, Complex<Base<F>>* w )

   Returns the eigenvalues of a square matrix using the QR algorithm.

.. note::

   There are not yet wrappers for computing general eigenvectors.
