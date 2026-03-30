import os
import urllib.request
from pathlib import Path

# 定义要下载的模型信息：文件名、存放相对路径、下载链接
MODELS_TO_DOWNLOAD = [
    {
        "filename": "svd_xt_1_1.safetensors",
        "path": "models/checkpoints",
        "url": "https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt-1-1/resolve/main/svd_xt_1_1.safetensors"
    },
    {
        "filename": "v1-5-pruned.safetensors",
        "path": "models/checkpoints",
        "url": "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors"
    },
    {
        "filename": "clip_l.safetensors",
        "path": "models/clip",
        "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors"
    },
    {
        "filename": "t5xxl_fp16.safetensors",
        "path": "models/clip",
        "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors"
    },
    {
        "filename": "qwen_image_fp8_e4m3fn.safetensors",
        "path": "models/diffusion_models",
        "url": "https://huggingface.co/Kijai/Qwen2.5-VL-7B-Instruct_fp8_e4m3fn/resolve/main/qwen_image_fp8_e4m3fn.safetensors"
    },
    {
        "filename": "my_first_flux_lora_v1_000004.safetensors",
        "path": "models/loras",
        "url": "" # 注意：需要用户提供真实链接
    },
    {
        "filename": "nsfw_flux_lora_v1.safetensors",
        "path": "models/loras",
        "url": "" # 注意：需要用户提供真实链接
    },
    {
        "filename": "NSFW_master.safetensors",
        "path": "models/loras",
        "url": "" # 注意：需要用户提供真实链接
    },
    {
        "filename": "qwen_2.5_vl_7b_fp8_e4m3fn.safetensors",
        "path": "models/text_encoders",
        "url": "https://huggingface.co/Kijai/Qwen2.5-VL-7B-Instruct_fp8_e4m3fn/resolve/main/qwen_2.5_vl_7b_fp8_e4m3fn.safetensors"
    },
    {
        "filename": "flux1-dev.safetensors",
        "path": "models/unet",
        "url": "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors"
    },
    {
        "filename": "ae.safetensors",
        "path": "models/vae",
        "url": "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors"
    },
    {
        "filename": "qwen_image_vae.safetensors",
        "path": "models/vae",
        "url": "https://huggingface.co/Kijai/Qwen2.5-VL-7B-Instruct_fp8_e4m3fn/resolve/main/qwen_image_vae.safetensors"
    }
]

def download_file(url, filepath):
    if not url:
        print(f"[-] URL为空，跳过下载: {filepath.name}")
        return
        
    print(f"[*] 开始下载: {filepath.name} ...")
    try:
        # 添加 User-Agent 防止被拒绝访问
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            total_size = int(response.info().get('Content-Length', 0))
            downloaded = 0
            block_size = 1024 * 1024 # 1MB
            
            with open(filepath, 'wb') as out_file:
                while True:
                    data = response.read(block_size)
                    if not data:
                        break
                    out_file.write(data)
                    downloaded += len(data)
                    if total_size > 0:
                        percent = int(downloaded * 100 / total_size)
                        print(f"\r    -> 进度: {percent}% ({downloaded/(1024*1024):.1f}MB / {total_size/(1024*1024):.1f}MB)", end="")
        print(f"\n[+] 下载完成: {filepath.name}")
    except Exception as e:
        print(f"[!] 下载失败 {filepath.name}: {e}")

def main():
    base_dir = Path("ComfyUI")
    
    for model in MODELS_TO_DOWNLOAD:
        target_dir = base_dir / model["path"]
        target_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = target_dir / model["filename"]
        if filepath.exists():
            print(f"[~] 文件已存在，跳过: {filepath.name}")
            continue
            
        download_file(model["url"], filepath)

if __name__ == "__main__":
    main()
