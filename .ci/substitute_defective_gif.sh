#!/bin/bash
cd doc/_build/html/examples/gallery_examples/00-mapdl-examples || exit 1
cp ../../../../../source/images/dcb.gif ../../../_images/
sed -i 's+../../../_images/sphx_glr_composite_dcb_004.gif+../../../_images/dcb.gif+g' composite_dcb.html
cd ../../../../../../  || exit 1