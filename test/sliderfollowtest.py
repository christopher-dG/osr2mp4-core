import os
import unittest

import osrparse

from CheckSystem.checkmain import checkmain
from Parser.osrparser import setupReplay
from Parser.osuparser import read_file
from Parser.skinparser import Skin
from global_var import Settings


def getinfos(path, mapname, upsidedown=False):
	skin = Skin("{}".format(path), "{}".format(path))
	bmap = read_file("{}{}.osu".format(path, mapname), 1, skin.colours, upsidedown)

	replays = []
	replay_infos = []
	should_continue = True
	x = 0
	fname = ''
	while should_continue:
		replay_event, cur_time = setupReplay("{}{}{}.osr".format(path, mapname, fname), bmap)
		replays.append(replay_event)
		replay_info = osrparse.parse_replay_file("{}{}{}.osr".format(path, mapname, fname))
		replay_infos.append(replay_info)

		x += 1
		fname = str(x)
		should_continue = os.path.isfile("{}{}{}.osr".format(path, mapname, fname))

	return bmap, replays, replay_infos


class TestSliderfollow(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.tests = []
		cls.custom = []
		cls.custom_expect100 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
		cls.custom_expect50 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		Settings.timeframe = 1000
		Settings.fps = 60
		cls.tests.append(getinfos("../test/resources/", "yomi"))
		cls.tests.append(getinfos("../test/resources/", "tool"))
		cls.tests.append(getinfos("../test/resources/", "2tool"))
		cls.tests.append(getinfos("../test/resources/", "2yomi"))
		cls.tests.append(getinfos("../test/resources/", "3yomi"))
		cls.tests.append(getinfos("../test/resources/", "4yomi"))
		cls.custom.append(getinfos("../test/resources/", "69tool"))
		cls.custom.append(getinfos("../test/resources/", "69yomi", True))
		cls.custom.append(getinfos("../test/resources/", "70tool"))
		cls.custom.append(getinfos("../test/resources/", "71tool"))
		cls.custom.append(getinfos("../test/resources/", "69kikoku"))
		cls.custom.append(getinfos("../test/resources/", "70kikoku"))
		cls.custom.append(getinfos("../test/resources/", "71kikoku"))
		cls.custom.append(getinfos("../test/resources/", "72yomi", True))
		cls.custom.append(getinfos("../test/resources/", "73yomi", True))
		cls.custom.append(getinfos("../test/resources/", "74yomi", True))
		cls.custom.append(getinfos("../test/resources/", "75yomi", True))
		cls.custom.append(getinfos("../test/resources/", "76yomi", True))
		cls.custom.append(getinfos("../test/resources/", "77yomi", True))


	def test_sliderfollow(self):
		for i in range(len(self.tests)):
			case = self.tests[i]
			for x in range(len(case[1])):
				resultinfo = checkmain(case[0], case[2][x], case[1][x], 0, True)
				self.assertEqual(case[2][x].number_300s, resultinfo[-1].accuracy[300], msg="replay {} case {} {}".format(str(x), str(i), str(case[2][x].timestamp)))
				self.assertEqual(case[2][x].number_100s, resultinfo[-1].accuracy[100], msg="replay {} case {} {}".format(str(x), str(i), str(case[2][x].timestamp)))
				self.assertEqual(case[2][x].number_50s, resultinfo[-1].accuracy[50], msg="replay {} case {} {}".format(str(x), str(i), str(case[2][x].timestamp)))

	def test_sliderfollowcustom(self):
		for i in range(len(self.custom)):
			case = self.custom[i]
			for x in range(len(case[1])):
				resultinfo = checkmain(case[0], case[2][x], case[1][x], 0, True)
				self.assertEqual(self.custom_expect100[i], resultinfo[-1].accuracy[100], msg="custom replay {} case {}".format(str(x), str(i)))
				self.assertEqual(self.custom_expect50[i], resultinfo[-1].accuracy[50], msg="custom replay {} case {}".format(str(x), str(i)))




if __name__ == '__main__':
	unittest.main()