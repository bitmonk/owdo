REGION = 'us-east-1'

import boto.opsworks
ow = boto.opsworks.connect_to_region(REGION)

