import cloudinary
import cloudinary.uploader
cloudinary.config(
    cloud_name="dvjg6st2t",
    api_key="352511942345566",
    api_secret="JyGRhYmoWMZbE2r21GCwnCv4fyg"
)

result = cloudinary.uploader.upload_image("mohit.jpg")
print(result)
# result = cloudinary.uploader.upload("mohit.jpg")
# print(result)