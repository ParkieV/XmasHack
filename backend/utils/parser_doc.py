import json
import aspose.words as aw

MAIN = "C:\\projects\\hack\\XmasHack\\backend\\data\\"

def open_doc(name="doc.docx", format="r"):
    doc = aw.Document(name)
    return doc.get_text()


def doc(self): #for rtf/doc/docx files
        doc = aw.Document(self.input)
        doc.save(f'{self.output}\\{self.name_of_file}.txt')

def parser_doc_docx_rtf():
    jsonf = json_open(MAIN + "classes.json")
    result = dict()
    acc = 0
    for file_name in jsonf.keys():
        result[acc] = dict()
        result[acc]['file_id'] = file_name
        result[acc]['file_class'] = jsonf[file_name]
        doc_str = open_doc(MAIN + "docs\\" + file_name)
        result[acc]['file_body'] = doc_str
        acc += 1
    print("Success!")
    return result


def save_doc(doc_str: str = None):
    with open("123.txt", "w") as f_output:
        f_output.write(doc_str)

def get_paragraph(doc_str: str = None):
    doc_list = doc_str.split("\n")
    start = False
    start_paragraph = False
    paragraph = ""
    for line in doc_list:
        if "предмет договора" in line.lower():
            start = True
        elif line == "" and start is True:
            if start_paragraph is True:
                start = False
                break
            else:
                start_paragraph = True
        if start is True:
            paragraph += line + "\n"
            
    return paragraph

def json_open(path: str = None):
    with open(path) as json_file:
        jsonf = json.load(json_file)
        return jsonf



if __name__ == '__main__':
    with open(MAIN + "docx.json", "w") as f:
        json.dump(parser_doc_docx_rtf(), f)