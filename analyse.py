#! /usr/bin/env python
# -*- encoding: utf-8 -*-
from config import conf
from os import path, makedirs, listdir, walk
import git
from git import Repo
import csv

def analyse():
    file_name = conf.get('general', 'input_file')
    version_from = conf.get('general', 'version_from')
    version_to = conf.get('general', 'version_to')
    lst_repo_from = conf.get(version_from, 'list_repository').split(',')
    lst_repo_to = conf.get(version_to, 'list_repository').split(',')
    main_analysis_file = conf.get('general', 'main_analysis_file')
    fo = open(main_analysis_file, "r+")
    analysis_lines = fo.readlines()
    fo.close()
    res = []
    sum_res_from = {}
    sum_res_to = {}
    with open(file_name, 'rb') as csv_file:
        spamreader = csv.reader(
            csv_file,
            delimiter=conf.get('general', 'input_delimiter'),
            quotechar=conf.get('general', 'input_quotechar'))
        for row in spamreader:
            value = {}
            module_name = row[conf.getint('general', 'input_module_col')]
            value['name'] = module_name

            # Manage FROM
            apath_from = False
            repo_found = False
            for repo_from in lst_repo_from:
                if path.isdir('./%s/%s/%s' % (version_from, repo_from, module_name)):
                    apath_from = './%s/%s/%s' % (version_from, repo_from, module_name)
                elif path.isdir('./%s/%s/addons/%s' % (version_from, repo_from, module_name)):
                    apath_from = './%s/%s/addons/%s' % (version_from, repo_from, module_name)
                elif path.isdir('./%s/%s/openerp/addons/%s' % (version_from, repo_from, module_name)):
                    apath_from = './%s/%s/openerp/addons/%s' % (version_from, repo_from, module_name)

                if apath_from:
                    repo_found = repo_from
                    break

            if not repo_found:
                value['version_from'] = 'ERROR - NOT FOUND'
            else:
                value['version_from'] = repo_found
                if sum_res_from.get(repo_found):
                    sum_res_from[repo_found] += 1
                else:
                    sum_res_from[repo_found] = 1

            # Manage To
            repo_found = False
            check_main_analysis = False
            for repo_to in lst_repo_to:
                if path.isdir('./%s/%s/%s' % (version_to, repo_to, module_name)):
                    apath_to = './%s/%s/%s' % (version_to, repo_to, module_name)
                    repo_found = repo_to
                elif path.isdir('./%s/%s/addons/%s' % (version_to, repo_to, module_name)):
                    apath_to = './%s/%s/addons/%s' % (version_to, repo_to, module_name)
                    repo_found = repo_to
                    check_main_analysis = True
                elif path.isdir('./%s/%s/openerp/addons/%s' % (version_to, repo_to, module_name)):
                    apath_to = './%s/%s/openerp/addons/%s' % (version_to, repo_to, module_name)
                    repo_found = repo_to
                    check_main_analysis = True

            if not repo_found:
                if value['version_from'] == 'ERROR - NOT FOUND':
                    value['version_to'] = 'ERROR - NOT FOUND'
                else:
                    value['version_to'] = 'TODO - PORT MODULE'
                value['analysis_state'] = 'TODO - ANALYSE'
            else:
                value['version_to'] = repo_found
                if sum_res_to.get(repo_found):
                    sum_res_to[repo_found] += 1
                else:
                    sum_res_to[repo_found] = 1
                if check_main_analysis:
                    value['analysis_state'] = 'RENAMED ?'
                    for analysis_line in analysis_lines:
                        if analysis_line.startswith('|' + module_name + ' '):
                            analyse = analysis_line.split('|')[2].strip()
                            if analyse != '':
                                value['analysis_state'] = analysis_line.split('|')[2].strip()
                            else:
                                value['analysis_state'] = 'TODO - UPGRADE'
                            break
                else:
                    value['analysis_state'] = 'TODO - ANALYSE'

            # Size of the analysis file
            value['upgrade_size'] = ''
            if value['analysis_state'] == 'TODO - UPGRADE':
                if path.isdir(apath_to + '/migrations'):
                    for dir in listdir(apath_to + '/migrations'):
                        if path.isfile(apath_to + '/migrations/' + dir + '/openupgrade_analysis.txt'):
                            num_lines = sum(1 for line in open(apath_to + '/migrations/' + dir + '/openupgrade_analysis.txt'))
                            if value['upgrade_size'] == '':
                                value['upgrade_size'] = num_lines
                            else:
                                value['upgrade_size'] += num_lines
                if value['upgrade_size'] == '':
                    value['upgrade_size'] = 'ERROR'
                else:
                    value['upgrade_size'] = str(value['upgrade_size'])

            # Size of the module


            if value['version_from'] == 'ERROR - NOT FOUND':
                value['technic_size'] = 'ERROR'
            elif value['analysis_state'] in ['TODO - ANALYSE', 'TODO - UPGRADE']:
                num_lines = 0
                num_class = 0
                for (dirpath, dirnames, filenames) in walk(apath_from):
                    for filename in filenames:
                        if filename[-3:] == '.py' and filename != '__openerp__.py':
                            for line in open(dirpath + '/' + filename):
                                if not line.strip().startswith('#') and line.strip() != '' :
                                    num_lines += 1
                                    if line.strip().startswith('class '):
                                        num_class += 1
                value['technic_size'] = str(num_class) + ' / ' + str(num_lines)
            else:
                value['technic_size'] = ''

            res.append(value)
    csv_file.close()
    
    MODULE_SIZE = 40
    FROM_SIZE = 30
    TO_SIZE = 30
    ANALYSIS_SIZE = 20
    UPGRADE_SIZE = 5
    TECHNIC_SIZE = 10
    INTERLINE =  "-" * (7 + MODULE_SIZE + FROM_SIZE + TO_SIZE + ANALYSIS_SIZE + UPGRADE_SIZE + TECHNIC_SIZE)

    print INTERLINE
    print "|"\
        + 'Module Name' + " " * (MODULE_SIZE-len('Module Name')) + "|"\
        + 'Repository (' + version_from + ')'+\
        " " * (FROM_SIZE-len('Repository (' + version_from + ')')) + "|"\
        + 'Repository (' + version_to + ')'+\
        " " * (FROM_SIZE-len('Repository (' + version_to + ')')) + "|"\
        + 'Analysis File' + " " * (ANALYSIS_SIZE-len('Analysis File')) + "|"\
        + 'Size' + " " * (UPGRADE_SIZE-len('Size')) + "|"\
        + 'Cls/lines' + " " * (TECHNIC_SIZE-len('Cls/lines')) + "|"

    print INTERLINE
    for item in res:
        print "|" + item['name'][0:MODULE_SIZE] \
            + " " * (MODULE_SIZE-len(item['name'][0:MODULE_SIZE])) \
            + "|" + item['version_from'][0:FROM_SIZE] \
            + " " * (FROM_SIZE-len(item['version_from'][0:FROM_SIZE]))\
            + "|"+ item['version_to'][0:TO_SIZE] \
            + " " * (TO_SIZE-len(item['version_to'][0:TO_SIZE]))\
            + "|"+ item['analysis_state'][0:ANALYSIS_SIZE] \
            + " " * (ANALYSIS_SIZE-len(item['analysis_state'][0:ANALYSIS_SIZE]))\
            + "|"+ item['upgrade_size'][0:UPGRADE_SIZE] \
            + " " * (UPGRADE_SIZE-len(item['upgrade_size'][0:UPGRADE_SIZE]))\
            + "|"+ item['technic_size'][0:TECHNIC_SIZE] \
            + " " * (TECHNIC_SIZE-len(item['technic_size'][0:TECHNIC_SIZE]))\
            + "|"
    print INTERLINE
    
    total_from = 0
    total_to = 0

    for k, v in sum_res_from.items():
        print " - FROM : %s : %d    (%s)" % (k, v, conf.get(version_from, k))
        total_from += v
    print " - FROM : NOT FOUND : %d " % (len(res) - total_from)

    print INTERLINE
    for k, v in sum_res_to.items():
        print " - FROM : %s : %d    (%s)" % (k, v, conf.get(version_to, k))
        total_to += v
    print " - TO : NOT FOUND : %d " % (len(res) - total_to)

    print INTERLINE

analyse()
