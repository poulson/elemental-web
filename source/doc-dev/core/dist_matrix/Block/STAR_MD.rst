``[STAR,MD]``
=============
In the case of our :math:`2 \times 3` process grid, each diagonal of the
tesselation of the process grid will contain the entire set of processes,
for instance, in the order :math:`0,3,4,1,2,5`. This would result in the 
following overlay for the owning processes of the subblocks of our
:math:`7 \times 7` block matrix example:

.. math::

   \left(\begin{array}{ccccccc}
     0 & 3 & 4 & 1 & 2 & 5 & 0 \\
     0 & 3 & 4 & 1 & 2 & 5 & 0 \\
     0 & 3 & 4 & 1 & 2 & 5 & 0 \\
     0 & 3 & 4 & 1 & 2 & 5 & 0 \\
     0 & 3 & 4 & 1 & 2 & 5 & 0 \\
     0 & 3 & 4 & 1 & 2 & 5 & 0 \\
     0 & 3 & 4 & 1 & 2 & 5 & 0 
   \end{array}\right)

Notice that each *block row* of this matrix is distributed like a diagonal of a 
``[MC,MR]`` distribution.

.. cpp:class:: DistMatrix<scalarType,STAR,MD,BLOCK>
