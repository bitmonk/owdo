#!/usr/bin/env python

import logging, time

from owdo.connection import ow
from owdo.util import deploy_and_wait

stack_list = ow.describe_stacks()['Stacks']
stacks = {}
for stack in stack_list:
  stacks[stack['Name']] = stack
  layer_list =  ow.describe_layers(stack['StackId'])['Layers']
  layers = {}
  for layer in layer_list:
    layers[layer['Name']] = layer
    instance_list = ow.describe_instances(layer_id=layer['LayerId'])['Instances']
    instances = {}
    id_instances = {}
    for instance in instance_list:
      id_instances[instance['InstanceId']] = instance
      try:
        instances[instance['Hostname']] = instance
      except:
        pass
    layer['id_instances'] = id_instances
    layer['instances'] = instances
  stacks[stack['Name']]['layers'] = layers

ot = stacks['opstest']
hop = ot['layers']['http outbound proxy']
nas = ot['layers']['nodejs app']
m = ot['layers']['monitoring']
h = ot['layers']['honeypot']
#rw = ot['layers']['raw web']

o = h['instances']['okamuro']
#a1 = nas['instances']['opstest-nodejs-app01']
#a2 = nas['instances']['opstest-nodejs-app02']
#a3 = nas['instances']['opstest-nodejs-app03']
