from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
# github.com/caicloud/tensorflow-tutorial
# cargo.caicloud.io/tensorflow/tensorflow:0.12.0
# mnist = input_data.read_data_sets('MNIST_data',one_hot=True)

# print("Train Data Shape             :",mnist.train.images.shape)
# print("Train Data Size              :",mnist.train.num_examples)
# print("Validating Data Size         :",mnist.validation.num_examples)
# print("Testing Data Size            :",mnist.test.num_examples)
# print("Example trainning data label :",mnist.train.labels[0])

# batch_size =100

# xs,ys = mnist.train.next_batch(batch_size)

# print("X Shape :",xs.shape)
# print("Y Shape :",ys.shape)
#输入层的节点数
INPUT_NODE = 784
#输出层的节点数
OUTPUT_NODE = 10
#隐藏节点数
LAYER1_NODE = 500
#一次训练的数据个数
BATCH_SIZE = 100
#基础学习率
LEARNING_RATE_BASE = 0.8
#学习率的衰减率
LEARNING_RATE_DECAY = 0.99
#损失函数系数
REGULARIZATION_RATE = 0.0001
#训练轮数
TRAINNING_STEPS = 30000
#滑动平均衰减率
MOVING_AVERAGE_DECAY = 0.99

def interface(input_tensor,avg_class,weights1,biases1,weights2,biases2):
    '''
    '''
    if avg_class == None:
        layer1 = tf.nn.relu(tf.matmul(input_tensor,weights1) +biases1)
        return tf.matmul(layer1,weights2)+biases2
    else:
        layer1 = tf.nn.relu(tf.matmul(input_tensor,avg_class.average(weights1)) + avg_class.average(biases1))
        return tf.matmul(layer1,avg_class.average(weights2))+avg_class.average(biases2)

def train(mnist):
    '''
    '''
    x = tf.placeholder(tf.float32,[None,INPUT_NODE],name = 'input-x')
    y_= tf.placeholder(tf.float32,[None,OUTPUT_NODE],name = 'input-y')

    #隐藏层参数
    weights1 = tf.Variable(tf.truncated_normal([INPUT_NODE,LAYER1_NODE],stddev=0.1))
    biases1 = tf.Variable(tf.constant(0.1,shape =[LAYER1_NODE]))
    #输出层参数
    weights2 = tf.Variable(tf.truncated_normal([LAYER1_NODE,OUTPUT_NODE],stddev=0.1))
    biases2 = tf.Variable(tf.constant(0.1,shape=[OUTPUT_NODE]))

    y = interface(x,None,weights1,biases1,weights2,biases2)

    #训练轮数变量 不参与训练
    global_step = tf.Variable(0,trainable=False)

    variable_average = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY,global_step)

    variable_averages_op = variable_average.apply(tf.trainable_variables())
    average_y = interface(x,variable_average,weights1,biases1,weights2,biases2)

    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y,labels = tf.arg_max(y_,1))

    cross_entropy_mean = tf.reduce_mean(cross_entropy)

    #计算L2正则化损失函数
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)

    regularization = regularizer(weights1)+regularizer(weights2)

    loss = cross_entropy_mean +regularization

    leaning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE,global_step,mnist.train.num_examples/BATCH_SIZE,LEARNING_RATE_DECAY)

    train_step = tf.train.GradientDescentOptimizer(leaning_rate).minimize(loss,global_step=global_step)

    with tf.control_dependencies([train_step,variable_averages_op]):
        train_op = tf.no_op(name ='train')

    corrrect_prediction =  tf.equal(tf.arg_max(average_y,1),tf.arg_min(y_,1))
    accuracy = tf.reduce_mean(tf.cast(corrrect_prediction,tf.float32))

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        validate_feed = {x:mnist.validation.images,y_:mnist.validation.labels}
        test_feed = {x:mnist.test.images,y_:mnist.test.labels}

        for i in range(TRAINNING_STEPS):
            if i%1000 ==0:
                validate_acc = sess.run(accuracy,feed_dict=validate_feed)
                test_acc = sess.run(accuracy,feed_dict=test_feed)
                print("After %d steps train,validation accuracy using average model is %g,test accuracy using average model is %g"%(i,validate_acc,test_acc))

                xs,ys = mnist.train.next_batch(BATCH_SIZE)
                sess.run(train_op,feed_dict={x:xs,y_:ys})
        
        test_acc = sess.run(accuracy,feed_dict=test_feed)
        print("After %d steps train, test accuracy using average model is %g"%(TRAINNING_STEPS,test_acc))

def main(argv = None):
    '''
    '''
    mnist = input_data.read_data_sets("MNIST_data",one_hot=True)
    train(mnist)
    

if __name__ == '__main__':
    tf.app.run()