# owdo
opsworks do

    (owdo)ip-192-168-1-6:owdo justinryan$ owdo -h
    usage: owdo (sub-commands ...) [options ...] {arguments ...}

    Opsworks do-er of things

    commands:

      force-setup
        launch a fresh instance in a layer of a stack.

      launch
        launch a fresh instance in a layer of a stack.

    optional arguments:
      -h, --help            show this help message and exit
      --debug               toggle debug output
      --quiet               suppress all output
      -s STACK, --stack STACK
                            stack name
      -l LAYER, --layer LAYER
                            layer name
      -t TYPE, --type TYPE  instance type
      -n NAME, --name NAME  name

Furthemore:

    owdo launch -s opstest -l monitoring -n opstest-monitoring05

Also:

    owdo force-setup -s opstest -l monitoring -n opstest-monitoring05

Yep.
