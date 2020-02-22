from numpy import argmax, expand_dims, split, tile
from scipy.optimize import differential_evolution


def affect_predictions(image, model, perturbations, colorful, normalized):
    if perturbations.ndim == 1:
        perturbations = expand_dims(perturbations, 0)
    if colorful:
        images = tile(image, (len(perturbations), 1, 1, 1))
        for image, perturbation in zip(images, perturbations):
            pixels = split(perturbation, len(perturbation) // 5)
            for pixel in pixels:
                x, y, *value = pixel
                value[0] = int(value[0]) / 255.0
                value[1] = int(value[1]) / 255.0
                value[2] = int(value[2]) / 255.0
                image[int(x), int(y)] = value
    else:
        images = tile(image, (len(perturbations), 1, 1))
        for image, perturbation in zip(images, perturbations):
            pixels = split(perturbation, len(perturbation) // 3)
            for pixel in pixels:
                x, y, value = pixel
                image[int(x), int(y)] = int(value) / 255.0
    if not normalized:
        images = (images * 255.0).astype('uint8')
    predictions = model.predict(images)
    return predictions


def create_func(image, model, label, colorful, normalized):
    def func(perturbations):
        return affect_predictions(image, model, perturbations, colorful, normalized)[:, label]

    return func


def create_callback(image, model, label, colorful, normalized):
    def callback(perturbations, convergence):
        if argmax(affect_predictions(image, model, perturbations, colorful, normalized)[0]) != label:
            return True

    return callback


def attack(image, model, label, count, normalized):
    width, height, *color = image.shape
    colorful = len(color) != 0
    if normalized:
        prediction = model.predict(expand_dims(image, 0))[0]
    else:
        prediction = model.predict(expand_dims((image * 255.0).astype('uint8'), 0))[0]
    if label == -1:
        label = int(argmax(prediction))
    result = differential_evolution(func=create_func(image, model, label, colorful, normalized),
                                    bounds=([(0, width), (0, height)] + [(0, 256)] * (3 if colorful else 1)) * count,
                                    args=(),
                                    strategy='best1bin',
                                    maxiter=60,
                                    popsize=60 // count,
                                    tol=0.01,
                                    mutation=(0.5, 1),
                                    recombination=1,
                                    seed=None,
                                    callback=create_callback(image, model, label, colorful, normalized),
                                    disp=False,
                                    polish=False,
                                    init='latinhypercube',
                                    atol=-1,
                                    updating='immediate',
                                    workers=1)
    perturbation = result.x.astype('uint8')
    affected_prediction = affect_predictions(image, model, perturbation, colorful, normalized)[0]
    pixels = split(perturbation.astype(int), count)
    perturbation = []
    for pixel in pixels:
        x, y, *value = pixel.tolist()
        perturbation.append({'x': x, 'y': y, 'value': value * (3 // len(value))})
    return width, height, label, prediction, perturbation, affected_prediction
