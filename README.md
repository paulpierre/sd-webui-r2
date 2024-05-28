# 🌩️ sd-webui-r2
    Cloudflare R2 Bucket Upload Extension for Stable Diffusion WebUI
    This extension for the Stable Diffusion WebUI automatically uploads generated images and their corresponding JSON metadata to Cloudflare's R2 storage. It also provides an optional feature to post the uploaded data to a custom Slack webhook for easy sharing and collaboration.

## 🚀 Features

- 📷 Uploads generated images to Cloudflare R2 storage
- 📝 Uploads JSON metadata alongside the images
- 🔒 Securely stores and retrieves images and metadata
- 💬 Optionally posts the uploaded data to a Slack webhook for sharing
- 🔗 Shares image and json link with image preview in Slack

## 🛠️ Installation

In Stable Diffusion Web UI go to Extensions and click on "Install from URL" and paste the following URL
```
https://github.com/paulpierre/sd-webui-r2
```

## ⚙️ Configuration
To use this extension effectively, you need to provide the following configuration options in the WebUI's settings tab:

In the settings configure the necessary settings in the WebUI's settings tab under the "R2BucketUpload Settings" section:

- Configure via environment variables
    ```bash
    # Example .env or environment variable export setup
    R2_BUCKET_NAME=production-bucket
    R2_UPLOAD_PATH=assets
    R2_DOMAIN=example.com
    R2_ACCESS_KEY_ID=e2a2cf725d0c49d887b9b0a815c4cb56
    R2_SECRET_ACCESS_KEY=2565b9d469be4b549e426f1feb08c952
    R2_ENDPOINT=https://r2.cloudflare.com/1/production-bucket
    ```

## ☁️ Cloudflare R2 configuration
R2 Access Key ID: Your Cloudflare R2 access key ID.
R2 Secret Access Key: Your Cloudflare R2 secret access key.
R2 Upload Path: The desired upload path within your R2 bucket (default: "assets").
Local Upload Path: The local directory where the images and metadata will be temporarily stored before uploading (default: "output").
R2 Endpoint: The endpoint URL for your R2 bucket.
R2 Bucket Name: The name of your R2 bucket.
R2 Domain: The domain associated with your R2 bucket.
Slack Webhook URL (optional): The URL of your Slack webhook for posting the uploaded data.

🖼️ Usage
Generate an image using the Stable Diffusion WebUI as usual.
The extension will automatically upload the generated image and its corresponding JSON metadata to your specified R2 bucket.

If a Slack webhook URL is provided, the extension will also post the uploaded data to the specified Slack channel.
The generated shareable links will be logged in the console for easy access.

### 📄 JSON Metadata Format
The JSON metadata file contains the following information:
```json
{
{
   "prompt":"picture of morty from rick and morty, ultra detailed, 135mm",
   "all_prompts":[
      "picture of morty from rick and morty, ultra detailed, 135mm"
   ],
   "negative_prompt":"",
   "all_negative_prompts":[
      ""
   ],
   "seed":123456789,
   "all_seeds":[
      123456789
   ],
   "subseed":123456789,
   "all_subseeds":[
      123456789
   ],
   "subseed_strength":0,
   "width":512,
   "height":512,
   "sampler_name":"DPM++ 2M",
   "cfg_scale":7,
   "steps":20,
   "batch_size":1,
   "restore_faces":false,
   "face_restoration_model":null,
   "sd_model_name":"epicPhotonism_v10",
   "sd_model_hash":"eed0bdfc49",
   "sd_vae_name":null,
   "sd_vae_hash":null,
   "seed_resize_from_w":-1,
   "seed_resize_from_h":-1,
   "denoising_strength":0.7,
   "extra_generation_params":{
      "Lora hashes":"goodhands_Beta_Gtonero: e7911d734eef",
      "Schedule type":"Karras"
   },
   "index_of_first_image":0,
   "infotexts":[
      "picture of morty from rick and morty, ultra detailed, 135mm\nSteps: 20, Sampler: DPM++ 2M, Schedule type: Karras, CFG scale: 7, Seed: 2899092436, Size: 512x512, Model hash: eed0bdfc49, Model: epicPhotonism_v10, Lora hashes: \" goodhands_Beta_Gtonero: e7911d734eef\", Version: v1.9.2"
   ],
   "styles":[
      
   ],
   "job_timestamp":"20240528101357",
   "clip_skip":1,
   "is_using_inpainting_conditioning":false,
   "version":"v1.9.2"
}
}
```

## 📜 License
This extension is released under the MIT License.

## 🙏 Acknowledgments
Cloudflare for providing an insane amount of value to the developer community


Enjoy using the R2 Bucket Upload Extension for Stable Diffusion WebUI! If you have any questions or need further assistance, feel free to reach out. Happy generating! 🎉