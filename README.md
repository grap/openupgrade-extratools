openupgrade-extratools
======================

This tool is a light python script to generate an analysis file to evaluate the quantity of works neeeded to upgrade an
Odoo instance from a major version to another.

To use it:
----------

1. Initialize Project
```
git clone https://github.com/grap/openupgrade-extratools.git
cd openupgrade-extratools
cp ./sample_config.ini config.ini
cp ./sample_input.ini input.ini
```

2. In your Odoo instance, extract your installed modules, and copy the list in 'input.csv';

3. Depending of your extra-repository, update your config.ini file, setting your old repositories (version from) and 
your new repositories (version to);

4. Run this command to download sources and make you a coffee

`python update.py`

5. Once the coffee drunk and the previous script is complete, run 

`python analyse.py`

Result:
-------

The result is a log file as:


|Module Name  | Repository (version_7) | Repository (version_8) | Analysis File | Size | Cls/lines  |
|-------------|------------------------|------------------------|---------------|------|------------|
|account                                 |odoo                          |odoo                          |Done                |     |          |
|account_report_company                  |odoo                          |TODO - PORT MODULE            |TODO - ANALYSE      |     |3 / 38    |
|account_voucher                         |odoo                          |odoo                          |Done                |     |          |
|analytic                                |odoo                          |odoo                          |Done                |     |          |
|auth_admin_passkey                      |server-tools                  |TODO - PORT MODULE            |TODO - ANALYSE      |     |3 / 207   |
|auth_signup                             |odoo                          |odoo                          |Nothing to do       |     |          |
|base                                    |odoo                          |odoo                          |Done                |     |          |
|base_import                             |odoo                          |odoo                          |Nothing to do       |     |          |
|base_optional_quick_create              |server-tools                  |server-tools                  |TODO - ANALYSE      |     |1 / 38    |
|base_setup                              |odoo                          |odoo                          |Nothing to do       |     |          |
|board                                   |odoo                          |odoo                          |Nothing to do       |     |          |
|cron_run_manually                       |server-tools                  |server-tools                  |TODO - ANALYSE      |     |1 / 49    |
|decimal_precision                       |odoo                          |odoo                          |Nothing to do       |     |          |
|edi                                     |odoo                          |odoo                          |Nothing to do       |     |          |
|email_template                          |odoo                          |odoo                          |Done                |     |          |
|fetchmail                               |odoo                          |odoo                          |Nothing to do       |     |          |
|mail                                    |odoo                          |odoo                          |Done                |     |          |
|point_of_sale                           |odoo                          |odoo                          |TODO - UPGRADE      |101  |52 / 3278 |
|portal                                  |odoo                          |odoo                          |TODO - UPGRADE      |23   |9 / 540   |
|portal_sale                             |odoo                          |odoo                          |TODO - UPGRADE      |20   |4 / 103   |
|portal_stock                            |odoo                          |odoo                          |Nothing to do       |     |          |
|process                                 |odoo                          |TODO - PORT MODULE            |TODO - ANALYSE      |     |6 / 301   |
|procurement                             |odoo                          |odoo                          |TODO - UPGRADE      |121  |14 / 1001 |
|product                                 |odoo                          |odoo                          |Done                |     |          |
|sale                                    |odoo                          |odoo                          |TODO - UPGRADE      |98   |15 / 1589 |
|sale_stock                              |odoo                          |odoo                          |TODO - UPGRADE      |64   |10 / 835  |
|share                                   |odoo                          |odoo                          |Nothing to do       |     |          |
|stock                                   |odoo                          |odoo                          |TODO - UPGRADE      |540  |52 / 5369 |
|web                                     |odoo                          |odoo                          |Nothing to do       |     |          |
|web_calendar                            |odoo                          |odoo                          |Nothing to do       |     |          |
|web_diagram                             |odoo                          |odoo                          |Nothing to do       |     |          |
|web_easy_switch_company                 |web                           |web                           |TODO - ANALYSE      |     |3 / 43    |
|web_export_view                         |web                           |web                           |TODO - ANALYSE      |     |1 / 28    |
|web_gantt                               |odoo                          |odoo                          |Nothing to do       |     |          |
|web_graph                               |odoo                          |odoo                          |Nothing to do       |     |          |
|web_kanban                              |odoo                          |odoo                          |Nothing to do       |     |          |
|web_tests                               |odoo                          |odoo                          |Nothing to do       |     |          |
|web_view_editor                         |odoo                          |odoo                          |Nothing to do       |     |          |
|web_widget_float_formula                |web                           |TODO - PORT MODULE            |TODO - ANALYSE      |     |0 / 0     |


- FROM : web : 3    (git://github.com/OCA/web.git -b 7.0)
- FROM : server-tools : 3    (git://github.com/OCA/server-tools.git -b 7.0)
- FROM : odoo : 33    (git://github.com/OCA/OCB.git -b 7.0)
- FROM : NOT FOUND : 0 


- TO : web : 2    (git://github.com/OCA/web.git -b 8.0)
- TO : server-tools : 2    (git://github.com/OCA/server-tools.git -b 8.0)
- TO : odoo : 31    (git://github.com/OpenUpgrade/OpenUpgrade.git -b 8.0)
- TO : NOT FOUND : 4 
