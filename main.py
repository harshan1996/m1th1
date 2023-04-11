class Indexer:
    def __init__(self, pages, exclude_words_file, results_file):
        self.pages = pages
        self.exclude_words_file = exclude_words_file
        self.results_file = results_file
        self.exclude_words = []
        self.results = {}

    def read_exclude_words(self):
        with open(self.exclude_words_file, "r") as f:
            self.exclude_words = f.read().split("\n")

    def clean_data(self, data):
        import re
        # removing unnecessary characters i.e data cleaning and storing the words in a list
        cleaned_data = re.sub(
            '[\n,.,),(,/,\,'',"",\d,:,;,-,,]', " ", data).split()
        cleaned_data_lowercase = list(
            set([word.lower() for word in cleaned_data]))
        return cleaned_data_lowercase

    def index_of_words(self):
        self.read_exclude_words()
        for current_page_number, page_name in enumerate(self.pages, 1):
            with open(page_name, "r") as f:
                data = f.read()
                cleaned_data = self.clean_data(data)
                for word in cleaned_data:
                    if word not in self.exclude_words:
                        # checking to see whether we are encountering the same word in the subsequent pages
                        if word not in self.results.keys():
                            self.results[word] = current_page_number
                        else:
                            page_number = self.results.get(word)
                            self.results[word] = f"{page_number},{current_page_number}"

        # list of tuples containing word and their corresponding page numbers getting sorted in the alphabetically order.
        sorted_results = list(sorted(self.results.items()))

        # writing the data to the index.txt and then closing it after it is done.
        with open(self.results_file, "w") as f:
            f.write("Word: Page Numbers \n-------------------\n")
            for data in sorted_results:
                f.write(f"{data[0]} : {data[1]} \n")
        return sorted_results


if __name__ == "__main__":
    pages = ["Page1.txt", "Page2.txt", "Page3.txt"]
    exclude_words_file = "exclude-words.txt"
    results_file = "index.txt"
    indexer = Indexer(
        pages=pages, exclude_words_file=exclude_words_file, results_file=results_file)
    indexer.index_of_words()
    print("message: results are stored in index.txt")
