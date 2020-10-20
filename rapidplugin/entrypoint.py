# Copyright 2020 Software Improvement Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import argparse
import pprint
from time import sleep
from rapid_plugin import RapidPlugin
from config import Config

logger = logging.getLogger(__name__)

plugin_name = 'RapidPlugin'
plugin_description = 'A FASTEN plug-in to populate risk related metadata for a product.'
plugin_version = '0.0.1'

def get_args_parser():
    args_parser = argparse.ArgumentParser("RapidPlugin")
    
    args_parser.add_argument('--consume_topic', type=str,
                             default='fasten.RepoCloner.out',
                             help="Kafka topic to consume from.")
    
    args_parser.add_argument('--produce_topic', type=str,
                             default='fasten.RapidPlugin.callable.out',
                             help="Kafka topic to produce to.")
    
    args_parser.add_argument('--err_topic', type=str,
                             default='fasten.RapidPlugin.callable.err',
                             help="Kafka topic to write errors to.")

    args_parser.add_argument('--log_topic', type=str,
                             default='fasten.RapidPlugin.callable.log',
                             help="Kafka topic to write logs to.")
    
    args_parser.add_argument('--bootstrap_servers', type=str,
                             default='localhost',
                             help="Kafka servers, comma separated list between quotes.")
    
    args_parser.add_argument('--group_id', type=str,
                             default='RapidPlugin',
                             help="Kafka consumer group ID to which the consumer belongs.")
    
    args_parser.add_argument('--sleep_time', type=int,
                             default=1,
                             help="Time to sleep in between each message consumption (in sec).")
    args_parser.add_argument('--sources_dir', type=str,
                             default='src',
                             help="Base directory for temporary storing downloaded source code.")
    return args_parser

def get_config(args):
    c = Config('Default')
    c.add_config_value('bootstrap_servers', args.bootstrap_servers)
    c.add_config_value('consume_topic', args.consume_topic)
    c.add_config_value('produce_topic', args.produce_topic)
    c.add_config_value('err_topic', args.err_topic)
    c.add_config_value('log_topic', args.log_topic)
    c.add_config_value('group_id', args.group_id)
    c.add_config_value('sleep_time', args.sleep_time)
    c.add_config_value('sources_dir', args.sources_dir)
    return c

def main():
    parser = get_args_parser()
    plugin_config = get_config(parser.parse_args())

    print(plugin_name + ' ' + plugin_version)
    print('Running with configuration ' + '\"' + plugin_config.get_config_name() + '\"')

    pp = pprint.PrettyPrinter(indent = 2)
    pp.pprint(plugin_config.get_all_values())
    
    plugin = RapidPlugin(plugin_name, plugin_version, plugin_description, plugin_config)

    # Run forever
    while True:
        plugin.consume_messages()
        sleep(plugin_config.get_config_value('sleep_time'))

if __name__ == "__main__":
    main()
