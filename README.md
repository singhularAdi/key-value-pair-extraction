## Setup
1. For running vision.py there needs to be a GCP project created with Google Vision API enabled.
2. Then a service account needs to be created associated with that API.
3. Create/Download a JSON key associated with that service account.
3. Set the GOOGLE_APPLICATION_CREDENTIALS environment variable pointing to the downloaded private key.
4. Run vision.py with the image file's full path as the first CLI argument.
