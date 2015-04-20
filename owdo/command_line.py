"""
Cement script using http://builtoncement.com/2.4/dev/quickstart.html
"""
from cement.core import backend, foundation, controller, handler
from owdo.connection import ow
from owdo.types import OWStack, OWLayer, OWInstance
import owdo.core

class OwdoBaseController(controller.CementBaseController):
  class Meta:
    label = 'base'
    description = 'Opsworks do-er of things'

    config_defaults = dict(
      stack_name = 'opstest',
      layer_name = 'test',
    )

    arguments = [
      (['-s', '--stack'], dict(action='store', help='stack name')),
      (['-l', '--layer'], dict(action='store', help='layer name')),
      (['-t', '--type'],  dict(action='store', help='instance type')),
      (['-n', '--name'],  dict(action='store', help='name')),
    ]

  @controller.expose(hide=True, aliases=['run'])
  def default(self):
    self.app.log.info('Inside base.default function.')
    if self.app.pargs.stack:
      self.app.log.info("Recieved option 'stack' with value '%s'." % \
        self.app.pargs.stack)

    if self.app.pargs.layer:
      self.app.log.info("Recieved option 'layer' with value '%s'." % \
        self.app.pargs.layer)

  @controller.expose(help='launch a fresh instance in a layer of a stack.')
  def launch(self):
    self.app.log.info('Inside base.launch function.')
    if self.app.pargs.stack:
      stack_name = self.app.pargs.stack
    else:
      stack_name = 'opstest'

    stack = OWStack(ow, stack_name)

    if self.app.pargs.layer:
      layer_name = self.app.pargs.layer
    else:
      layer_name = 'test'

    layer = OWLayer(ow, stack._stack, layer_name)

    if self.app.pargs.type:
      instance_type = self.app.pargs.type
    else:
      instance_type = 't2.medium'

    if self.app.pargs.name:
      name = self.app.pargs.name
    else:
      name = None

    print owdo.core.launch(layer, name, 't2.medium')


  @controller.expose(help='launch a fresh instance in a layer of a stack.')
  def force_setup(self):
    self.app.log.info('Inside base.force_setup function.')
    if self.app.pargs.stack:
      stack_name = self.app.pargs.stack
    else:
      stack_name = 'opstest'

    stack = OWStack(ow, stack_name)

    if self.app.pargs.layer:
      layer_name = self.app.pargs.layer
    else:
      layer_name = 'test'

    layer = OWLayer(ow, stack._stack, layer_name)

    if self.app.pargs.name:
      instance_name = self.app.pargs.name
    else:
      raise "No instance name!"

    instance = OWInstance(ow, stack, layer, instance_name)
    owdo.core.force_setup([instance])

class OwdoApp(foundation.CementApp):
  class Meta:
    label = 'owdo'
    base_controller = OwdoBaseController

def main():
  app = OwdoApp()

  try:
    app.setup()
    app.run()
  finally:
    app.close()

if __name__ == '__main__':
  main()

