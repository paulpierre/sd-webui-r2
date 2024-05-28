from modules.processing import StableDiffusionProcessing
from modules import scripts, script_callbacks, shared
from r2client.R2Client import R2Client
from modules.shared import opts
from typing import Optional
import requests
import logging
import hashlib
import json
import os


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

    def postprocess(self, p: StableDiffusionProcessing, processed, *args, **kwargs):  #
        logger.info("⚡ [R2BucketUpload] Starting post processing ..")

        slack_webhook_url = opts.slack_webhook_url

        data = p.js()

        logger.debug(f"⚡ [R2BucketUpload] JSON data: {data}")

        if processed.images:
    
            output_file_path = p.images[0]  # Path to the output image
            file_hash = self.generate_sha256_file(output_file_path)
            output_json_path = os.path.join(os.path.dirname(output_file_path), f"{file_hash}.json")
            
            with open(output_json_path, 'w') as json_file:
                json.dump(data, json_file)
            
            
            
            logger.info(f"🔄 [R2BucketUpload] Uploading json {output_json_path} to R2")
            prompt_url = self.upload_to_r2(output_json_path)
            
            # Clean up
            os.remove(output_json_path)

            img_url = ""
            for image in processed.images:

                logger.info(f"🔄 [R2BucketUpload] Uploading image {image} to R2")
                url = self.upload_to_r2(image, file_name=f"{file_hash}.png")
                img_url += url + "\n"

            if slack_webhook_url:
                logger.info("🚀 Sending slack message")
                payload = self.format_slack_message(
                    img_url,
                    prompt_url,
                    data.get('prompt'),
                    data.get('negative_prompt'),
                    data.get('sd_model_name')
                )
                self.send_slack_message(payload, webhook_url=slack_webhook_url)

            logger.info("✅ [R2BucketUpload] Successfully uploaded to R2")
        else:
            logger.error("❌ [R2BucketUpload] No images found in processed data")

    def upload_to_r2(self, file_path, file_name: Optional[str] = None):
        file_name = file_name or os.path.basename(file_path)

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
        logger.info(f"🔄 [R2BucketUpload] Uploading file to R2 - bucket_name:{bucket_name} file_path:{file_path} upload_path:{upload_path}")
        try:
            r2.upload_file(bucket_name, file_path, upload_path)
        except Exception as e:
            logger.error(f"❌ [R2BucketUpload] Failed to upload file to R2: {e}")
            return None

        url = f"https://{bucket_domain}/{upload_path}"

        return url

    def generate_sha256_file(self, file_path):
        """
        Generate a SHA256 hash of a file.

        :param file_path: Path to the file to hash
        :return: SHA256 hash of the file
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as file:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: file.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
        
    def format_slack_message(
        self,
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


    def send_slack_message(self, payload: dict, webhook_url: Optional[str] = None):
        webhook_url = webhook_url or opts.slack_webhook_url or os.environ["SLACK_WEBHOOK_URL"]
        if webhook_url is None:
            raise ValueError("Webhook URL is required to send a Slack message.")

        # Send Slack notification
        result = requests.post(webhook_url, json=payload)
        logger.debug(f"💬 [R2BucketUpload] Slack response: {result.text}")
        return result


    @script_callbacks.on_ui_tabs
    def on_ui_tabs():
        return [R2BucketUpload()]
