from bitdeli.widgets import Widget, Table
from bitdeli.insight import insight
from discodb.query import Q, Literal, Clause

class TokenInput(Widget):
    pass

BINS = ['0', '1', '2-3', '4-7', '8+']

def month_keys(model):
    keys = list(frozenset(key[:7] for key in model))
    keys.sort(reverse=True)
    return keys
    
def months(params):
    monthx = monthy = None
    if 'monthx' in params and params['monthx']['value']:
        monthx = params['monthx']['value'][0]
    if 'monthy' in params and params['monthy']['value']:
        monthy = params['monthy']['value'][0]
    return monthx, monthy

def rows(model, monthx, monthy):
    def clauses(month):
        q = [Literal('%s:%s' % (month, bin)) for bin in range(1, len(BINS))]
        return [Clause(~x for x in q)] + [Clause([x]) for x in q]

    def row(biny, y):
        yield 'ybin', {'label': BINS[biny]}
        for binx, x in enumerate(clauses(monthx)):
            norm = float(max(1, len(model.query(Q([x | y])))))
            perc = len(model.query(Q((y, x)))) / norm
            yield BINS[binx], {'label': '%d%%' % (perc * 100),
                               'background': perc}

    return (dict(row(biny, y))
            for biny, y in enumerate(clauses(monthy)))

@insight
def insight(model, params):
    monthx, monthy = months(params)
    
    yield TokenInput(id='monthx',
                     label='First Month',
                     size=(6, 1),
                     data=month_keys(model),
                     value=[monthx] if monthx else [])
    yield TokenInput(id='monthy',
                     label='Second Month',
                     size=(6, 1),
                     data=month_keys(model),
                     value=[monthy] if monthy else [])
    
    if monthx and monthy:
        columns = [{'row_header': True,
                    'label': monthy,
                    'name': 'ybin'}] +\
                  [{'label': bin, 'name': bin} for bin in BINS]
        
        rowss = list(rows(model, monthx, monthy))
        print rowss
        
        yield Table(size=(12, 'auto'),
                    label='% returning users over the frequency of use',
                    fixed_width=True,
                    columns_label=monthx,
                    data={'columns': columns,
                          'rows': rowss})