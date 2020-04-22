from recordclass import recordclass

from Objects.abstracts import *


spinnerbackground = "spinner-background"
spinnercircle = "spinner-circle"


Spinner = recordclass("Spinner", "angle duration starttime_left alpha index")


class SpinnerManager(Images):
	def __init__(self, frames, scale, moveright, movedown):
		self.moveright = moveright
		self.movedown = movedown
		self.scale = scale
		self.spinners = {}
		self.spinner_images, self.spinnermetre, self.spinner_frames = frames

		self.interval = 1000/60

	def add_spinner(self, starttime, endtime, curtime):
		duration = endtime - starttime
		# img, duration, startime left, alpha, index, progress
		self.spinners[str(starttime) + "o"] = Spinner(0, duration, starttime - curtime, 0, 0)

	def update_spinner(self, timestamp, angle, progress):
		# angle = round(angle * 0.9)
		# n_rot = int(angle/90)
		# index = int(angle - 90*n_rot)
		# n_rot = n_rot % 4 + 1

		self.spinners[timestamp].angle = angle
		# if n_rot != 1:
		# 	self.spinners[timestamp][0] = self.spinners[timestamp][0].transpose(n_rot)

		progress = progress * 10
		if 0.3 < progress - int(progress) < 0.35 or 0.6 < progress - int(progress) < 0.65:
			progress -= 1

		self.spinners[timestamp][4] = min(10, int(progress))

	def add_to_frame(self, background, i, alone):
		if self.spinners[i].starttime_left > 0:
			self.spinners[i].starttime_left -= self.interval
			self.spinners[i].alpha = min(1, self.spinners[i].alpha + self.interval / 400)
		else:
			self.spinners[i].duration -= self.interval
			if 0 > self.spinners[i].duration > -200:
				self.spinners[i].alpha = max(0, self.spinners[i].alpha - self.interval / 200)
			else:
				self.spinners[i].alpha = 1
		self.img = self.spinner_images[spinnerbackground].img
		# if not alone:
		super().add_to_frame(background,  background.size[0]//2, 46 + self.img.size[1]//2, alpha=self.spinners[i].alpha)
		# else:
		# 	x, y = background.size[0]//2 - self.img.size[0]//2, 46
		# 	y1, y2, ystart, yend = super().checkOverdisplay(y, y + self.img.size[1], background.size[1])
		# 	x1, x2, xstart, xend = super().checkOverdisplay(x, x + self.img.size[0], background.size[0])
		# 	background[y1:y2, x1:x2, :] = self.img[ystart:yend, xstart:xend, :3]

		self.img = self.spinnermetre.rotate(self.spinners[i].angle)
		super().add_to_frame(background, background.size[0] // 2, int(198.5 * self.scale) + self.movedown, alpha=self.spinners[i].alpha)

		height = self.spinner_frames.size[1]
		y_start = height - self.spinners[i].index * height // 10
		width = self.spinner_frames.size[0]
		self.img = self.spinner_frames.crop((0, y_start, width, height))
		super().add_to_frame(background, background.size[0]//2, 46 + self.img.size[1]//2 + y_start, alpha=self.spinners[i].alpha)