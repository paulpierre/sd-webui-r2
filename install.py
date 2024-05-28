import launch
if not launch.is_installed("r2client"):
    launch.run_pip("install r2client==0.2.1", "r2client: requirements for Cloudflare R2")
if not launch.is_installed("httpx"):
    launch.run_pip("install httpx", "httpx: requirements for Cloudflare R2")
