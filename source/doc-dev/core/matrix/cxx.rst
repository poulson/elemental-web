Matrix (C++ interface)
======================
The :cpp:type:`Matrix\<scalarType>` class is the building of the library:
its purpose is to provide convenient mechanisms for performing basic matrix 
manipulations, such as setting and querying individual matrix entries, 
without giving up compatibility with interfaces such as BLAS and LAPACK, 
which assume column-major storage.

An example of generating an :math:`m \times n` matrix of real double-precision 
numbers where the :math:`(i,j)` entry is equal to :math:`i-j` would be:

  .. code-block:: cpp

     #include "El.hpp"
     using namespace El;
     ...
     Matrix<double> A( m, n );
     for( Int j=0; j<n; ++j )
         for( Int i=0; i<m; ++i )
             A.Set( i, j, double(i-j) );

whereas the complex double-precision equivalent could use :cpp:type:`Complex\<double>`, which is currently a typedef for ``std::complex<double>``.
     
The underlying data storage for :cpp:class:`Matrix\<scalarType>` is simply a
contiguous buffer that stores entries in a column-major fashion with a *leading 
dimension* which is only required to be at least as large as the height of the 
matrix (so that entry :math:`(i,j)` is located at position ``i+j*ldim``). 
For modifiable instances of the :cpp:class:`Matrix\<scalarType>` class,
the routine
:cpp:func:`Matrix\<scalarType>::Buffer` returns a pointer to the underlying 
buffer, while :cpp:func:`Matrix\<scalarType>::LDim` returns the leading 
dimension; these two routines could be used to directly perform the equivalent
of the first code sample as follows:

  .. code-block:: cpp
     
     #include "El.hpp"
     using namespace El;
     ...
     Matrix<double> A( m, n );
     double* buffer = A.Buffer();
     const Int ldim = A.LDim();
     for( Int j=0; j<n; ++j )
         for( Int i=0; i<m; ++i )
             buffer[i+j*ldim] = double(i-j);

For immutable instances of the :cpp:class:`Matrix\<scalarType>` class, a
``const`` 
pointer to the underlying data can similarly be returned with a call to 
:cpp:func:`Matrix\<scalarType>::LockedBuffer`.
In addition, a (``const``) pointer to the place in the 
(``const``) buffer where entry :math:`(i,j)` resides can be easily retrieved
with a call to :cpp:func:`Matrix\<scalarType>::Buffer` or 
:cpp:func:`Matrix\<scalarType>::LockedBuffer`.

It is also important to be able to create matrices which are simply *views* 
of existing (sub)matrices. In general, to view the submatrix with row indices 
:math:`[\text{iBeg},\text{iEnd}]` and column indices 
:math:`[\text{jBeg},\text{jEnd}]`, one can use a statement of the form

  .. code-block:: cpp

     #include "El.hpp"
     ...
     auto ASub = A( IR(iBeg,iEnd), IR(jBeg,jEnd) );

