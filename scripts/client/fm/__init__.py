# Embedded file name: scripts/client/fm/__init__.py
import Avatar
import BigWorld
import DestructibleObjectFactory
import PlayerAvatar
import Weapons
from fm.FMAvatar import fmAvatar
from fm.FMGuns import fmGuns
from fm.FMPlayerAvatar import fmPlayerAvatar
from fm.FMWeapons import fmWeapons
Avatar.Avatar = fmAvatar(Avatar.Avatar)
Avatar.PlayerAvatar = fmPlayerAvatar(Avatar.PlayerAvatar)
Weapons.Guns = fmGuns(Weapons.Guns)
DestructibleObjectFactory.Weapons = fmWeapons(DestructibleObjectFactory.Weapons)