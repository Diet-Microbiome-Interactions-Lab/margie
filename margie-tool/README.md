# 🧬 Snakemake Tinkering

Experimental implementation of the margie genome annotation pipeline using Snakemake for workflow management.

## Architecture

```
FASTA → Validate → SQLite DB → Snakemake Pipeline → Update DB → Results
```

### Components

1. **`src/pipeline.py`** - Main pipeline controller
   - `GenomeAnnotationPipeline` - Orchestrates the entire workflow
   - `AnnotationDatabase` - Manages SQLite database operations

2. **`workflows/annotation.smk`** - Snakemake workflow
   - Gene prediction (Prodigal)
   - PFAM annotation (HMMER)
   - TIGRfam annotation (HMMER)
   - Database updates
   - Report generation

3. **`tests/test_pipeline.py`** - Testing suite

## Quick Start

### 1. Test the Pipeline
```bash
# From the snakemake-tinkering directory
python tests/test_pipeline.py
```

### 2. Run with Your Own FASTA
```python
from src.pipeline import GenomeAnnotationPipeline

# Initialize pipeline
pipeline = GenomeAnnotationPipeline(
    fasta_file="your_genome.fasta",
    output_dir="results/",
    config={
        "pfam_database": "/path/to/Pfam-A.hmm",
        "tigrfam_database": "/path/to/TIGRFAMs.hmm"
    }
)

# Run the pipeline
db_path = pipeline.run()

# Get results summary
summary = pipeline.get_annotations_summary()
print(summary)
```

### 3. Query the Results Database
```python
from src.pipeline import AnnotationDatabase

db = AnnotationDatabase("results/annotations.db")

# Get all annotations for a sequence
annotations = db.get_sequence_annotations("sequence_header")

for ann in annotations:
    print(f"{ann['annotation_type']}: {ann['description']}")
```

## Database Schema

### Tables

**`sequences`**
- `id` - Primary key
- `header` - FASTA header
- `sequence` - DNA/RNA sequence
- `length` - Sequence length
- `gc_content` - GC content percentage
- `created_at` - Timestamp

**`annotations`**
- `id` - Primary key
- `sequence_id` - Foreign key to sequences
- `annotation_type` - Type (pfam, tigrfam, etc.)
- `tool` - Tool used (hmmscan, etc.)
- `start_pos`, `end_pos` - Position on sequence
- `score`, `evalue` - Statistical measures
- `description` - Annotation description
- `raw_data` - JSON for additional data
- `created_at` - Timestamp

**`pipeline_runs`**
- `id` - Primary key
- `fasta_file` - Input file path
- `output_dir` - Output directory
- `status` - running/completed/failed
- `started_at`, `completed_at` - Timestamps
- `config` - JSON configuration

## Workflow Steps

1. **Validation** - Validate FASTA file using bioinformatics_tools
2. **Database Init** - Create SQLite database and add sequences
3. **Gene Prediction** - Use Prodigal to predict genes
4. **PFAM Annotation** - Run HMMER against PFAM database
5. **TIGRfam Annotation** - Run HMMER against TIGRfam database
6. **Database Update** - Add all annotations to database
7. **Report Generation** - Create HTML summary report

## Customization

### Adding New Annotation Tools

1. **Add rule to `workflows/annotation.smk`**:
   ```python
   rule new_annotation:
       input: "proteins.faa"
       output: "new_results.txt"
       shell: "your_tool {input} > {output}"
   ```

2. **Update database parser in `src/pipeline.py`**:
   ```python
   def add_annotation_results(self, annotation_type, tool, results_file):
       # Add parser for your tool's output format
   ```

3. **Add to pipeline config**:
   ```yaml
   new_tool_database: "/path/to/database"
   ```

## Dependencies

- Python 3.9+
- bioinformatics_tools (your local package)
- Snakemake (for production use)
- SQLite3 (built into Python)

## Next Steps

- [ ] Integrate real Snakemake execution
- [ ] Add more annotation tools (COG, KEGG, etc.)
- [ ] Implement proper result parsers for each tool
- [ ] Add visualization of results
- [ ] Performance optimization for large genomes
- [ ] Add configuration validation

## Notes

Currently uses mock/simulated annotation results for demonstration. Replace the shell commands in the Snakemake rules with real tool calls once you have the annotation databases set up.