# My Personal Site

Uses Djot as its markup language. Depends on Pandoc version 3.9.0.2.

## Building

To convert the Djot content to HTML and extract metadata, run the following script:

```bash
#!/bin/bash
mkdir -p dist

for file in content/*.dj; do
    filename=$(basename "$file" .dj)
    echo "Processing $filename..."
    
    # Generate HTML
    pandoc -f djot -t html --lua-filter djot.lua "$file" -o "dist/$filename.html"
    
    # Extract Metadata
    pandoc -f djot --lua-filter djot-metadata.lua "$file" > "dist/$filename.json"
done

echo "Build complete. Files in dist/"
ls -F dist/
```
