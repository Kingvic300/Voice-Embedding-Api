# Voice Embedding Flask API

## Overview

This Flask application provides a RESTful API for extracting, storing, and comparing audio embeddings. It allows users to upload audio files, obtain unique embeddings for voice recognition or comparison, and compare these embeddings against each other.

## Features

*   **Audio Feature Extraction**: Extracts relevant features from audio files (WAV, MP3, M4A, FLAC) to generate unique embeddings.
*   **Embedding Storage**: Stores generated embeddings with a unique `file_id` for later retrieval and comparison.
*   **Embedding Retrieval**: Allows retrieval of stored embeddings using their `file_id`.
*   **Voice Comparison**: Compares two voice embeddings and returns a similarity score or other relevant comparison metrics.
*   **Health Check**: Provides a health endpoint to check the service status.

## Setup and Installation

### Prerequisites

*   Python 3.x
*   `pip` (Python package installer)
*   `ffmpeg` (for audio processing, ensure it's in your system's PATH)

### Clone the Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### Install Dependencies

This application relies on several Python libraries. You can install them using `pip`.

```bash
pip install Flask numpy soundfile librosa scikit-learn pydub
```

*Note: The provided code snippet implies `db.py` and `embedding_service.py` modules. Ensure these files are present in the same directory as `app.py` and contain the necessary implementations for database interaction and embedding logic.* 

### Database Initialization

The `db.py` module is responsible for initializing the database. The `init_db()` function is called at the application startup. By default, it's expected to set up a SQLite database or similar lightweight solution for storing embeddings.

### Running the Application

To start the Flask API server, run the `app.py` file:

```bash
python app.py
```

The application will run on `http://0.0.0.0:5000` by default.

## API Endpoints

### 1. `POST /extract-embedding`

Extracts audio features and generates an embedding from an uploaded audio file.

*   **Request Type**: `POST`
*   **Content-Type**: `multipart/form-data`
*   **Parameters**:
    *   `audio`: The audio file to process (WAV, MP3, M4A, FLAC).

*   **Example Request (using `curl`):**

    ```bash
    curl -X POST -F "audio=@/path/to/your/audio.wav" http://localhost:5000/extract-embedding
    ```

*   **Example Response (Success):**

    ```json
    {
        "file_id": 1,
        "embedding": [0.123, 0.456, ..., 0.789],
        "feature_count": 128
    }
    ```

*   **Example Response (Error - No file):**

    ```json
    {
        "error": "No audio file provided"
    }
    ```

*   **Example Response (Error - Unsupported format):**

    ```json
    {
        "error": "Supported formats: WAV, MP3, M4A, FLAC"
    }
    ```

### 2. `GET /get-embedding/<int:file_id>`

Retrieves a stored audio embedding by its `file_id`.

*   **Request Type**: `GET`
*   **Parameters**:
    *   `file_id`: The unique identifier of the embedding.

*   **Example Request (using `curl`):**

    ```bash
    curl http://localhost:5000/get-embedding/1
    ```

*   **Example Response (Success):**

    ```json
    {
        "file_id": 1,
        "embedding": [0.123, 0.456, ..., 0.789],
        "created_at": "2023-10-27 10:00:00"
    }
    ```

*   **Example Response (Error - Not found):**

    ```json
    {
        "error": "Embedding not found"
    }
    ```

### 3. `POST /compare-voices`

Compares two voice embeddings.

*   **Request Type**: `POST`
*   **Content-Type**: `application/json`
*   **Parameters**:
    *   `embedding1`: The first voice embedding (list of floats).
    *   `embedding2`: The second voice embedding (list of floats).

