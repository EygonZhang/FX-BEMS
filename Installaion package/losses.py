
from tip_loss import prandtl_tip_loss
from hub_loss import hub_loss

def Losses(Tip_Loss, Hub_Loss,r, phi, Nb, Radius,r1):

      if Tip_Loss and Hub_Loss:
         F = prandtl_tip_loss(r, phi, Nb, Radius) * hub_loss(r, phi, Nb, r1)

      elif Tip_Loss and not Hub_Loss:
         F = prandtl_tip_loss(r, phi, Nb, Radius)

      elif Hub_Loss and not Tip_Loss:
         F =  hub_loss(r, phi, Nb, r1)

      else:
         F = 1
      return F
