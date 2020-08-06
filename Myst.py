#!/usr/bin/env python3
import sys
import numpy as np
import Canvas
################################################
def load():
  """ Load stdin input as list of strings """
  buf = sys.stdin.read()
  # discard empty lmnts
  return list(filter(None, buf.split(sep='\n')))

################################################
class SQr:
  """ Myst Square """
  ##############################################
  def __init__(self, ch='Ø'):
    ''' Constructor "M7ag TexHuK" '''
    self.type = [ch]
    self.nbor = True # some nbor has changed
    self.skip = False

  ##############################################
  def __str__(self):
    """ (Ø, True, False) """
    return ("("  + self.type[-1]  + 
            ", " + str(self.nbor) +
            ", " + str(self.skip) + ")")
  
################################################
class PhotoShop:
  Brush = {'W': Canvas.Brush('W')}

################################################
class Myst:
  """ Mysterious Continent """
  ##############################################
  def __init__(self, bf):
    """ Construct from input buffer """
    h, w = len(bf), len(bf[0])
    ry = np.empty((h, w), dtype=object)
    for (i, j) in np.ndindex(ry.shape):
      ch = bf[i][j]
      ry[i, j] = SQr(ch)
    # add Ocean frame
    vrt = np.array([SQr() for j in range(h)])
    hrz = np.array([SQr() for i in range(w + 2)])
    ry = np.insert(ry, w, vrt, 1)
    ry = np.insert(ry, 0, vrt, 1)
    ry = np.insert(ry, h, hrz, 0)
    ry = np.insert(ry, 0, hrz, 0)
    self.ry = ry

################################################
if __name__ == "__main__":
  bf = load()
  myst = Myst(bf)
  print(myst.ry.shape)
  PhotoShop.Brush['W'].Draw(
    (10, 20),
    [(Canvas.SGR.Ital,)],
    [(5, 10, 80)],
    [(10, 8, 230)],
    rndm=True)
  print()
  
################################################
# cure:
# next:
