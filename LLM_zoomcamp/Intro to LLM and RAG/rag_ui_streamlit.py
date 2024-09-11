from elasticsearch import Elasticsearch
import os
import ollama
import json
import streamlit as st

ollama.pull('phi3')

try:
    os.system("""docker run -it \
        --rm \
        --name elasticsearch \
        -m 4GB \
        -p 9200:9200 \
        -p 9300:9300 \
        -e "discovery.type=single-node" \
        -e "xpack.security.enabled=false" \
        docker.elastic.co/elasticsearch/elasticsearch:8.4.3""")


    ## Loading documents into elasticsearch database
  
    with open('./documents.json', 'rt') as f:
        docs_raw = json.load(f)
        documents = []
    for course in docs_raw:
        for doc in course['documents']:
            doc['course'] = course['course']
            documents.append(doc)
    es_client = Elasticsearch('http://localhost:9200')
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "section": {"type": "text"},
                "question": {"type": "text"},
                "course": {"type": "keyword"} 
            }
        }
    }
    index_name = 'course-questions'

    
    es_client.indices.create(index=index_name, body=index_settings)
    for doc in documents:
        es_client.index(index=index_name, document=doc)
except:
    es_client = Elasticsearch('http://localhost:9200')


def rag_elastic_phi3(query):
    result_docs = elastic_search(query)
    prompt = build_prompt(query=query, search_results=result_docs)
    answer = phi3(prompt)
    return answer

def phi3(query):
    response = ollama.chat(model='phi3:mini', messages=[
        {'role': 'user',
        'content': query}
    ])
    return response['message']['content']

def elastic_search(query):
    index_name = 'course-questions'
    search_query = {
        "size": 3,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "data-engineering-zoomcamp"
                    }
                }
            }
        }
    }
    response = es_client.search(index=index_name, body=search_query)
    result_docs = []
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    return result_docs

def build_prompt(query, search_results):
    promp_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT. Use only the facts from the CONTEXT when answering the question. 
QUESTION: {question}

CONTEXT: {context}
""".strip()
    context = ""
    for doc in search_results:
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"

    return promp_template.format(question=query, context=context).strip()

def main():
    st.title("RAG with Elasticsearch and Phi3")
    
    user_input = st.text_input("Enter your question:")
    if st.button("Ask"):
        with st.spinner("Processing..."):
            output = rag_elastic_phi3(user_input)
            st.success("Completed!")

            st.write(f'Q: {user_input}')
            st.write(f'A: {output}')
            print(output)


if __name__ == "__main__":
    main()