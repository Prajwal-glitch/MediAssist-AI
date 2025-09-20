 
import chromadb
from pubmed import PubMedRetriever

class ChromaStore:

    def __init__(self,path="chromadb",name="Intermittent_Fasting"):
        self.client=chromadb.PersistentClient(path=path)
        self.col=self.client.get_or_create_collection(name=name)

    def add(self,abstracts):
        ids = []
        docs = []
        metadatas = []


        for abstract in abstracts:
            ids.append(abstract["pmid"])
            docs.append(" ".join(abstract["abstract"].values()))
            metadatas.append({
                        "pmid": abstract["pmid"],
                        "title": abstract["title"],
                        "journal": abstract["journal"],
                        "authors": abstract["authors"],
                        "publication_date": abstract["publication_date"]
                    })
            
        self.col.add(documents=docs,metadatas=metadatas,ids=ids)


    def search(self,query,k=5):
        return self.col.query(
        query_texts=["Does intermittent fasting help with obesity?"],
        n_results=2
        )

if __name__=="__main__":
    pmids=PubMedRetriever.search_pubmed_articles("intermittent fasting (IF) obesity Type 2 Diabetes metabolic disorders")
    articles=PubMedRetriever.fetch_pubmed_abstracts(pmids)
    store=ChromaStore()
    store.add(articles)
    res=store.search("intermittent fasting and diabetes")
    print(res)
