#!/usr/bin/env python3

import sqlite3
import argparse
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Generator, Tuple
from pydantic import BaseModel, Field

from bioinformatics_tools.FileClasses.Fasta import Fasta





# class SequenceRecord(BaseModel):
#     """Pydantic model for a sequence record."""
#     id: Optional[int] = None
#     header: str = Field(..., min_length=1, description="Sequence header/identifier")
#     sequence: str = Field(..., min_length=1, description="DNA/RNA/Protein sequence")
#     length: int = Field(..., ge=0, description="Length of the sequence")
#     gc_content: Optional[float] = Field(None, ge=0, le=100, description="GC content percentage")
#     created_at: Optional[datetime] = None


def main():
    parser = argparse.ArgumentParser(description='Convert FASTA file to SQLite database')
    parser.add_argument('-i', '--input', help='Input FASTA file path')
    # parser.add_argument('-o', '--output', help='Output SQLite database path (default: sequences.db)')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing database')
    parser.add_argument('-b', '--batch-size', type=int, default=1000,
                       help='Batch size for database inserts (default: 1000)')

    args = parser.parse_args()
    print(f'Starting main')

    # # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: FASTA file '{args.input}' not found")
        return 1

    # Step 1: Validate the fasta file
    # Init the file
    fastaClass = Fasta(file=args.input, run_mode='module')
    # test if valid
    if not fastaClass.valid:
        print(f"Error: FASTA file '{args.input}' is invalid.")
        return 1

    # print out fasta into
    print(fastaClass.fastaKey)
    # to model so we can add to our db
    print(fastaClass.to_pydantic())

if __name__ == '__main__':
    exit(main())
