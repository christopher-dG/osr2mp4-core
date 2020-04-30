from ImageProcess.PrepareFrames.YImage import YImages

followpoints = "followpoint"


def prepare_fpmanager(path, scale):
	"""
	:param path: string
	:param scale: float
	:return: [PIL.Image]
	"""
	fp = YImages(path, followpoints, scale * 0.5, delimiter="-", rotate=1)
	return fp.frames


def prepare_fp(fp, angle):
	"""
	:param fp: [PIL.Image]
	:param angle: float
	:return: [PIL.Image]
	"""
	frames = []
	for x in range(len(fp)):
		frames.append(fp[x].rotate(angle))
	return frames