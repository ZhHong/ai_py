'''
    gen self profile
    IPython
    python version 3.5.3
    tensorflow version 1.2.0
    numpy version 1.13.0
    ipython version 6.1.0
    PIL not suport python 3.x use Pillow instead;
    Pillow version 4.1.1
    scipy version  0.19.0  download from  http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy
    MKLpy version -- user num+mkl version 1.13.0 download from  http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy
    base code from book and modified https://www.tensorflow.org/tutorials/mandelbrot
'''
import tensorflow as tf
import numpy as np
import PIL.Image
from io import BytesIO
from IPython.display import clear_output, Image, display
import scipy.ndimage as nd

def show_profile(a, fmt='jpeg'):
    """
    gen jpeg profile
    """
    a_cyclic = (15.55 * a / 25.5).reshape(list(a.shape) + [1])
    img = np.concatenate([15 + 25 * np.cos(a_cyclic),
                          35 + 25 * np.sin(a_cyclic),
                          155 - 55 * np.cos(a_cyclic)], 2)
    img[a == a.max()] = 0
    a = img
    a = np.uint8(np.clip(a, 0, 255))
    f = BytesIO()
    PIL.Image.fromarray(a).save("Profile.jpeg", fmt)
    # display(Image(data = f.getvalue()))

def main():
    sess = tf.InteractiveSession()
    Y,X =np.mgrid[-1.5:1.5:0.0015,-2.5:1.5:0.0015]
    Z =X+1j*Y

    xs = tf.constant(Z.astype("complex64"))
    zs = tf.Variable(xs);
    ns = tf.Variable(tf.zeros_like(xs,"float32"))

    tf.global_variables_initializer().run()

    zs_ = zs *zs+xs;
    # not_diverged = tf.complex_abs(zs_) <4;
    not_diverged = tf.abs(zs_) <5;

    step = tf.group(
        zs.assign(zs_),
        ns.assign_add(tf.cast(not_diverged,"float32"))
    )

    for i in range(523):
        step.run()
    
    show_profile(ns.eval());


if __name__ == '__main__':
    main()