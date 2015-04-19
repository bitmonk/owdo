#!/usr/bin/env python

import logging, time
from owdo.connection import ow
from owdo.util import deploy_and_wait

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
