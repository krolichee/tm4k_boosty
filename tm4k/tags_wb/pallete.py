from matplotlib import colors

PALLETE = [c.replace('#', "") for c in list(colors.TABLEAU_COLORS.values())]


def getFromPalleteCycle(color_i: int):
    return PALLETE[color_i % len(PALLETE)]
