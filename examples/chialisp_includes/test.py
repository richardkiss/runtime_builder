from chialisp_includes import include_directory


t = include_directory()
print(t)
assert t.parts[-3:] == ( 'chialisp_includes', 'chialisp_includes', 'clib')
