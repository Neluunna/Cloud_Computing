from flask import Flask, render_template
from azure.storage.blob import BlobServiceClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

# Configuration Azure Blob Storage
connect_str = "DefaultEndpointsProtocol=https;AccountName=retoursclientsstorage;AccountKey=/EZiihDpp/0KqGc4dst2HujUNNaLaHywUaa47+fPMc22Xl3cvlWe8YFu7bwCA75Ws1ebOzSziJNg+AStrGapOw==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "retours-clients"

# Télécharger les fichiers du conteneur
container_client = blob_service_client.get_container_client(container_name)
contenu = ""
for blob in container_client.list_blobs():
    blob_client = container_client.get_blob_client(blob.name)
    contenu = blob_client.download_blob().readall().decode('utf-8')
    print(f"Contenu du fichier {blob.name} : {contenu}")

# Configuration Azure Text Analytics
endpoint = "https://francecentral.api.cognitive.microsoft.com/"
key = "b3a40941f7b4467cb58abe174af9fbbd"
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = [contenu]
response = text_analytics_client.analyze_sentiment(documents=documents)[0]
print(f"Sentiment global : {response.sentiment}")
for sentence in response.sentences:
    print(f"Phrase : {sentence.text} | Sentiment : {sentence.sentiment}")

@app.route('/')
def index():
    sentiments = {
        "positif": 10,
        "neutre": 5,
        "négatif": 2
    }
    return render_template('index.html', sentiments=sentiments)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)