import blessed

term = blessed.Terminal()
colors = ['black',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white']
for n in colors:
    color = getattr(term, n)
    print(color+'{}'.format(n))
    bright_color = getattr(term, 'bright_'+n)
    print(bright_color+'{}'.format('bright_'+n))
