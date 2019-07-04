# -*- coding: utf8 -*-
from script.object_factory import SetGlobalApp

def CreateApp():
	import script.team.team as ModTm
	return SetGlobalApp(ModTm.CTeam())
