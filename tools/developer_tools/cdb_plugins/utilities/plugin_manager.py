#!/usr/bin/env python
"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
try:
    # attempt to import unique package of cdb python web service to ensure loaded environment
    import cdb.cdb_web_service
except:
    import os, sys
    directory = os.path.dirname(__file__)
    fullPath = os.path.abspath(directory + "/../../../..")
    print >> sys.stderr, "Environment not loaded. Please run `source %s/setup.sh` before running this script." % (
    fullPath)
    exit(1)

import os
import shutil

from plugin_java_parser import PluginJavaParser
from plugin_xhtml_parser import PluginXhtmlParser

from objects.cdb_plugin import CdbPlugin

CDB_INSTALL_DIRECTORY = os.environ['CDB_INSTALL_DIR']
CDB_DIST_DIRECTORY = os.environ['CDB_ROOT_DIR']

CDB_PYTHON_WEB_SERVICE_PATH = 'src/python/cdb'
CDB_XHTML_PLUGIN_PATH = CdbPlugin.get_xhtml_plugin_path(CDB_DIST_DIRECTORY)
CDB_JAVA_PLUGIN_PATH = CdbPlugin.get_java_plugin_path(CDB_DIST_DIRECTORY)
CDB_PYTHON_PLUGIN_PATH = CdbPlugin.get_python_plugin_path(CDB_DIST_DIRECTORY)

CDB_PLUGIN_DIRECTORY = '%s/plugins' % CDB_INSTALL_DIRECTORY

JAVA_PLUGIN_REGISTRAR_FILE_NAME = 'PluginRegistrar.java'

