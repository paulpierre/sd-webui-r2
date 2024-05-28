# 🌩️ sd-webui-r2

<center>
Your own portal gun for your generated images.

<img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDBzZGF2azBnZ2F0YzJqbzBodWc5enZhaDM1YmFqZnQ1cnZmOG9mZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriNTivEJZ1ASRnMc/giphy.gif" width="300" /></center>

Wish your instance of Stable Diffusion WebUI behaved more like Midjourney? You've found the right repo. sd-webui-2 is an extension that leverages callbacks to automatically upload generated images and configuration metadata as JSON to Cloudflare's R2 bucket storage.

As a bonus, it also provides an optional feature to post the uploaded data to a custom Slack webhook for easy sharing and collaboration.

## 🚀 Features

- 📷 Uploads generated images to Cloudflare R2 storage
- 📝 Uploads JSON metadata alongside the images
- 🔒 Securely stores and retrieves images and metadata
- 💬 Optionally posts the uploaded data to a Slack webhook for sharing
- 🔗 Shares image and json link with image preview in Slack

## 🛠️ Installation

1. In Stable Diffusion Web UI go to Extensions and click on "Install from URL" and paste the following URL

    ```
    https://github.com/paulpierre/sd-webui-r2
    ```

    ![image](https://github.com/paulpierre/sd-webui-r2/blob/main/img/7.png?raw=true)

2. Click install and the extension will be installed
3. Click on "Settings"
    ![image](https://github.com/paulpierre/sd-webui-r2/blob/main/img/2.png?raw=true)

4. Click on "R2 Settings" towards the bottom of the page
    
    ![image](https://github.com/paulpierre/sd-webui-r2/blob/main/img/3.png?raw=true)

5. Provide your credentials from Cloudflare R2, if you haven't already, [go ahead and create one for free](https://developers.cloudflare.com/r2/)

    ![image](https://github.com/paulpierre/sd-webui-r2/blob/main/img/2.png?raw=true)

    All the fields are required, for r2 domain you can just keep the default root domain if you don't have a custom domain setup.

    - **R2 Access Key ID**: Your Cloudflare R2 access key ID.
    - **R2 Secret Access Key**: Your Cloudflare R2 secret access key.
    - **R2 Upload Path**: The desired upload path within your R2 bucket (default: "assets").
    - **Local Upload Path**: The local directory where the images and metadata will be temporarily stored before uploading (default: "output").
    - **R2 Endpoint**: The endpoint URL for your R2 bucket.
    - **R2 Bucket Name**: The name of your R2 bucket.
    - **R2 Domain**: The domain associated with your R2 bucket.
    - **Slack Webhook URL (optional)**: The URL of your Slack webhook for posting the uploaded data.

1. Optionally you can automatically post your generated image to a slack webhook via [Incoming Webhooks](https://api.slack.com/messaging/webhooks). Below you can see what it would look like.
    ![image](https://github.com/paulpierre/sd-webui-r2/blob/main/img/8.png?raw=true)

    - Model and prompt / negative prompt are displayed
    - Image URL and image preview are provided
    - Link to the JSON metadata is provided

## ⚙️ Environment variables
Environment variables are supported

```bash
# Example .env or environment variable export setup
R2_BUCKET_NAME=production-bucket
R2_UPLOAD_PATH=assets
R2_DOMAIN=example.com
R2_ACCESS_KEY_ID=e2a2cf725d0c49d887b9b0a815c4cb56
R2_SECRET_ACCESS_KEY=2565b9d469be4b549e426f1feb08c952
R2_ENDPOINT=https://r2.cloudflare.com/1/production-bucket
```



🖼️ Usage
Generate an image using the Stable Diffusion WebUI as usual.
The extension will automatically upload the generated image and its corresponding JSON metadata to your specified R2 bucket.

If a Slack webhook URL is provided, the extension will also post the uploaded data to the specified Slack channel.
The generated shareable links will be logged in the console for easy access.

### 📄 JSON Metadata Format
The JSON metadata file contains the following information:
```json
{
   "prompt":"picture of morty from rick and morty, ultra detailed, 135mm",
   "negative_prompt":"",
   "width":512,
   "height":512,
   "sampler_name":"DPM++ 2M",
   "cfg_scale":7,
   "steps":20,
   ... etc.
}
```

## 📜 License
This extension is released under the MIT License.

Enjoy. PRs welcome and happy generating! 🎉