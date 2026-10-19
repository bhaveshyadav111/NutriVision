from huggingface_hub import login, upload_folder

# (optional) Login with your Hugging Face credentials
login()

# Push your model files
upload_folder(folder_path="NutriVision/models/Nutriv2.", repo_id="Bhavesh540/Nutriv2", repo_type="model")
