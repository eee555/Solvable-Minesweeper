import ms_toollib
import matplotlib.image as mpimg
import numpy as np
file = r'C:\Users\jia32\Desktop\无标题.png'# 彩色图片
lena = mpimg.imread(file)
(height, width) = lena.shape[:2]
lena = np.concatenate((lena, 255.0 * np.ones((height, width, 1))), 2)
lena = (np.reshape(lena, -1) * 255).astype(np.uint32)
board = ms_toollib.py_OBR_board(lena, height, width)
print(np.array(board))# 打印识别出的局面
poss = ms_toollib.py_cal_possibility(board, 99)
print(poss)# 用雷的总数计算概率
poss_onboard = ms_toollib.py_cal_possibility_onboard(board, 99)
print(poss_onboard)# 用雷的总数计算概率，输出局面对应的位置
poss_ = ms_toollib.py_cal_possibility_onboard(board, 0.20625)
print(poss_)# 用雷的密度计算概率