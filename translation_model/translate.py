import torch.nn.functional as F
import argparse
from utils import get_config, get_renderdata_loader
from data import ImageFolder, label2Color
from trainer import MUNIT_Trainer
import numpy as np
import torchvision.utils as vutils
import torchvision
import sys
import torch
import os
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, default='configs/simulation2surgery.yaml', help='Path to the config file. Use this to adjust the output image size.')
#parser.add_argument('--input_folder', type=str, default='/mnt/g27prist/TCO/TCO-Studenten/rivoirdom/pytorch_render_test/prepared_data/512_biggerLigament', help="input image folder")
parser.add_argument('--input_folder', type=str, default='/mnt/g27prist/TCO/TCO-Studenten/rivoirdom/pytorch_render_test/prepared_data/seq_suppl_30fps', help="input image folder")
parser.add_argument('--output_folder', type=str, default='translations/ours_suppl_30fps', help="output image folder")
parser.add_argument('--checkpoint', type=str, default='trials/acos20_graySSIM/outputs/simulation2surgery/checkpoints/gen_00500000.pt', help="checkpoint of autoencoders")
parser.add_argument('--seed', type=int, default=1, help="random seed (for drawing styles)")
parser.add_argument('--batch_size', type=int, default=10, help="batch size")

save_only_translation = True

opts = parser.parse_args()
conf = get_config(opts.config)
# Figure out how large the result images should be:
if "crop_image_width_translation" in conf:
	w = conf["crop_image_width_translation"]
else:
	w = conf["crop_image_width"]
if "crop_image_height_translation" in conf:
	h = conf["crop_image_height_translation"]
else:
	h = conf["crop_image_height"]
print("Will output translated images of size {}x{}".format(w,h))

#if conf["batch_size"] > 1:
#	print("Warning: Currently only batch size of 1 is supported during translation.")
#	conf["batch_size"] = 1

torch.manual_seed(opts.seed)
torch.cuda.manual_seed(opts.seed)

#batch_size = conf['batch_size']
batch_size = opts.batch_size
num_workers = conf['num_workers']
aug = {}
aug["new_size_min"] = 512
aug["new_size_max"] = 512
aug["output_size"] = (w,h)

scenes = ['3DIrcadb1.1','3DIrcadb1.2','3DIrcadb1.3','3DIrcadb1.4','3DIrcadb1.5','Scene0','Scene0_def']
scene_to_index = {scene: i for i,scene in enumerate(scenes)}
num_scenes = len(scenes)

loader = get_renderdata_loader(opts.input_folder, scene_to_index, batch_size, False, num_workers, translation_mode=True, augmentation=aug )

conf['num_scenes'] = num_scenes
trainer = MUNIT_Trainer(conf)
state_dict = torch.load(opts.checkpoint)
trainer.gen_a.load_state_dict(state_dict['a'])
trainer.gen_b.load_state_dict(state_dict['b'])
trainer.tex = state_dict['tex']
trainer.tex_ref = state_dict['tex_ref']
trainer.cuda()
trainer.eval()

with torch.no_grad():

	for renderdata,scene_idx,input_paths in loader:

		x_a = trainer.render_a(renderdata,scene_idx)
		c_a = trainer.gen_a.encode(x_a)
		x_ab = trainer.gen_b.decode(c_a)

		x_a, x_ab = (x_a+1)/2, (x_ab+1)/2
		texture = x_a[:,:3]
		reference = x_a[:,3:]

		for input_path,fake,tex,ref in zip(input_paths,x_ab,texture,reference):

			scene_name = os.path.basename(os.path.dirname(input_path))
			img_name = os.path.basename(input_path).split('.')[0][8:] + '.png'
			
			if save_only_translation:

				translation_path = os.path.join(opts.output_folder,scene_name,img_name)
				if not os.path.exists(os.path.dirname(translation_path)):
					os.makedirs(os.path.dirname(translation_path))
				vutils.save_image(fake.data, translation_path, padding=0, normalize=False)

			else:

				ref_path = os.path.join(opts.output_folder,scene_name,'reference',img_name)
				tex_path = os.path.join(opts.output_folder,scene_name,'texture',img_name)
				translation_path = os.path.join(opts.output_folder,scene_name,'translation',img_name)
				for path in [ref_path,tex_path,translation_path]:
					if not os.path.exists(os.path.dirname(path)):
						os.makedirs(os.path.dirname(path))

				vutils.save_image(ref.data, ref_path, padding=0, normalize=False)
				vutils.save_image(tex.data, tex_path, padding=0, normalize=False)
				vutils.save_image(fake.data, translation_path, padding=0, normalize=False)

			print("Saved Image '{}'".format(translation_path))