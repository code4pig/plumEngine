# -*- coding: utf8 -*-
from script.object_factory import SetGlobalApp

def CreateApp():
	import script.teamproxy.teamproxy as ModTm
	return SetGlobalApp(ModTm.CTeamProxy())
