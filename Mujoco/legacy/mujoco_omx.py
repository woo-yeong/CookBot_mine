import mujoco
import mujoco.viewer
from pathlib import Path

model_path = Path(__file__).with_name("scene.xml")
model = mujoco.MjModel.from_xml_path(str(model_path))
data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()