class PluginManager():
    def __init__(self):
        print('Using XHTML Path %s' % CDB_XHTML_PLUGIN_PATH)
        print('Using JAVA Path %s' % CDB_JAVA_PLUGIN_PATH)
        self.plugins = []
        self.__load_plugins()
        self.java_parser = PluginJavaParser(CDB_JAVA_PLUGIN_PATH)
        self.xhtml_parser = PluginXhtmlParser(CDB_XHTML_PLUGIN_PATH)

    def list_plugins(self):
        self.__print_selection_list(self.plugins, 'CDB Plug-ins')

    def prompt_save_plugin(self):
        self.__prompt_plugin_action("Enter the number of plugin to save.", self.save_portal_plugin)

    def save_portal_plugin(self, selection):
        if os.path.exists(CDB_PLUGIN_DIRECTORY) == False:
            os.mkdir(CDB_PLUGIN_DIRECTORY)

        if selection is not None:
            self.__save_portal_plugin(selection)
        else:
            for i in range(0, self.plugins.__len__()):
                self.__save_portal_plugin(i)

    def __save_portal_plugin(self, selection):
        cdb_plugin = self.plugins[selection]
        cdb_plugin.save_plugin_to_saved_plugins_directory()

    def prompt_remove_plugin(self):
        self.__prompt_plugin_action('Enter the number of plugin to remove.', self.remove_portal_plugin)

    def remove_portal_plugin(self, selection):
        if selection is not None:
            self.__remove_portal_plugin(selection)
        else:
            for i in range(0, self.plugins.__len__()):
                self.__remove_portal_plugin(i)

        self.__update_autogenerated_files()

    def __remove_portal_plugin(self, selection):
        cdb_plugin = self.plugins[selection]
        cdb_plugin.remove_plugin_from_distribution()

    def prompt_deploy_plugin(self):
        self.__prompt_plugin_action('Enter the number of plugin to deploy.', self.deploy_portal_plugin)

    def deploy_portal_plugin(self, selection):
        if selection is not None:
            self.__deploy_portal_plugin(selection)
        else:
            for i in range(0, self.plugins.__len__()):
                self.__deploy_portal_plugin(i)

        self.__update_autogenerated_files()

    def __deploy_portal_plugin(self, selection):
        cdb_plugin = self.plugins[selection]
        cdb_plugin.copy_plugin_to_distribution()

    def __prompt_plugin_action(self, actionPrompt, actionMethod):
        self.list_plugins()
        selection = raw_input("%s [All]: " % actionPrompt)
        if selection == "" or selection == "All":
            selection = None
        else:
            selection = int(selection)

        actionMethod(selection)

        print "\n\nCompleted: result plugin list."
        self.list_plugins()

    def update_auto_generated_files(self):
        print 'Updating auto-generated CDB plugin files'
        self.__update_autogenerated_files()

    def __update_autogenerated_files(self):
        self.__load_plugins()
        plugin_registrar_contents = self.java_parser.generate_plugin_registrar_file_contents(self.plugins)

        if not os.path.exists(CDB_JAVA_PLUGIN_PATH):
            os.mkdir(CDB_JAVA_PLUGIN_PATH)

        dist_plugin_java_path = '%s/%s' % (CDB_JAVA_PLUGIN_PATH, JAVA_PLUGIN_REGISTRAR_FILE_NAME)
        java_registrar_file = open(dist_plugin_java_path, 'w')
        java_registrar_file.write(plugin_registrar_contents)
        java_registrar_file.close()

        xhtml_pages = self.xhtml_parser.generate_xhtml_files_contents(self.plugins)

        if not os.path.exists(CDB_XHTML_PLUGIN_PATH):
            os.mkdir(CDB_XHTML_PLUGIN_PATH)

        for file_name in xhtml_pages:
            contents = xhtml_pages[file_name]
            file_path = '%s/%s' % (CDB_XHTML_PLUGIN_PATH, file_name)
            xhtml_file = open(file_path, 'w')
            xhtml_file.write(contents)
            xhtml_file.close()

        if os.path.exists(CDB_PYTHON_PLUGIN_PATH):
            # Create a __init__.py file for all python plugins.
            init_file_path = "%s/%s" % (CDB_PYTHON_PLUGIN_PATH, '__init__.py')
            init_file = os.open(init_file_path, os.O_CREAT)
            os.close(init_file)

    @staticmethod
    def __get_directories_in_path(path, skip_hidden = True):
        directories = []
        if os.path.exists(path):
            for file_name in os.listdir(path):
                if skip_hidden and file_name[0] == '.':
                    # skip hidden files
                    continue
                full_path = '%s/%s' % (path, file_name)
                if os.path.isdir(full_path):
                    directories.append(file_name)

        return directories

    def __load_plugins(self):
        self.plugins = []
        xhtml_dirs = self.__get_directories_in_path(CDB_XHTML_PLUGIN_PATH)
        java_dirs = self.__get_directories_in_path(CDB_JAVA_PLUGIN_PATH)

        plugin_names = xhtml_dirs
        for file_name in java_dirs:
            if file_name not in plugin_names:
                plugin_names.append(file_name)

        saved_plugin_names = self.__get_directories_in_path(CDB_PLUGIN_DIRECTORY)
        for saved_plugin_name in saved_plugin_names:
            if saved_plugin_name not in plugin_names:
                plugin_names.append(saved_plugin_name)

        for plugin_name in plugin_names:
            cdb_plugin = CdbPlugin(plugin_name, CDB_PLUGIN_DIRECTORY, CDB_DIST_DIRECTORY)
            self.plugins.append(cdb_plugin)

    def __print_selection_list(self, selection_list, title):
        width = 70
        header_available = width -2
        header_before = ''
        header_after = ''
        if title.__len__() < header_available:
            width_before = (header_available - title.__len__()) / 2
            width_after = header_available - (width_before + title.__len__())

            header_after = '*' * width_after
            header_before = '*' * width_before

        listItemFormat = '*%4s - %-' + str(width - 36) + 's %-6s %-6s %-12s*'

        print '\nSaved plugins are located in plug-in directory: %s' % CDB_PLUGIN_DIRECTORY
        print 'for xhtml, java, python (s = stored d=deployed)'

        print "\n%s %s %s" % (header_before, title, header_after)
        print listItemFormat % ('#', 'Plugin Name', 'Xhtml', 'Java', 'Python')
        column_header_seperator = '-' * (width-2)
        print '*%s*' % (column_header_seperator)
        for i in range(0, selection_list.__len__()):
            plugin = selection_list[i]
            xhtml = ''
            java = ''
            python = ''
            if plugin.has_python():
                python = 's'
            if plugin.has_java():
                java = 's'
            if plugin.has_xhtml():
                xhtml = 's'

            if plugin.has_deployed_python():
                python += 'd'
            if plugin.has_deployed_java():
                java += 'd'
            if plugin.has_deployed_xhtml():
                xhtml += 'd'


            print listItemFormat % (str(i), plugin.plugin_name, xhtml, java, python)
        print '*' * width

if __name__ == '__main__':
    plugin_manager = PluginManager()
    plugin_manager.list_plugins()
    plugin_manager.save_portal_plugin(0)

    plugin_manager.list_plugins()
    #plugin_manager.update_auto_generated_files()



