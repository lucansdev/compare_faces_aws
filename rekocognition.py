import boto3
from pathlib import Path
from PIL import Image,ImageDraw

client = boto3.client('rekognition')

def compare_faces(source_path,target_image_path,similarity_threshold=80):
    with open(source_path,"rb") as source_image,open(target_image_path,"rb") as target_image:
        response = client.compare_faces(SourceImage={"Bytes":source_image.read()},TargetImage={"Bytes":target_image.read()},SimilarityThreshold=similarity_threshold)
    return response

def get_rectangle(target_path,face_details):
    image = Image.open(target_path)
    draw = ImageDraw.Draw(image)
    print(draw)

    widht,height = image.size

    for face in face_details:
        box = face["Face"]["BoundingBox"]
        left = int(box["Left"] * widht)
        top = int(box["Top"] * height)
        right = int((box["Left"] + box["Width"]) * widht)
        bottom = int((box["Top"] + box["Height"]) * height)

        draw.rectangle([left,top,right,bottom],outline="red",width=3)
        draw.text((left,top-10),text=f"{face["Similarity"]:.1f}",fill="red")
        image.show()
    

if __name__ == "__main__":
    source_path = str(Path(__file__).parent/"images"/"ney_barca.png")
    target_image_path = str(Path(__file__).parent/"ney_atual.png")
    response = compare_faces(source_path,target_image_path)
    face_details = response["FaceMatches"]
    get_rectangle(target_image_path,face_details)