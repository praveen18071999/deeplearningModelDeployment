import io
import torch
import torch.nn as nn
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import torchvision.transforms as transforms
from fastapi.middleware.cors import CORSMiddleware


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.5)
        self.fc1 = nn.Linear(128 * 3 * 3, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 14)  # 14 classes for chestmnist dataset

    def forward(self, x):
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))
        x = self.pool(torch.relu(self.bn2(self.conv2(x))))
        x = self.pool(torch.relu(self.bn3(self.conv3(x))))
        x = x.view(x.size(0), -1)  # Flatten
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

cnn = CNN()
cnn.load_state_dict(torch.load("chestmnist.pth"))
cnn.eval()


transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class_names = [
    'Atelectasis', 'Cardiomegaly', 'Effusion', 'Infiltration', 'Mass', 'Nodule',
    'Pneumonia', 'Pneumothorax', 'Consolidation', 'Edema', 'Emphysema', 'Fibrosis',
    'Pleural_Thickening', 'Hernia'
]

# Prediction endpoint
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()  
    

    image = Image.open(io.BytesIO(contents))
    
    image = transform(image).unsqueeze(0) 

    # Perform inference
    with torch.no_grad():
        output = cnn(image)
        predictions = torch.sigmoid(output).squeeze().numpy()
    predicted_labels = {class_names[i]: f"{float(predictions[i]) * 100:.2f}%" for i in range(len(class_names))}
 
    sorted_predictions = {k: v for k, v in sorted(predicted_labels.items(), key=lambda item: float(item[1][:-1]), reverse=True)}
    
    return {"predictions": sorted_predictions}