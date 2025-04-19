docker run -d \
  -p 8080:80 \
  -v $(pwd)/data/chroma_storage:/opt/app/data/chroma_storage \
  sombra/datathon