
class vbe:
    """
    Praise Kumin and the book
    """
    def encode_number(self, num):
        byte_list = []
        while True:
            byte_list.insert(0, num % 128)
            if num < 128:
                break
            num = num//128
        byte_list[-1] += 128
        return byte_list

    def decode(self, num_list):
        numbers = []
        n = 0
        for i in range(len(num_list)):
            if num_list[i] < 128:
                n = 128 * n + num_list[i]
            else:
                n = 128 * n + (num_list[i] - 128)
                numbers.append(n)
                n = 0
        return numbers
