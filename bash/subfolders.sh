for dir in */; do 
    [ ! -d "$dir/compilation_output" ] && mkdir -p "$dir/compilation_output" && echo "Created $dir/compilation_output" || echo "Skipped $dir/compilation_output (exists)"
done
