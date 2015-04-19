#!/usr/bin/env python

import logging, time

REGION = 'us-east-1'

import boto.opsworks

ow = boto.opsworks.connect_to_region(REGION)

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


def force_setup(instances, update=True):
  stack_id = instances[0]['StackId']
  instance_ids = [ instance['InstanceId'] for instance in instances ]
  if update:
    update_depl = deploy_and_wait(
      stack_id = stack_id,
      instance_ids = instance_ids,
      command_name = 'update_custom_cookbooks'
    )
  setup_depl = deploy_and_wait(
    stack_id = stack_id,
    instance_ids = instance_ids,
    command_name = 'setup'
  )

def launch(layer, name, type='t2.medium'):
  id = ow.create_instance(
    stack_id = layer['StackId'],
    layer_ids = [layer['LayerId'],],
    instance_type = type,
    hostname = name,
    os = 'Ubuntu 14.04 LTS'
  )['InstanceId']
  ow.start_instance(id)
  return id

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
