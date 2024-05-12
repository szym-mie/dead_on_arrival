(let* ((image (car (gimp-file-load RUN-NONINTERACTIVE \"$in\" \"$in\")))
       (drawable (car (gimp-image-get-active-layer image))))
  (gimp-file-save RUN-NONINTERACTIVE image drawable \"$out\" \"$out\"))