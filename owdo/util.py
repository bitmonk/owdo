#!/usr/bin/env python

import logging, time

from owdo.connection import ow

def get_all_stacks(ow):
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

def deploy_and_wait(stack_id, instance_ids, command_name):
  depl_id = ow.create_deployment(
    stack_id = stack_id,
    instance_ids = instance_ids,
    command = {
      'Name': command_name,
    }
  )['DeploymentId']

  done = False
  logging.warning("waiting for %s (%s)" % (command_name, depl_id))
  while not done:
    depl = ow.describe_deployments(
      deployment_ids=[depl_id,]
    )['Deployments'][0]
    logging.debug("deployment: %s" % depl)
    if depl['Status'] == u'running':
      time.sleep(5)
    else:
      # fix race condition here, initial status may not be "running"
      done = True
  return depl_id

