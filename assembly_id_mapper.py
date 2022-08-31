# inspired by https://www.biostars.org/p/141581/

import argparse
import time

from Bio import Entrez



def perform_id_mapping(idlist):
	for id_ in idlist:
		handle = Entrez.esearch(db="assembly", term=f"{id_}")
		record = Entrez.read(handle)
	
		for assembly_id in record["IdList"]:
			handle = Entrez.esummary(db="assembly", id=assembly_id, report="full")
			record_assemble = Entrez.read(handle)
	
			synonyms = record_assemble['DocumentSummarySet']['DocumentSummary'][0]['Synonym']
	
			print(
				id_,
				record_assemble['DocumentSummarySet']['DocumentSummary'][0]['AssemblyAccession'], 
				synonyms.get("Genbank"),
				synonyms.get("RefSeq"),
				synonyms.get("Similarity"),
				sep="\t", flush=True
			)
	
			time.sleep(5)



def main():


	ap = argparse.ArgumentParser()
	ap.add_argument("idfile", type=str)
	ap.add_argument("email", type=str)
	args = ap.parse_args()

	Entrez.email = args.email

	with open(args.idfile) as _in:	
		idlist = [line.strip() for line in _in]

	perform_id_mapping(idlist)


if __name__ == "__main__":

	main()
