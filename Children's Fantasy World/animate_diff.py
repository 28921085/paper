import torch
from diffusers import AnimateDiffControlNetPipeline, AutoencoderKL, ControlNetModel, MotionAdapter, LCMScheduler
from diffusers.utils import export_to_gif, load_image
from controlnet_aux.processor import ZoeDetector

# 載入控制網路模型
controlnet = ControlNetModel.from_single_file("control_v11f1p_sd15_depth.pth", torch_dtype=torch.float16)

# 載入運動適配器
motion_adapter = MotionAdapter.from_pretrained("wangfuyun/AnimateLCM")

# 載入 VAE
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse", torch_dtype=torch.float16)

# 建立管道
pipe = AnimateDiffControlNetPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V5.1_noVAE",
    motion_adapter=motion_adapter,
    controlnet=controlnet,
    vae=vae,
).to(device="cuda", dtype=torch.float16)

# 設定調度器
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config, beta_schedule="linear")

# 載入並處理輸入圖片
image_path = "path_to_your_image.png"
input_image = load_image(image_path)

# 使用 ZoeDetector 生成深度圖
depth_detector = ZoeDetector.from_pretrained("lllyasviel/Annotators").to("cuda")
conditioning_frame = depth_detector(input_image)

prompt = "描述您希望生成的場景"
negative_prompt = "不希望出現的元素"

output = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_frames=16,
    num_inference_steps=25,
    guidance_scale=7.5,
    conditioning_frames=[conditioning_frame],
    generator=torch.Generator().manual_seed(42),
)

# 將生成的幀保存為 GIF
frames = output.frames[0]
export_to_gif(frames, "output_animation.gif")
