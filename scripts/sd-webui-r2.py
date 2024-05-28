from modules import scripts, script_callbacks, shared
from r2client.R2Client import R2Client
from modules.shared import opts
from typing import Optional
import logging
import httpx
import os
import json

logger = logging.getLogger(__name__)

shared.opts.add_option("r2_access_key_id", shared.OptionInfo("", "R2 Access Key ID", section=("r2", "R2 Settings")))
shared.opts.add_option("r2_secret_access_key", shared.OptionInfo("", "R2 Secret Access Key", section=("r2", "R2 Settings")))
shared.opts.add_option("r2_upload_path", shared.OptionInfo("assets", "R2 Upload Path", section=("r2", "R2 Settings")))
shared.opts.add_option("local_upload_path", shared.OptionInfo("output", "Local Upload Path", section=("r2", "R2 Settings")))
shared.opts.add_option("r2_endpoint", shared.OptionInfo("", "R2 Endpoint", section=("r2", "R2 Settings")))
shared.opts.add_option("r2_bucket_name", shared.OptionInfo("", "R2 Bucket Name", section=("r2", "R2 Settings")))
shared.opts.add_option("r2_domain", shared.OptionInfo("", "R2 Domain", section=("r2", "R2 Settings")))
shared.opts.add_option("slack_webhook_url", shared.OptionInfo("", "Slack Webhook URL", section=("r2", "R2 Settings")))


class R2BucketUpload(scripts.Script):

    def title(self):
        return "R2 Bucket upload"

    def show(self, is_img2img):
        return not is_img2img

    async def postprocess(self, p, processed, *args, **kwargs):

        slack_webhook_url = opts.slack_webhook_url

        data = p.js()

        if processed.images:
            output_file_path = processed.images[0]  # Path to the output image
            output_json_path = output_file_path.replace('.png', '.json')  # Assuming output is a .png file
    
            with open(output_json_path, 'w') as json_file:
                json.dump(data, json_file)
            
            logger.info(f"🔄 Uploading {output_file_path} to R2")
            img_url = self.upload_to_r2(output_file_path)
            logger.info(f"🔄 Uploading {output_json_path} to R2")
            prompt_url = self.upload_to_r2(output_json_path)
            # Clean up
            os.remove(output_json_path)

            if slack_webhook_url:
                logger.info("🚀 Sending slack message")
                payload = self.format_slack_message(
                    img_url,
                    prompt_url,
                    data.get('prompt'),
                    data.get('negative_prompt'),
                    data.get('sd_model_name')
                )
                await self.send_slack_message(payload, webhook_url=slack_webhook_url)

            logger.info("✅ Successfully uploaded to R2")


    def upload_to_r2(self, file_path):
        file_name = os.path.basename(file_path)

        bucket_name = opts.r2_bucket_name or os.environ["R2_BUCKET_NAME"]
        base_upload_path = opts.r2_upload_path or os.environ["R2_UPLOAD_PATH"]
        bucket_domain = opts.r2_domain or os.environ["R2_DOMAIN"]
        access_key_id = opts.r2_access_key_id or os.environ["R2_ACCESS_KEY_ID"]
        secret_access_key = opts.r2_secret_access_key or os.environ["R2_SECRET_ACCESS_KEY"]
        bucket_endpoint = opts.r2_endpoint or os.environ["R2_ENDPOINT"]

        r2 = R2Client(
            access_key=access_key_id,
            secret_key=secret_access_key,
            endpoint=bucket_endpoint,
        )

        upload_path = f"{base_upload_path}/{file_name}"
        logger.info(f"Uploading file to R2 - bucket_name:{bucket_name} file_path:{file_path} upload_path:{upload_path}")
        try:
            r2.upload_file(bucket_name, file_path, upload_path)
        except Exception as e:
            logger.error(f"❌ Failed to upload file to R2: {e}")
            return None

        url = f"https://{bucket_domain}/{upload_path}"
        logger.info(f"Uploaded file to R2: {url}")
        return url

        
    def format_slack_message(
        image_url: str,
        prompt_url: str,
        prompt: str,
        negative_prompt: str,
        reference_img: str,
        model: str
    ) -> dict:

        link_blocks = [
            {
                "type": "link",
                "url": image_url,
                "text": "📷 Photo link ",
                "style": {"bold": True},
            },
            {
                "type": "link",
                "url": prompt_url,
                "text": "📝 Prompt JSON ",
                "style": {"bold": True},
            },
        ]

        if reference_img:
            link_blocks.append(
                {
                    "type": "link",
                    "url": reference_img,
                    "text": "🔍 Controlnet reference",
                    "style": {"bold": True},
                }
            )

        prompt_section = {
            "type": "rich_text_quote",
            "elements": [
                {"type": "text", "text": f"🧠 Model: {model}"},
                {"type": "text", "text": f"📄 Prompt: {prompt}"},
                {"type": "text", "text": f"🚫 Negative Prompt: {negative_prompt}"} if negative_prompt else {},
            ],
        } if prompt else {}

        blocks = {
            "blocks": [
                {
                    "type": "rich_text",
                    "elements": [
                        prompt_section,
                        {"type": "rich_text_section", "elements": link_blocks},
                    ],
                },
            ]
        }
        return blocks


    async def send_slack_message(self, payload: dict, webhook_url: Optional[str] = None):
        webhook_url = webhook_url or opts.slack_webhook_url or os.environ["SLACK_WEBHOOK_URL"]
        if webhook_url is None:
            raise ValueError("Webhook URL is required to send a Slack message.")

        # Send Slack notification
        async with httpx.AsyncClient() as client:
            result = await client.post(webhook_url, json=payload)
        print(f"slack response: {result.text}")
        return result

    def on_ui_tabs():
        script_callbacks.on_after_process(R2BucketUpload())
        script_callbacks.on_after_process(R2BucketUpload())