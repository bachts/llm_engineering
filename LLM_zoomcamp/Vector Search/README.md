This is a code-along with some modifications for DataTalksClub LLMZoomcamp chapter 1 and 2 that can be found [here](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/03-vector-search).

# Concepts

## What are vector data and vector DB?
Vector data is the representation of different data points, querys, pictures, texts,... as vectors, similar to how word embeddings or semantic embeddings are formed in NLP applications, often used in search engines,... It provides a structured way to store unstructured data, such as images, audio, videos, acting as a nice interface for our searching tasks.
Vector DBs provide the ability to store and retrieve data for LLMs, without comprising performance by adding to their prompts.

## Creating vector embeddings

Gather dataset -> Data pre-processing -> Training ML Model -> Embeddings -> Evaluate qualities -> Model for embeddings

## Vector DBS:
Indexes and store vector embeddings, often linked to their respective object, able to compare multiple things at once, making it very efficient for models to remember and source of truth for the data.