.. cpp:class:: Matrix<scalarType>

   The goal is for the `Matrix` class to support any datatype `scalarType` which
   supports both addition and multiplication and has the associated identities
   (that is, when the datatype `scalarType` is a *ring*). While there are
   several barriers to reaching this goal, it is important to keep in mind that,
   in addition to `scalarType` being allowed to be a real or complex 
   (single- or double-precision) floating-point type, signed integers 
   are also supported.

   .. rubric:: Constructors and destructors

   .. note::

      Many of the following constructors have the default parameter
      ``bool fixed=false``, which can be changed to ``true`` in order to 
      produce a `Matrix` whose entries can be modified, but the matrix's 
      dimensions cannot. This is useful for the
      :cpp:class:`DistMatrix\<scalarType>` 
      class, which contains a local :cpp:class:`Matrix\<scalarType>` whose
      entries can be locally modified in cases where it would not make sense to
      change the local matrix size (which should instead result from changing
      the size of the full distributed matrix).

   .. cpp:function:: Matrix( bool fixed=false )

      This simply creates a default :math:`0 \times 0` matrix with a leading 
      dimension of one (BLAS and LAPACK require positive leading dimensions).

   .. cpp:function:: Matrix( Int height, Int width, bool fixed=false )

      A `height` :math:`\times` `width` matrix is created with an unspecified
      leading dimension (though it is currently implemented as 
      :math:`\max(height,1)`).

   .. cpp:function:: Matrix( Int height, Int width, Int ldim, bool fixed=false )

      A `height` :math:`\times` `width` matrix is created with a leading 
      dimension equal to `ldim` (which must be greater than or equal 
      :math:`\max(height,1)`).

   .. cpp:function:: Matrix( Int height, Int width, const scalarType* buffer, Int ldim, bool fixed=false )
   .. cpp:function:: Matrix( Int height, Int width, scalarType* buffer, Int ldim, bool fixed=false )

      A matrix is built around a column-major (immutable) buffer 
      with the specified dimensions. The memory pointed to by `buffer` should
      not be freed until after the :cpp:class:`Matrix\<scalarType>` object is destructed.

   .. cpp:function:: Matrix( const Matrix<scalarType>& A )

      A copy (not a view) of the matrix :math:`A` is built.

   .. cpp:function:: Matrix( Matrix<scalarType>&& A ) noexcept

      A C++11 move constructor which creates a new matrix by moving the metadata
      from the specified matrix over to the new matrix, which cheaply gives the
      new matrix control over the resources originally assigned to the input
      matrix.

   .. cpp:function:: ~Matrix()

      Frees all resources owned by the matrix upon destruction.

   .. rubric:: Submatrices

   .. cpp:function:: Matrix<scalarType> operator()( Range<Int> I, Range<Int> J )
   .. cpp:function:: const Matrix<scalarType> operator()( Range<Int> I, Range<Int> J ) const

      Return a view of a contiguous submatrix with the given row and column
      index ranges.

   .. cpp:function:: Matrix<scalarType> operator()( Range<Int> I, const vector<Int>& J ) const
   .. cpp:function:: Matrix<scalarType> operator()( const vector<Int>& I, Range<Int> J ) const
   .. cpp:function:: Matrix<scalarType> operator()( const vector<Int>& I, const vector<Int>& J ) const

      Return a copy of the (generally non-contiguous) submatrix given by the
      specified row and column index lists.

   .. rubric:: Assignment and reconfiguration

   .. cpp:function:: const Matrix<scalarType>& operator=( const Matrix<scalarType>& A )

      Create a full copy of the specified matrix.

   .. cpp:function:: Matrix<scalarType>& operator=( Matrix<scalarType>&& A )

      A C++11 move assignment which swaps the metadata of two matrices so that
      the resources owned by the two objects will have been cheaply
      switched.

   .. cpp:function:: void Empty()

      Sets the matrix to :math:`0 \times 0` and frees any owned resources.

   .. cpp:function:: void Resize( Int height, Int width )

      Reconfigures the matrix to be `height` :math:`\times` `width`.

   .. cpp:function:: void Resize( Int height, Int width, Int ldim )

      Reconfigures the matrix to be `height` :math:`\times` `width`, but with 
      leading dimension equal to `ldim` (which must be greater than or equal to 
      :math:`\max(height,1)`).

   .. cpp:function:: void Attach( Int height, Int width, scalarType* buffer, Int ldim )
   .. cpp:function:: void LockedAttach( Int height, Int width, const scalarType* buffer, Int ldim )

      Reconfigure the matrix around the specified (unmodifiable) buffer.

   .. cpp:function:: void Control( Int height, Int width, scalarType* buffer, Int ldim )

      Reconfigure the matrix around a specified buffer and give ownership of
      the resource to the matrix.

   .. rubric:: Basic queries

   .. cpp:function:: Int Height() const
   .. cpp:function:: Int Width() const

      Return the height/width of the matrix.

   .. cpp:function:: Int LDim() const

      Return the leading dimension of the underlying buffer.

   .. cpp:function:: Int MemorySize() const

      Return the number of entries of type `scalarType` that this :cpp:class:`Matrix\<scalarType>`
      instance has allocated space for.

   .. cpp:function:: Int DiagonalLength( Int offset=0 ) const

      Return the length of the specified diagonal of the matrix: an offset of 
      :math:`0` refers to the main diagonal, an offset of :math:`1` refers to 
      the superdiagonal, an offset of :math:`-1` refers to the subdiagonal, 
      etc.

   .. cpp:function:: scalarType* Buffer()
   .. cpp:function:: const scalarType* LockedBuffer() const

      Return a pointer to the (immutable) underlying buffer.

   .. cpp:function:: scalarType* Buffer( Int i, Int j )
   .. cpp:function:: const scalarType* LockedBuffer( Int i, Int j ) const

      Return a pointer to the (immutable) portion of the buffer that holds entry
      :math:`(i,j)`.

   .. cpp:function:: bool Viewing() const

      Returns `true` if the underlying buffer is merely a pointer into an 
      externally-owned buffer.

   .. cpp:function:: bool FixedSize() const

      Returns `true` if the dimensions of the matrix cannot be changed.

   .. cpp:function:: bool Locked() const

      Returns `true` if the entries of the matrix cannot be changed.

   .. rubric:: Single-entry manipulation

   .. cpp:function:: scalarType Get( Int i, Int j ) const
   .. cpp:function:: Base<scalarType> GetRealPart( Int i, Int j ) const
   .. cpp:function:: Base<scalarType> GetImagPart( Int i, Int j ) const

      Return entry :math:`(i,j)` (or its real or imaginary part).

   .. cpp:function:: void Set( Int i, Int j, scalarType alpha )
   .. cpp:function:: void SetRealPart( Int i, Int j, Base<scalarType> alpha )
   .. cpp:function:: void SetImagPart( Int i, Int j, Base<scalarType> alpha )

      Set entry :math:`(i,j)` (or its real or imaginary part) to :math:`\alpha`.

   .. cpp:function:: void Update( Int i, Int j, scalarType alpha )
   .. cpp:function:: void UpdateRealPart( Int i, Int j, Base<scalarType> alpha )
   .. cpp:function:: void UpdateImagPart( Int i, Int j, Base<scalarType> alpha ) 

      Add :math:`\alpha` to entry :math:`(i,j)` (or its real or imaginary part).

   .. cpp:function:: void MakeReal( Int i, Int j )
 
      Force the :math:`(i,j)` entry to be real.

   .. cpp:function:: void Conjugate( Int i, Int j )

      Conjugate the :math:`(i,j)` entry of the matrix.

Special cases used in Elemental
-------------------------------
This list of special cases is here to help clarify the notation used throughout
Elemental's source (as well as this documentation). These are all special
cases of :cpp:class:`Matrix\<scalarType>`.

.. cpp:class:: Matrix<Real>

   Used to denote that the underlying datatype `Real` is real.

.. cpp:class:: Matrix<Complex<Real> >

   Used to denote that the underlying datatype :cpp:type:`Complex\<Real>` is
   complex with base type `Real`.

.. cpp:class:: Matrix<F>

   Used to denote that the underlying datatype `F` is a field.

.. cpp:class:: Matrix<Int>

   When the underlying datatype is a signed integer.

