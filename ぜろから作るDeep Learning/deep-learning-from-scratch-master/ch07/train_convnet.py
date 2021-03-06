
import sys, os
sys.path.append(os.pardir)
import numpy as np
import matplotlib.pyplot as plt
from dataset.mnist import load_mnist
from simple_convnet import SimpleConvNet
from common.trainer import Trainer

# データの読み込み
(x_train, t_train), (x_test, t_test) = load_mnist(flatten=False)


max_epochs = 20

network = SimpleConvNet(input_dim=(1,28,28), 
                        conv_param = {'filter_num': 30, 'filter_size': 5, 'pad': 0, 'stride': 1},
                        hidden_size=100, output_size=10, weight_init_std=0.01)
                        
trainer = Trainer(network, x_train, t_train, x_test, t_test,
                  epochs=max_epochs, mini_batch_size=100,
                  optimizer='Adam', optimizer_param={'lr': 0.001},
                  evaluate_sample_num_per_epoch=1000)
trainer.train()

# パラメータの保存
network.save_params("params.pkl")
print("Saved Network Parameters!")

# グラフの描画
markers = {'train': 'o', 'test': 's'}
x = np.arange(max_epochs)
plt.plot(x, trainer.train_acc_list,color = (0,0,1), marker='o', label='train', markevery=1)
plt.plot(x, trainer.test_acc_list,color=(1,0,0), marker='s', label='test', markevery=1)
plt.xlabel("Epochs",fontsize = 60)
plt.ylabel("Accuracy",fontsize = 60)
plt.hlines(1,0,max_epochs,linestyle = "dashed")
plt.ylim(0, 1.3)
plt.legend(loc='lower right',fontsize=60, title= "LABEL NAME")
plt.show()
