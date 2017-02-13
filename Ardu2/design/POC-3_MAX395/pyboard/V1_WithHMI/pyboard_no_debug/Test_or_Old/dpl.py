# dpl.py
# to test loading of defaultPresets in case of SD read error
# 2016 12 31: works

fail = True

curDict = {}

def test():
    """
    locally imports defaultPresets
    then assigns it to the module scope curDict
    but only if fail is True
    """
    global curDict
    if fail:
        import defaultPresets
        curDict = defaultPresets.defPresetDict

