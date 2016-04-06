import os
import sys

from experiment import ToolsExperiment
from config import configs

  
log_dir = sys.argv[1]
config_name = sys.argv[2]
trial = sys.argv[3]

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

xp = ToolsExperiment(config=configs[config_name], context_mode=configs[config_name].context_mode, log_dir=log_dir)
    
xp.trial = trial

xp.start_trial()