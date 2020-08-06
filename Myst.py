#!/usr/bin/env python3
import sys
import numpy as np
import Canvas as cv
################################################
def load(): #                               LOAD
  """ Load stdin input as list of strings """
  buf = sys.stdin.read()
  # discard empty lmnts
  return list(filter(None, buf.split(sep='\n')))
################################################
#
################################################
class Glob: #                               GLOB
  type = "WØBLGMPC"
################################################
#
################################################
class PaintShop: #                     PAINTSHOP
  Brush = { k : cv.Brush(k) for k in Glob.type }
  Colour = {
    'W': (( 10, 35, 110), (12, 28, 74)),
    'Ø': (( 20, 10, 120), (14,  8, 52)),
    'G': ((120, 60,  20), (60, 40, 23))
  }
################################################
#
################################################
class SQr: #                                 SQR
  """ Myst Square """
  ##############################################
  def __init__(self, ch):           #   __INIT__
    ''' Constructor "M7ag TexHuK" '''
    self.type = ch
    self.nbor = True # some nbor has changed
    self.skip = False
  ##############################################
  #
  ##############################################
  def __str__(self): #                   __STR__                
    """ (Ø, True, False) """
    return ("("  + self.type      + 
            ", " + str(self.nbor) +
            ", " + str(self.skip) + ")")
  ##############################################
  #
  ##############################################
  def Draw(self, r): #                      DRAW
    ch = self.type
    brush = PaintShop.Brush[ch]
    colour = PaintShop.Colour[ch]
    sgr = [cv.SGR.Rndm()]
    fgr = [cv.RndmClr(colour[0])]
    bgr = [cv.RndmClr(colour[1])]
    return brush.Draw(r, sgr, fgr, bgr, True)
  ##############################################
  #
  ##############################################
  def _locked(self): #                   _LOCKED
    return self.skip or not self.nbor
  ##############################################
  #
################################################
#
################################################
def hood(i, j): #                           HOOD
  return ((i - 1, j),
          (i + 1, j),
          (i, j - 1),
          (i, j + 1))
################################################
#
################################################
class Myst: #                               MYST
  """ Mysterious Continent """
  ##############################################
  def __init__(self, bf, orig): #       __INIT__
    """ Construct from input buffer """
    h, w = len(bf), len(bf[0])
    ry = np.empty((h, w), dtype=object)
    for (i, j) in np.ndindex(ry.shape):
      ch = bf[i][j]
      ry[i, j] = SQr(ch)
    self.ry = ry
    self.orig = orig
  ##############################################
  #
  ##############################################
  def Draw(self): #                         DRAW
    for coor, sq in np.ndenumerate(self.ry):
      r = np.add(self.orig, coor)
      sq.Draw(r)
  ##############################################
  #  
  ##############################################
  def cont(self, i, j): #                   CONT
    c = { k : 0 for k in Glob.type } # init to 0
    for coor in hood(i, j):
      type = self.ry[coor].type
      c[type] += 1
      c['W'] += type in "ØB"
      c['G'] += type in "MP"
    return c
  ##############################################
  #
  ##############################################
  def relabel(self, coor): #             RELABEL
    sq = self.ry[coor]
    type = sq.type
    if type not in 'WØG': return False
    if sq._locked(): return False
    cont = self.cont(*coor)
    if type is 'W':
      if cont['Ø']: 
        sq.type = 'Ø'
        return True
    elif type is 'Ø':
      if (cont['G'] == 2 and cont['Ø'] > 0 or
          cont['B']  > 0 and cont['Ø'] < 2):
        sq.type = 'B'
        return True
    elif type is 'G':
      for i in 0, 1, 2:
        if (cont['W'] == 3 - i and 
            cont['P']  > i - 1):
          sq.type = 'P'
          return True
################################################
#
################################################
if __name__ == "__main__": #            __MAIN__
  bf = load()
  myst = Myst(bf, (50, 10))
  myst.Draw()
  cont = myst.cont(4, 4)
  print()
  print(cont)
################################################
# THINK
