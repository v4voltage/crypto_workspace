import numpy as np

# Hash function
def encrypt_password(g):
    # Create identity matrix
    n = 32  # size of the identity matrix
    T = np.eye(n) # passing the size of the matrix as an argument

    # Randomly switch the columns of matrix using seed value
    seed_value = 43
    np.random.seed(seed_value)
    num_columns = T.shape[1]
    column_indices = np.random.permutation(num_columns)
    permuted_T = T[:, column_indices]

    M = len(T)
    N = len(g)
    # Get ASCII code for alphanumeric characters
    indices = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))
    indices_chars = list(map(chr,indices))

    # Choose random characters to add to the original password
    c_ascii = np.random.choice(indices, size=M-N, replace=False)
    c = list(map(chr,c_ascii))
    g_ascii = list(bytes(g, "ascii"))
    g_ascii_transposed = np.transpose(g_ascii)
    c_ascii_transposed = np.transpose(c_ascii)
    T1 = permuted_T[:M, :N] # MxN
    T2 = permuted_T[:M, N:M] # Mx(M-N)

    # Hide the original password in the combined password
    GC_ascii = np.dot(T1,g_ascii) + np.dot(T2,c_ascii)

    # Convert combined password to a list of characters 
    integer_matrix = GC_ascii.astype(np.int32)
    sent_password = np.transpose(list(map(chr,integer_matrix)))
    matrix_string = ''.join([' '.join(map(str, row)) for row in sent_password])

    # Apply Caesar Cipher with shift of 31
    string_input = matrix_string

    shift_input = 31

    input_length = len(string_input)

    string_output = ""

     # Shift each character by 31 places
    for i in range(input_length):
        character = string_input[i]
        location_of_character = indices_chars.index(character)
        new_location = (location_of_character + shift_input) % 62
        string_output += indices_chars[new_location]

    return string_output