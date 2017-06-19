import numpy as np


def numpy_property():
    '''
    '''
    a = np.arange(20).reshape(4,5);
    ### arange(20) ===>return array([1,...20]) int的一维数组
    ### reshape(4,5) ===>指定形状
    
    ### a.ndim =2
    ### a.shape =(4,5)
    ### a.itemsize =4
    ### a.size =20
    ### a.dtype =dtype('int32')

    b= np.array([
        [
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ],
        [
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ],
        [
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ],
    ])

    ### b.ndim = 3
    ### b.shape = (3,3,3)
    ### b.itemsize =4
    ### b.size = 27
    ### b.dtype =dtype('int32')

    c= np.array([
        [
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ],
        [
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ],
        [
            [1,2,3],
        ],
    ])

    ### c.ndim  =1 (这里会把不规则的列表当成一个元素)
    ### c.shape = (3,) (数组不规则，数组的后续长度无法确定)
    ### c.itemsize =8 (item变成的object)
    ### c.size =3 
    ### c.dtype =dtype('O') 'Object'

def main():
    numpy_property();

if __name__ == '__main__':
    main()