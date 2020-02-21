import sys
import time
tot_book_types = None
tot_libraries = None
days_left = None
book_scores = None
lib_ids = None
library_tuples = [] 
# format for library_tuples:
# ([number of books in library, signup days, shipping capacity], [books in library])
# format for the output tuple
# (total libraries used, [(library id, number of books to be scanend, [array of the books id])])


def parse(path):
    global tot_book_types, tot_libraries, days_left, book_scores, library_tuples, lib_ids
    tot_book_types = None
    tot_libraries = None
    days_left = None
    book_scores = None
    lib_ids = None
    library_tuples = [] 
    with open(path) as file:
        lines = file.readlines()
        lines = list(filter(lambda s: len(s.strip("\n")) > 0, lines))
        metadata = lines[0].split(" ")
        tot_book_types = int(metadata[0])
        tot_libraries = int(metadata[1])
        lib_ids = [i for i in range(tot_libraries)]
        days_left = int(metadata[2])
        book_scores = lines[1].strip("\n").split(" ")
        book_scores = list(map(lambda score: int(score), book_scores))
        # for each library
        for i in range(2, len(lines), 2):
            metadata = list(map(lambda s: int(s), lines[i].strip("\n").split(" ")))
            books = list(map(lambda s: int(s), lines[i + 1].strip("\n").split(" ")))
            library_tuples.append((metadata, books))

def main():
    inputs = ["a_example.txt","b_read_on.txt","c_incunabula.txt","d_tough_choices.txt","e_so_many_books.txt","f_libraries_of_the_world.txt"]
    for elem in inputs:
        t1 = time.time()
        parse(elem)
        print_sol(naive_colin(),elem)
    # print(tot_book_types)
    # print(tot_libraries)
    # print(days_left)
    # print(book_scores)
    #print_sol(naive_colin())

def naive_colin():
    sorted_libs = sorted(lib_ids, key=lambda i: -get_lib_score(i))
    library_sols = []
    for i in sorted_libs:
        meta, book_array = library_tuples[i]
        sorted_books = sortBooks(i)
        library_sols.append((i, len(sorted_books), book_array))
    return (len(sorted_libs), library_sols)
        

def naive_maxime(libraries, max_days):
    libraries = sort_libs(libraries)
    libraries_length = len(libraries)
    sortBooks(libraries)
    
    signing_lib = 0
    signing_lib_duration = libraries[signing_lib][1]
    signing_lib_day_elapsed = 0
    
    do_step = True
    for i in range(max_days):
        # process signing library
        if signing_lib != -1:
            if signing_lib_day_elapsed >= signing_lib_duration:
                signing_lib = signing_lib + 1 if signing_lib <= libraries_length else -1
                signing_lib_day_elapsed = 0
            
            signing_lib_day_elapsed += 1
        
        # 
        
def get_lib_score(lib_id):
    meta, book_assortment = library_tuples[lib_id]
    my_sum = 0
    for i in book_assortment:
        my_sum += book_scores[i]
    return my_sum/meta[1]

    
def sort_libs(libraries):
    return sorted(library_tuples, key=lambda t: t[0][1])

def sortBooks(lib):
    books = (library_tuples[lib])[1]

    return sorted(books,reverse=True,key=get_score)
    

def get_score(elem):
    return book_scores[elem]

def print_sol(sol, elem):
    nf = elem[:-4] + "_output.txt"
    with open(nf,"w") as fl:
        fl.write(str(sol[0])+"\n")
        for library_id, num_books, book_array in sol[1]:
            fl.write(f"{library_id} {num_books}\n")
            for book in book_array:
                fl.write(str(book)+" ")
            fl.write("\n")

if __name__ == "__main__":
    main()
