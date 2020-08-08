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
    'W': (( 10,  35, 110), (12, 28, 74)),
    'Ø': (( 20,  10, 120), (14,  8, 52)),
    'G': ((120,  60,  20), (60, 40, 23)),
    'M': ((140,   5,   5), (80,  8,  8)),
    'P': (( 20, 150,  30), ( 5, 50, 10)),
    'B': ((150, 130, 140), (15, 10, 80))
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
def _W2Ø(type, cont): #                     _W2Ø
  ''' Water 2 Ocean? '''
  if type != 'W': return False
  return cont['Ø'] > 0
################################################
#
################################################
def _Ø2B(type, cont): #                     _Ø2B
  ''' Ocean 2 Bay? '''
  if type != 'Ø': return False
  return (cont['G'] == 2 and cont['Ø'] > 0 or
          cont['B']  > 0 and cont['Ø'] < 2)
################################################
#
################################################
def _G2M(type, cont): #                     _G2M
  ''' Ground 2 Mountain? '''
  if type != 'G': return False
  return cont['G'] == 4
################################################
#
################################################
def _G2P(type, cont): #                     _G2P
  ''' Ground 2 Peninsula? '''
  if type != 'G': return False
  for i in range(3):
    if (cont['W'] == 3 - i and 
        cont['P']  > i - 1):
      return True
  return False
################################################
#
################################################
class Myst: #                               MYST
  """ Mysterious Continent """
  ##############################################
  def __init__(self, bf): #             __INIT__
    """ Construct from input buffer """
    h, w = len(bf), len(bf[0])
    ry = np.empty((h, w), dtype=object)
    for (i, j) in np.ndindex(ry.shape):
      ch = bf[i][j]
      ry[i, j] = SQr(ch)
    self.ry = ry
  ##############################################
  #
  ##############################################
  def Draw(self, orig): #                   DRAW
    for coor, sq in np.ndenumerate(self.ry):
      r = np.add(orig, coor)
      sq.Draw((r[1], r[0])) # thats an issue
  ##############################################
  # in ry[i, j], i is the y coor
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
    """ ys! """
    sq = self.ry[coor]
    type = sq.type
    if type not in 'WØG': return False
    if sq._locked(): return False
    cont = self.cont(*coor)
    skip = (False, True, True, True)
    newtype = "ØBMP"
    for i, f in enumerate((_W2Ø,_Ø2B,_G2M,_G2P)):
      if f(type, cont):
        sq.type = newtype[i]
        sq.skip = skip[i]
        return True
    return False
  ##############################################
  #
  ##############################################
  def remap(self):
    w, h = np.subtract(self.ry.shape, (1, 1))
    I, J = range(1, w), range(1, h)
    n = 0 # nof relabeled squares
    for i in I:
      for j in J:
        n += self.relabel((i, j))
    return n
  ##############################################
  #
################################################
#
################################################
if __name__ == "__main__": #            __MAIN__
  bf = load()
  myst = Myst(bf)
  i = 0
  while True:
    myst.Draw([5, 5 + i*12])
    n = myst.remap()
    i += 1
    if n == 0: break
  print(2*'\n')
################################################
# ./Myst.py <maps/heroes2.h2m
