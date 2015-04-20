
from owdo.connection import ow

class OWStack:
  def __init__(self, ow, name):
    stack_list = ow.describe_stacks()['Stacks']
    stacks = {}

    for stack in stack_list:
      stacks[stack['Name']] = stack

    self._stack_list = stack_list
    self._stacks = stacks

    self._stack = stacks[name]

  def __getitem__(self, key):
    return self._stack[key]

  def __iter__(self):
    for key in self._stack:
      yield self._stack[key]

class OWLayer:
  def __init__(self, ow, stack, name):
    layer_list =  ow.describe_layers(stack['StackId'])['Layers']
    layers = {}
    for layer in layer_list:
      layers[layer['Name']] = layer

    self._layer_list = layer_list
    self._layers = layers
    self._layer = layers[name]

  def __getitem__(self, key):
    return self._layer[key]

  def __iter__(self):
    for key in self._layer:
      yield self._layer[key]

