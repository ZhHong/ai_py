'''
tensorflow模型持久化
'''

import tensorflow as tf


def dump():
    v1 = tf.Variable(tf.constant(1.0,dtype=tf.float32,shape=[1],name = "v1"))
    v2 = tf.Variable(tf.constant(2.0,dtype=tf.float32,shape=[1],name = "v2"))

    saver = tf.train.Saver()

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver.export_meta_graph("dump/model/model.ckpt.meta.json",as_text=True)
        saver.save(sess,'dump/model/model.ckpt')

def load():
    v1 = tf.Variable(tf.constant(1.0,dtype=tf.float32,shape =[1],name = "v1"))
    v2 = tf.Variable(tf.constant(2.0,dtype = tf.float32,shape=[1],name = "v2"))

    r = v1 +v2
    saver = tf.train.Saver()

    with tf.Session() as sess:
        saver.restore(sess,"dump/model/model.ckpt")
        print(sess.run(r))

def load2():
    saver = tf.train.import_meta_graph("dump/model/model.ckpt.meta")

    with tf.Session() as sess:
        saver.restore(sess,"dump/model/model.ckpt")
        print(sess.run(tf.get_default_graph().get_tensor_by_name("add:0")))
def main(args = None):
    dump()
    # load()
    # load2()
if __name__ == '__main__':
    tf.app.run()