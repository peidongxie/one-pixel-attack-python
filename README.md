# One-Pixel-Attack-Web

'One Pixel Attack' is a tool for adversarial attacks. The project is the back end of it. 

## Table of Contents

- [Features](#Features)
- [Usage](#Usage)
- [References](#References)
- [License](#License)

## Features

- Designed for image classification with neural networks
- Very few pixels modified
- Untargeted attacks

## Usage

If you want to enable https, please provide the appropriate '.pem' file and '.key' file, and modify 'app.py'.

``` python
# berfore: app.run(host='0.0.0.0', port=50001, ssl_context=('api.peaceandlove.top.pem', 'api.peaceandlove.top.key'))
app.run(host='0.0.0.0', port=50001, ssl_context=('your.pem', 'your.key'))
```

If not, just modify 'app.py'.
``` python
# berfore: app.run(host='0.0.0.0', port=50001, ssl_context=('api.peaceandlove.top.pem', 'api.peaceandlove.top.key'))
app.run(host='0.0.0.0', port=50001)
```

If you want to cross domain, please modify 'app.py'.
``` python
# berfore: if origin.endswith('peaceandlove.top'):
if origin == 'your.own.domain':
```

Finally, you can start the project.
``` shell script
python3 app.py
```

## References

- Paper: [One Pixel Attack for Fooling Deep Neural Networks](https://ieeexplore.ieee.org/document/8601309)
- Project: [one-pixel-attack-keras](https://github.com/Hyperparticle/one-pixel-attack-keras)
- Tensorflow Tutorials: [Convolutional Neural Network](https://www.tensorflow.org/tutorials/images/cnn)

## License

[MIT](LICENSE) © Peidong Xie