*   **Example Request (using `curl`):**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"embedding1": [0.1, 0.2, 0.3], "embedding2": [0.1, 0.2, 0.3]}' http://localhost:5000/compare-voices
    ```

*   **Example Response (Success):**

    ```json
    {
        "similarity_score": 0.987
    }
    ```

*   **Example Response (Error - Missing parameters):**

    ```json
    {
        "error": "Both embedding1 and embedding2 required"
    }
    ```

### 4. `GET /health`

Checks the health status of the API.

*   **Request Type**: `GET`

*   **Example Request (using `curl`):**

    ```bash
    curl http://localhost:5000/health
    ```

*   **Example Response (Success):**

    ```json
    {
        "status": "healthy",
        "service": "voice-embedding-api"
    }
    ```

## Integration with Other Applications

This Flask API is designed to be easily integrated into various applications, regardless of the programming language. Below are examples of how to interact with this API from different environments.

### Java Implementation Example

This section demonstrates how a Java application can interact with the Voice Embedding Flask API. We will use the `java.net.http` package for making HTTP requests.

#### Prerequisites for Java

*   Java Development Kit (JDK) 11 or higher.
*   A build tool like Maven or Gradle (for dependency management, if needed).

#### Example: Extracting Embedding from Java

To extract an embedding, you'll need to send a `multipart/form-data` POST request with the audio file.

```java
import java.io.File;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class VoiceEmbeddingClient {

    private static final String API_BASE_URL = "http://localhost:5000";

    public static void main(String[] args) throws Exception {
        // Example: Extract Embedding
        File audioFile = new File("path/to/your/audio.wav"); // Replace with your audio file path
        if (!audioFile.exists()) {
            System.err.println("Audio file not found: " + audioFile.getAbsolutePath());
            return;
        }
        String fileId = extractEmbedding(audioFile);
        System.out.println("Extracted embedding with file_id: " + fileId);

        // Example: Get Embedding (assuming fileId is known)
        if (fileId != null) {
            getEmbedding(Integer.parseInt(fileId));
        }

        // Example: Compare Voices (using dummy embeddings for demonstration)
        List<Double> embedding1 = generateRandomEmbedding(128);
        List<Double> embedding2 = generateRandomEmbedding(128);
        compareVoices(embedding1, embedding2);

        // Example: Health Check
        checkHealth();
    }

    private static String extractEmbedding(File audioFile) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        String boundary = new Random().nextInt() + "";

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_BASE_URL + "/extract-embedding"))
                .header("Content-Type", "multipart/form-data;boundary=" + boundary)
                .POST(ofMimeMultipartData(audioFile.toPath(), boundary))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Extract Embedding Response Status: " + response.statusCode());
        System.out.println("Extract Embedding Response Body: " + response.body());

        // Parse file_id from response (simple JSON parsing for demonstration)
        if (response.statusCode() == 200) {
            // In a real application, use a JSON library like Jackson or Gson
            String responseBody = response.body();
            int fileIdStart = responseBody.indexOf("\"file_id\":") + "\"file_id\":".length();
            int fileIdEnd = responseBody.indexOf(",", fileIdStart);
            if (fileIdEnd == -1) {
                fileIdEnd = responseBody.indexOf("}", fileIdStart);
            }
            return responseBody.substring(fileIdStart, fileIdEnd).trim();
        }
        return null;
    }

    private static HttpRequest.BodyPublisher ofMimeMultipartData(Path file, String boundary) throws Exception {
        List<byte[]> byteArrays = new ArrayList<>();
        byteArrays.add(String.format("--%s\r\nContent-Disposition: form-data; name=\"audio\"; filename=\"%s\"\r\nContent-Type: application/octet-stream\r\n\r\n", boundary, file.getFileName().toString()).getBytes());
        byteArrays.add(Files.readAllBytes(file));
        byteArrays.add(String.format("\r\n--%s--\r\n", boundary).getBytes());
        return HttpRequest.BodyPublishers.ofByteArrays(byteArrays);
    }

    private static void getEmbedding(int fileId) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_BASE_URL + "/get-embedding/" + fileId))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Get Embedding Response Status: " + response.statusCode());
        System.out.println("Get Embedding Response Body: " + response.body());
    }

    private static void compareVoices(List<Double> embedding1, List<Double> embedding2) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        String jsonInput = String.format(
                "{\"embedding1\": %s, \"embedding2\": %s}",
                embedding1.toString().replace('[', '[').replace(']', ']'),
                embedding2.toString().replace('[', '[').replace(']', ']')
        );

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_BASE_URL + "/compare-voices"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonInput))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Compare Voices Response Status: " + response.statusCode());
        System.out.println("Compare Voices Response Body: " + response.body());
    }

    private static void checkHealth() throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_BASE_URL + "/health"))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Health Check Response Status: " + response.statusCode());
        System.out.println("Health Check Response Body: " + response.body());
    }

    private static List<Double> generateRandomEmbedding(int size) {
        Random rand = new Random();
        List<Double> embedding = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            embedding.add(rand.nextDouble());
        }
        return embedding;
    }
}
```

### Other Programming Languages

The Voice Embedding Flask API can be consumed by any programming language that supports HTTP requests. The core concepts remain the same:

*   **`POST /extract-embedding`**: Send a `multipart/form-data` request with the audio file.
*   **`GET /get-embedding/<file_id>`**: Perform a `GET` request to the specific URL.
*   **`POST /compare-voices`**: Send a `POST` request with a JSON payload containing the two embeddings.
*   **`GET /health`**: Perform a simple `GET` request.

Libraries commonly used for HTTP requests in other languages include:

*   **Python**: `requests`
*   **JavaScript (Node.js/Browser)**: `fetch` API, `axios`
*   **Ruby**: `Net::HTTP`
*   **Go**: `net/http`

Remember to handle JSON parsing for responses and construct request bodies (especially for `multipart/form-data` and JSON payloads) according to the API specifications.

## Contributing

Feel free to fork the repository, submit pull requests, or open issues for bugs and feature requests.

## License

This project is open-source and available under the [MIT License](LICENSE).

