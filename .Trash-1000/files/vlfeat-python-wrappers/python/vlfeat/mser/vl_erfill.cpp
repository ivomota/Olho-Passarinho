/**
 ** @author   Andrea Vedaldi
 ** @author   Mikael Rousson (Python wrapping)
 ** @brief    Extremal Regions filling
 **/

#include "../py_vlfeat.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <assert.h>

extern "C" {
#include <src/generic-driver.h>
#include <vl/generic.h>
#include <vl/stringop.h>
#include <vl/pgm.h>
#include <vl/mser.h>
}

#define MIN(x,y) (((x)<(y))?(x):(y))
#define MAX(x,y) (((x)>(y))?(x):(y))

typedef char unsigned val_t;
typedef int unsigned idx_t;
typedef vl_uint64 acc_t;

/* advance N-dimensional subscript */
void adv(int const* dims, int ndims, int* subs_pt)
{
	int d = 0;
	while (d < ndims) {
		if (++subs_pt[d] < dims[d])
			return;
		subs_pt[d++] = 0;
	}
}

/* driver */
PyObject * vl_erfill_python(PyArrayObject & image, double seed)
{
	// check types
	assert(image.descr->type_num == PyArray_UBYTE);
	assert(image.flags & NPY_FORTRAN);
	assert(image.nd == 2 || image.nd == 3);

	enum
	{
		IN_I = 0, IN_ER
	};
	enum
	{
		OUT_MEMBERS
	};

	idx_t i;
	int k, nel, ndims;
	int const dims[] = {image.dimensions[0], image.dimensions[1]};
	val_t const * I_pt;
	int last = 0;
	int last_expanded = 0;
	val_t value = 0;

	double const * er_pt;

	int* subs_pt; /* N-dimensional subscript                 */
	int* nsubs_pt; /* diff-subscript to point to neigh.       */
	idx_t* strides_pt; /* strides to move in image array          */
	val_t* visited_pt; /* flag                                    */
	idx_t* members_pt; /* region members                          */


	/* get dimensions */
	nel = image.dimensions[0] * image.dimensions[1];
	ndims = image.nd;
	I_pt = (val_t const *) image.data;

	/* allocate stuff */
	subs_pt = new int[ndims];
	nsubs_pt = new int[ndims];
	strides_pt = new idx_t[ndims];
	visited_pt = new val_t[nel];
	members_pt = new idx_t[nel];

	er_pt = &seed;

	/* compute strides to move into the N-dimensional image array */
	strides_pt[0] = 1;
	for (k = 1; k < ndims; ++k) {
		strides_pt[k] = strides_pt[k - 1] * dims[k - 1];
	}

	/* load first pixel */
	memset(visited_pt, 0, sizeof(val_t) * nel);
	{
		idx_t idx = (idx_t) *er_pt;
		if (idx < 1 || idx > nel) {
			char buff[80];
			printf("ER=%d out of range [1,%d]", idx, nel);
		}
		members_pt[last++] = idx;
	}
	value = I_pt[members_pt[0]];

	/* -----------------------------------------------------------------
	 *                                                       Fill region
	 * -------------------------------------------------------------- */
	while (last_expanded < last) {

		/* pop next node xi */
		idx_t index = members_pt[last_expanded++];

		/* convert index into a subscript sub; also initialize nsubs
		 to (-1,-1,...,-1) */
		{
			idx_t temp = index;
			for (k = ndims - 1; k >= 0; --k) {
				nsubs_pt[k] = -1;
				subs_pt[k] = temp / strides_pt[k];
				temp = temp % strides_pt[k];
			}
		}

		/* process neighbors of xi */
		while (true) {
			int good = true;
			idx_t nindex = 0;

			/* compute NSUBS+SUB, the correspoinding neighbor index NINDEX
			 and check that the pixel is within image boundaries. */
			for (k = 0; k < ndims && good; ++k) {
				int temp = nsubs_pt[k] + subs_pt[k];
				good &= 0 <= temp && temp < dims[k];
				nindex += temp * strides_pt[k];
			}

			/* process neighbor
			 1 - the pixel is within image boundaries;
			 2 - the pixel is indeed different from the current node
			 (this happens when nsub=(0,0,...,0));
			 3 - the pixel has value not greather than val
			 is a pixel older than xi
			 4 - the pixel has not been visited yet
			 */
			if (good && nindex != index && I_pt[nindex] <= value
					&& !visited_pt[nindex]) {

				/* mark as visited */
				visited_pt[nindex] = 1;

				/* add to list */
				members_pt[last++] = nindex;
			}

			/* move to next neighbor */
			k = 0;
			while (++nsubs_pt[k] > 1) {
				nsubs_pt[k++] = -1;
				if (k == ndims)
					goto done_all_neighbors;
			}
		} /* next neighbor */
		done_all_neighbors: ;
	} /* goto pop next member */

	/*
	 * Save results
	 */
	npy_intp _last = (npy_intp) last;
	PyArrayObject * res = (PyArrayObject*) PyArray_SimpleNew(
		1, (npy_intp*) &_last, PyArray_UINT);

	unsigned int * res_buffer = (unsigned int *) res->data;
	for (i = 0; i < last; ++i) {
		res_buffer[i] = members_pt[i];// + 1;
	}

	/* free stuff */
	delete[] members_pt;
	delete[] visited_pt;
	delete[] strides_pt;
	delete[] nsubs_pt;
	delete[] subs_pt;

	return PyArray_Return(res);
}
