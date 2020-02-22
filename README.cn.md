# 像素攻击Web端

“像素攻击”是一个对抗攻击工具。本项目是它的后端。

## 内容列表

- [特性](#特性)
- [使用说明](#使用说明)
- [参考资料](#参考资料)
- [使用许可](#使用许可)

## 特性

- 为基于神经网络的图像分类设计
- 极少被改变的像素
- 非针对性的攻击

## 使用说明

如果你想要启用https，请提供适当的.pem文件.key文件，并修改app.py。

``` python
# berfore: app.run(host='0.0.0.0', port=50001, ssl_context=('api.peaceandlove.top.pem', 'api.peaceandlove.top.key'))
app.run(host='0.0.0.0', port=50001, ssl_context=('your.pem', 'your.key'))
```

如果你不想启用https，只要修改app.py。
``` python
# berfore: app.run(host='0.0.0.0', port=50001, ssl_context=('api.peaceandlove.top.pem', 'api.peaceandlove.top.key'))
app.run(host='0.0.0.0', port=50001)
```

如果你想要跨域，请修改app.py。
``` python
# berfore: if origin.endswith('peaceandlove.top'):
if origin == 'your.own.domain':
```

最后，你就可以启动项目了。
``` shell script
python3 app.py
```

## 参考资料

- 论文： [One Pixel Attack for Fooling Deep Neural Networks](https://ieeexplore.ieee.org/document/8601309)
- 项目： [one-pixel-attack-keras](https://github.com/Hyperparticle/one-pixel-attack-keras)
- Tensorflow教程： [Convolutional Neural Network](https://www.tensorflow.org/tutorials/images/cnn)

## 使用许可

[MIT](LICENSE) © Peidong Xie
