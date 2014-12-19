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
