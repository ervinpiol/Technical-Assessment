# Technical-Assessment

## Overview

This repository contains a FastAPI-based application designed for technical assessment purposes. It provides a RESTful API that can be used for various operations.

## Tech Stack

- **Backend**: FastAPI
- **Language**: Python
- **Package Manager**: uv

## Getting Started

Follow the steps below to set up the project locally:

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- uv (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ervinpiol/Technical-Assessment.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Technical-Assessment
   ```
3. Install dependencies:
   ```bash
   uv sync
   playwright install chromium
   ```
4. Run the FastAPI application:
   ```bash
   fastapi run dev
   ```
   Alternatively, if you are using VSCode, you can use the `launch.json` configuration to run the application through the Debugging feature.

## API Documentation

The application provides interactive API documentation via Swagger UI and ReDoc.

- **Swagger UI**: Accessible at `http://127.0.0.1:8000/docs`
- **ReDoc**: Accessible at `http://127.0.0.1:8000/redoc`

## Using the API

You can interact with the API in two ways:

### 1. Using Swagger UI

- Open your browser and navigate to `http://127.0.0.1:8000/docs`.
- Use the interactive interface to explore and test the API endpoints.

### 2. Using Postman

- Import the API collection into Postman.
- Use the provided endpoints to send requests and receive responses.
