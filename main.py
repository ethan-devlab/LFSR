# coding=utf-8

# from texttable import Texttable
import streamlit as st
import pandas as pd


moose_table_A = {
    "0": "E",
    "00": "I",
    "000": "S",
    "0000": "H",
    "0001": "V",
    "001": "U",
    "0010": "F",
    "01": "A",
    "010": "R",
    "0100": "L",
    "011": "W",
    "0110": "P",
    "0111": "J",
    "1": "T",
    "10": "N",
    "100": "D",
    "1000": "B",
    "1001": "X",
    "101": "K",
    "1010": "C",
    "1011": "Y",
    "11": "M",
    "110": "G",
    "1100": "Z",
    "1101": "Q",
    "111": "O"
}

moose_table_B = {
    "E": "0",
    "I": "00",
    "S": "000",
    "H": "0000",
    "V": "0001",
    "U": "001",
    "F": "0010",
    "A": "01",
    "R": "010",
    "L": "0100",
    "W": "011",
    "P": "0110",
    "J": "0111",
    "T": "1",
    "N": "10",
    "D": "100",
    "B": "1000",
    "X": "1001",
    "K": "101",
    "C": "1010",
    "Y": "1011",
    "M": "11",
    "G": "110",
    "Z": "1100",
    "Q": "1101",
    "O": "111"
}


def showMoose(plaintext):
    encoded = ""
    plaintext = plaintext.upper()
    length = 0
    for i in range(len(plaintext)):
        encoded += moose_table_B[plaintext[i]] + " "
        length += len(moose_table_B[plaintext[i]])
    return encoded[:-1], length


def preprocess(plaintext: str, rule: list, seed: list):
    rule = [len(seed) - 1 - i for i in rule]  # Inverse the XOR bits
    initList = []
    init = 0
    for i in rule:
        init ^= seed[i]
    initList.append(init)
    for i in seed:
        initList.append(i)

    return initList, rule


def LSFR(encoded, bList, rule):
    initList_ = list(map(str, bList))
    initList_ += [""] * 3
    cipherbit = ""
    encoded_ = "".join(encoded.split())
    rowList = [initList_]

    for i in range(1, len(encoded_) + 1):
        k = bList.pop(-1)
        tempList = []
        temp = 0
        for j in rule:
            temp ^= bList[j]
        bList.insert(0, temp)
        tempList += bList
        tempList.append(str(k))
        tempList.append(encoded_[i - 1])  # append p
        tempList.append(str(int(encoded_[i - 1]) ^ k))  # append c
        cipherbit += str(int(encoded_[i - 1]) ^ k)
        rowList.append(tempList)

    return rowList, cipherbit


def printTable(seed_size, rowList):
    bit = "b"
    header = [str(bit + str(i)) for i in range(seed_size, -1, -1)]
    header += ["K", "P", "C"]
    index = ["Initial"]
    for i in range(1, len(rowList)):
        index.append(str(i))

    return header, index


def main():
    st.set_page_config(page_title="LFSR Calculator")
    st.title("Linear Feedback Shift Register")
    plaintext = st.text_input("Plaintext").upper()
    encoded = ""
    if plaintext:
        encoded, length = showMoose(plaintext)
        st.write(f"Moose Code of {plaintext}: {encoded}")
        st.write(f"Moose Code length:  {length}")

    seed = st.text_input("SEED")
    rule = list(map(int, st.text_input(u"Bits to XOR (Start at 0 from the right): ",
                                       placeholder="1 3 5").split()))
    if st.button("Calculate"):
        seed_ = list(map(int, seed))
        rule_text = f"XOR Rule: b{len(seed)} = "
        for i in range(len(rule)):
            rule_text += f"b{rule[i]}"
            if i != len(rule) - 1:
                rule_text += " ⊕ "    # print(u'\N{CIRCLED PLUS}')
        st.write(rule_text)
        st.write(f"\nSEED: {seed}")

        bList, rule = preprocess(plaintext, rule, seed_)
        rowList, cipherbit = LSFR(encoded, bList, rule)

        st.write(f"Plaintext: {plaintext} ({encoded})")
        st.write(f"Ciphertext: {cipherbit}")
        header, index = printTable(len(seed), rowList)
        df = pd.DataFrame(rowList, columns=header, index=index).astype(str)  # handle empty str problem
        st.table(df)


if __name__ == "__main__":
    main()