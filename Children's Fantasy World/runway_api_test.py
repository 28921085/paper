from runwayml import RunwayML
import time, base64
# The env var RUNWAYML_API_SECRET is expected to contain your API key.
client = RunwayML()

image = 'testimgs/0.jpg'

# encode image to base64
with open(image, "rb") as f:
    base64_image = base64.b64encode(f.read()).decode("utf-8")

task = client.image_to_video.create(
  model='gen3a_turbo',
  prompt_image=f"data:image/png;base64,{base64_image}",
  prompt_text="""The woman’s expression intensifies as her mouth opens and closes in an exaggerated manner, her hair swaying slightly with her animated movements. Her arms make small, sharp gestures while the child beside her shifts his gaze upward, his hands moving subtly toward the armrest, creating dynamic motion within the fixed frame.""",
  duration=5,
  ratio="768:1280"
)
print(task.id)
task_id = task.id

# Poll the task until it's complete
time.sleep(10)  # Wait for a second before polling
task = client.tasks.retrieve(task_id)
while task.status not in ['SUCCEEDED', 'FAILED']:
  time.sleep(10)  # Wait for ten seconds before polling
  task = client.tasks.retrieve(task_id)

print('Task complete:', task)