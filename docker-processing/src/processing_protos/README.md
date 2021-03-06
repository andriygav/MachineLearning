Generate python grpc protocol files.
```
python3 -m grpc_tools.protoc \
    -I ./proto/ \
    --python_out=. \
    --grpc_python_out=. \
    ./proto/example_protos/*.proto
```