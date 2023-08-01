# How to excute

only check.py means check `crm` `item` `order`

```bash
python check.py
```

you could also check specific files with

```bash
python check.py crm item
```

# Installation

```bash
pip install -r requirements.txt
```

# More detail

- definition.yml: the definition of columns
  - primaryKey is neccessary existed column:
  - columns are optional, but all input column need to be included within definition
- all input file need to be put in folder with filename: 'crm.csv', 'item.csv', 'order.csv'
