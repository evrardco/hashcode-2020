import sys
tot_book_types = None
tot_libraries = None
days_left = None
book_scores = None
library_tuples = []
# format for library_tuples:
# ([number of books in library, signup days, shipping capacity], [books in library])


def parse(path):
    global tot_book_types, tot_libraries, days_left, book_scores, library_tuples
    path = sys.argv[1]
    with open(path) as file:
        lines = file.readlines()
        metadata = lines[0].split(" ")
        tot_book_types = int(metadata[0])
        tot_libraries = int(metadata[1])
        days_left = int(metadata[2])
        book_scores = lines[1].split(" ")
        book_scores = list(map(lambda score: int(score), book_scores))
        # for each library
        for i in range(2, len(lines), 2):
            metadata = list(map(lambda s: int(s), lines[i].split(" ")))
            books = list(map(lambda s: int(s), lines[i + 1].split(" ")))
            library_tuples.append((metadata, books))


def main():
    parse(sys.argv[1])
    print(library_tuples)
    print(tot_book_types)
    print(tot_libraries)
    print(days_left)
    print(book_scores)


if __name__ == "__main__":
    main()
