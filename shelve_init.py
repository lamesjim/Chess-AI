import shelve

d = shelve.open('moves')

# d['even'] = {}
# d['odd'] = {}

print(d)

d.close()
